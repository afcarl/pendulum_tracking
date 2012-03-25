import math
import time
import numpy as np 

class KalmanFilter: 
    def __init__(self):
        # Process noise (TODO estimate it. ALS technique)
        self.Q = np.eye(2)*1e-4

        # Observation noise
        self.R = np.eye(2)*1e-2        

        # Observation model
        self.H = np.array([[1, 0]])

        # Estimate covariance
        self.P = np.zeros_like(self.Q)

        # Time at which the last observation has been taken
        self.last_obs = time.time();

        self.last_theta = math.radians(45)
        
    def predict(self, x, y):
        # Compute time elapsed
        curr_time = time.time()
        dt = curr_time - self.last_obs
        self.last_obs = curr_time
        
        # Estimate angle and angular velocity
        # Note: this transformation from observed
        # ball center to angle and angular velocity 
        # should be put into H
        theta = (math.pi/2.0) - math.atan2(y, x)
        theta_dot = (theta - self.last_theta)/dt
        self.last_theta = theta
        
        print '%d %d angle %f'%(x, y, math.degrees(theta))
        
        # F could also be kept constant given small constant values for dt
        F = np.array([[1, dt], [(-9.81/0.28)*dt, 1]])

        # Predict        
        self.x = F*self.x
        self.P = F*self.P*F.T + self.Q
        
        # Update 
        y = z - self.H*self.x
        S = self.H*self.P*self.H.T + self.R
        K = self.P*self.H.T*np.inv(S)
        self.x = self.x + K*y
		self.P = self.P - self.K * self.H * self.P
              
        return self.x
        
if __name__=="__main__": 
    filter = KalmanFilter()
    filter.predict()        
    
