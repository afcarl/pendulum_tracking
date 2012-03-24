import numpy as np 
import math

class KalmanFilter: 
    def __init__(self):
        self.x = 0
        self.z = 0
        self.P = np.zeros(10)        
        
    def predict(self, x, y):
        alpha = math.atan2(y, x)
        print '%d %d angle %f'%(x, y, math.degrees(math.pi/2.0 - alpha))
        
    def update(self):
        print 'update'
        
if __name__=="__main__": 
    filter = KalmanFilter()
    filter.predict()        
    
