import cv
from blob import BlobDetector

class ColorBlobTracker: 
    def __init__(self): 
        self.capture = cv.CreateCameraCapture(0) 
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT, 240);        
        self.detector = BlobDetector()

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

            #self.detector.detect(cv.fromarray(img_th))
            roi = self.detector.detect(cv.GetMat(img_th))
            for k in roi:
                if roi[k].count > 50:
                    cv.Rectangle(img, (roi[k].x1, roi[k].y1), (roi[k].x2, roi[k].y2), cv.RGB(255, 0, 0), 2)
                


            # Display the thresholded image 
            cv.ShowImage('Tracking', img) 

            if cv.WaitKey(10) == 27: 
                break 

if __name__=="__main__": 
    tracker = ColorBlobTracker()
    tracker.run()
