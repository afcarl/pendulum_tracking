import cv
import time
import math
import serial

from blob import BlobDetector
from KalmanFilter import KalmanFilter

class ColorBlobTracker: 
    def __init__(self):
        self.IMAGE_WIDTH = 320
        self.IMAGE_HEIGHT = 240
        
        # PID parameters
        self.KP = 0.035
        self.KI = 0.045
        self.KD = 0.005        
        
        self.prev_errx = 0
        self.prev_erry = 0

        self.integral_x = 0
        self.integral_y = 0
        
        self.curr_yaw = 90
        self.curr_pitch = 90
        
        self.last_obs = time.time()

        # Open the camera       
        self.capture = cv.CreateCameraCapture(0) 
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH, self.IMAGE_WIDTH)
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT, self.IMAGE_HEIGHT);     
        
        # Union-Find Connected Comonent Labeling
        self.detector = BlobDetector()
  
        # Kalman filter
        self.filter = KalmanFilter()
   
        # Open the serial port to the arduino
        print 'Opening serial port  ...'
        self.serial = serial.Serial('/dev/ttyACM0', 19200)
        time.sleep(2)
        print 'Moving servos to initial position ...'
        self.serial.write('90s90t')
        time.sleep(1)      
    
    def _MoveCameraHead(self, ballx, bally, angle):
        # Apply PID control to keep ball center in middle
        err_x = int(self.IMAGE_WIDTH/2) - ballx
        err_y = int(self.IMAGE_HEIGHT/2) - bally
        
        curr_time = time.time()
        dt = curr_time - self.last_obs
        self.last_obs = curr_time

        self.integral_x = self.integral_x + (err_x * dt)
        self.integral_y = self.integral_y + (err_y * dt)
        
        derivative_x = (err_x - self.prev_errx)/dt
        derivative_y = (err_y - self.prev_erry)/dt
        
        correction_x = self.KP*err_x + self.KI*self.integral_x + self.KD*derivative_x      
        self.curr_yaw = int(self.curr_yaw + correction_x)
        if (self.curr_yaw > 135):
            self.curr_yaw = 135
        elif (self.curr_yaw < 45):
            self.curr_yaw = 45
            
        correction_y = self.KP*err_y + self.KI*self.integral_y + self.KD*derivative_y      
        self.curr_pitch = int(self.curr_pitch + correction_y)
        if (self.curr_pitch > 135):
            self.curr_pitch = 135
        elif (self.curr_pitch < 45):
            self.curr_pitch = 45            
        
        print 'Correction x %f for error %d, command %d dt %f'%(correction_x, err_x, self.curr_yaw, dt)
        print 'Correction x %f for error %d, command %d dt %f'%(correction_y, err_y, self.curr_pitch, dt)
                
        self.serial.write('%ds%dt'%(self.curr_yaw, self.curr_pitch))
        
        self.prev_errx = err_x        
        self.prev_erry = err_y        
        
    def run(self): 
        while True: 
            img = cv.QueryFrame( self.capture ) 

            img_undist = cv.CreateImage(cv.GetSize(img), 8, 3)
            self.filter.undistort(img, img_undist)
            img = img_undist

            # Convert the BGR image to HSV space for easier color thresholding
            img_hsv = cv.CreateImage(cv.GetSize(img), 8, 3) 
            cv.CvtColor(img, img_hsv, cv.CV_BGR2HSV) 

            # Smooth the image with a Gaussian Kernel
            cv.Smooth(img_hsv, img_hsv, cv.CV_BLUR, 3); 
            
            # Threshold the HSV image to find yellow objects
            img_th = cv.CreateImage(cv.GetSize(img_hsv), 8, 1) 
            cv.InRangeS(img_hsv, (20, 100, 100), (30, 255, 255), img_th)

            # Connected Component Analysis
            roi = self.detector.detect(cv.GetMat(img_th))
            if len(roi) == 0:
                continue;
                
            # Only consider the biggest blob
            i = max(roi, key=lambda x:roi.get(x).count)
            blob = roi[i]

            # Filter out blobs that are smaller
            if blob.count > 50:
                # Draw bounding box and center of object
                center_x = int(blob.x1 + (blob.x2 - blob.x1)/2.0)
                center_y = int(blob.y1 + (blob.y2 - blob.y1)/2.0)
                
                cv.Rectangle(img, (blob.x1, blob.y1), (blob.x2, blob.y2), cv.RGB(255, 0, 0), 2)
                cv.Circle(img, (center_x, center_y), 2, cv.RGB(255, 0, 0), -1)

                # Draw cross
                cv.Line(img, (int(img.width/2), 0), (int(img.width/2), img.height), cv.RGB(0, 0, 0))
                cv.Line(img, (0, int(img.height/2)), (img.width, int(img.height/2)), cv.RGB(0, 0, 0))
               
                # Apply Kalman filter
                xhat = self.filter.predictUpdate(self.curr_pitch, self.curr_yaw, center_x, center_y)
                print math.degrees(xhat[0])
                #self._MoveCameraHead(center_x, center_y, angle)
                
                # Draw predicted object center
                                
            # Display the thresholded image 
            cv.ShowImage('Tracking', img_undist) 
                        
            if cv.WaitKey(10) == 27: 
                break 
                
        self.serial.close()                

if __name__=="__main__": 
    tracker = ColorBlobTracker()
    tracker.run()
