import math
import time
import numpy as np 
from numpy import linalg

class KalmanFilter: 
    def __init__(self):
        # Initial process state
        self.x = np.matrix([[0], [0]])
        
        # Process noise (TODO estimate it. ALS technique)
        self.Q = np.eye(2)*1e-4

        # Observation noise
        self.R = np.eye(2)*1e-2        

        # Observation model
        self.H = np.eye(2)

        # Estimate covariance
        self.P = np.zeros_like(self.Q)

        # Time at which the last observation has been taken
        self.last_obs = time.time();

        self.last_theta = 0
        
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
        z = np.matrix([[theta], [theta_dot]])
        self.last_theta = theta
        
        print '%d %d angle %f velocity %f'%(x, y, math.degrees(theta), theta_dot)
        
        # F could also be kept constant given small constant values for dt
        F = np.matrix([[1, dt], [(-9.81/0.28)*dt, 1]])

        # Predict      
        self.x = F*self.x   
        self.P = F*self.P*F.T + self.Q
        
        # Update 
        y = z - self.H*self.x
        S = self.H*self.P*self.H.T + self.R
        K = self.P*self.H.T*linalg.inv(S)
        self.x = self.x + K*y
        self.P = self.P - K *self.H*self.P
        
        return self.x
        
if __name__=="__main__": 
    filter = KalmanFilter()
    filter.predict(-11, 121)        
    
