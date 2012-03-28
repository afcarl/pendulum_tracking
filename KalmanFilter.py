import cv
import math
import time
import numpy as np 
from numpy import linalg

class KalmanFilter: 
    def __init__(self):
        # Initial process state
        self.x = np.array([0, 0]).T
        
        # Process noise (TODO estimate it. ALS technique)
        self.Q = np.eye(2)*1e-4

        # Observation noise
        self.R = np.eye(3)*1e-2        

        # Estimate covariance
        self.P = np.zeros_like(self.Q)

        # Time at which the last observation has been taken
        self.last_obs = time.time();
        
        # Camera calibration matrix
        self.K = np.array([[353.526260, 0.000000, 190.146881], 
           [0.000000, 356.349156, 138.256491],
           [0.000000, 0.000000, 1.000000]])   
        
        # Inverse calibration matrix
        self.Kinv = np.linalg.inv(self.K)
        
        # Matrices for undistort       
        self.cv_camera_matrix = cv.fromarray(self.K)        
        self.distortion_coefficients = cv.fromarray(np.matrix([0.053961, -0.153046, 0.001022, 0.017833, 0.0000]))
        
        # Camera frame with respect to fixed frame
        self.Pcf = np.array([0.0, 0.3, 0.48]).T
        
        # Length of the string
        self.l = 0.30
        
    def undistort(self, src, dst):
        '''Undistort the image from distortion coefficients'''
        cv.Undistort2(src, dst, self.cv_camera_matrix, self.distortion_coefficients)
    
    def project(self, pitch, yaw, x, y):
        '''Backproject the (x, y) position'''
        z = self.Pcf[2]
        Pbc = np.dot(self.Kinv, np.array([x, y, 1]).T)
        return np.dot(Pbc, z)
       
    def h(self, pitch, yaw):
        '''Brings the ball position x in camera frame'''
        Rx = np.array([[1, 0, 0],
                       [0, math.cos(yaw), math.sin(yaw)], 
                       [0, -1*math.sin(yaw), math.cos(yaw)]])
                       
        Ry = np.array([[math.cos(pitch), 0, -1*math.sin(pitch)], 
                       [0, 1, 0], 
                       [math.sin(pitch), 0, math.cos(pitch)]])
                       
        theta = self.x[0]
        Pbf = np.array([self.l*math.sin(theta), self.l*math.cos(theta), 0]).T

        return np.dot(np.dot(Ry, Rx).T, Pbf - self.Pcf)
        
    def jacobian(self, pitch, yaw):
        '''Jacobian of h'''
        theta = self.x[0]
        l = self.l
        H = np.array([[l*math.cos(yaw)*math.cos(theta), 0], 
                      [l*math.sin(pitch)*math.sin(yaw)*math.cos(theta) - l*math.cos(pitch)*math.sin(theta), 0],
                      [-1*math.sin(yaw)*math.cos(pitch)*l*math.cos(theta) - l*math.sin(pitch)*math.sin(theta), 0]])      
        return H
                      
    def predictUpdate(self, pitch, yaw, cx, cy):
        '''Execute the predict and update steps'''      
        # Compute time elapsed
        curr_time = time.time()
        dt = curr_time - self.last_obs
        self.last_obs = curr_time
               
        # Dynamical model
        F = np.array([[1, dt], [(-9.81/0.28)*dt, 1]])

        # Predict
        self.x = np.dot(F, self.x)
        self.P = np.dot(F, np.dot(self.P, F.T)) + self.Q
        
        # Update
        z = self.project(pitch, yaw, cx, cy)
        y = z - self.h(pitch, yaw)
        
        H = self.jacobian(pitch, yaw)
        S = np.dot(H, np.dot(self.P, H.T)) + self.R
        K = np.dot(self.P, np.dot(H.T, linalg.inv(S)))
        self.x = self.x + np.dot(K, y)
        self.P = self.P - np.dot(K, np.dot(H, self.P))
        
        return self.x
        
if __name__=="__main__": 
    filter = KalmanFilter()
    print filter.backproject(math.radians(0), math.radians(0), 0, 0)
    
