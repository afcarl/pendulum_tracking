import cv 

class ColorBlobTracker: 
    def __init__(self): 
        self.capture = cv.CreateCameraCapture(0) 
        
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

            # Display the thresholded image        
            cv.ShowImage('Tracking', img_th) 
            
            if cv.WaitKey(10) == 27: 
                break 
                
if __name__=="__main__": 
    tracker = ColorBlobTracker() 
    tracker.run() 
