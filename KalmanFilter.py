import math
import time
import numpy as np 

class KalmanFilter: 
    def __init__(self):
        # Current state estimate
        self.xhat = 0     
        # Estimate at t-1
        self.xhatp = 0
        # Time at which the last observation has been taken
        self.last_obs = 0;      
        self.k = math.sqrt(9.81/0.28)

    def _StateTransition(self):
        delta_t = time.time() - self.last_obs
        #theta_t = delta_t * (self.k*(-1.0*math.radians(45)))*math.sin(self.k*
        
        
    def predict(self, x, y):
        alpha = math.atan2(y, x)
        print '%d %d angle %f'%(x, y, math.degrees(math.pi/2.0 - alpha))
        return math.pi/2.0 - alpha
        
    def update(self):
        print 'update'
        
if __name__=="__main__": 
    filter = KalmanFilter()
    filter.predict()        
    
