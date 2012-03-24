import cv
from blob import BlobDetector
from KalmanFilter import KalmanFilter

class ColorBlobTracker: 
    def __init__(self): 
        self.capture = cv.CreateCameraCapture(0) 
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT, 240);        
        self.detector = BlobDetector()
        self.filter = KalmanFilter()
        
    def run(self): 
        while True: 
            img = cv.QueryFrame( self.capture ) 

            # Smooth the image with a Gaussian Kernel
            cv.Smooth(img, img, cv.CV_BLUR, 3); 

            # Convert the BGR image to HSV space for easier color thresholding
            img_hsv = cv.CreateImage(cv.GetSize(img), 8, 3) 
            cv.CvtColor(img, img_hsv, cv.CV_BGR2HSV) 

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

                cv.Line(img, (int(img.width/2), 0), (int(img.width/2), img.height), cv.RGB(0, 0, 0))
                #cv.Line(img, (0, int(img.height/2)), (img.width, int(img.height/2)), cv.RGB(0, 0, 0))

                # Apply Kalman filter
                center_x = int(center_x - (img.width/2.0))
                self.filter.predict(center_x, center_y)

            # Display the thresholded image 
            cv.ShowImage('Tracking', img) 
            if cv.WaitKey(10) == 27: 
                break 

if __name__=="__main__": 
    tracker = ColorBlobTracker()
    tracker.run()
