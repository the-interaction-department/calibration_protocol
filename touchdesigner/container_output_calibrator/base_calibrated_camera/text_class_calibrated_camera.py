import numpy as np
import cv2 as cv
import glob

class CalibratedCamera:

	def __init__(self):
		self.chessboard_dims = (7, 6)
		self.window_size = (11, 11)

	def Find_object_points(self, load_path):
		"""Step 1: https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html"""

		# Termination criteria
		criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

		# Prepare object points, like (0, 0, 0), (1, 0, 0), (2, 0, 0) ...., (6, 5, 0)
		default_object_points = np.zeros((6 * 7, 3), np.float32)
		default_object_points[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
		
		# 3D point in real world space
		self.object_points = [] 

		# 2D points in image plane
		self.image_points = [] 

		images = glob.glob('{}/*.jpg'.format(load_path))

		for index, file_name in enumerate(images):
		    image = cv.imread(file_name)
		    self.height, self.width = image.shape[:2]

		    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

		    # Find the chess board corners
		    ret, corners = cv.findChessboardCorners(gray, self.chessboard_dims, None)

		    # If found, add object points, image points (after refining them)
		    if ret:
		        self.object_points.append(default_object_points)

		        corners2 = cv.cornerSubPix(gray, corners, self.window_size, (-1, -1), criteria)
		        self.image_points.append(corners)

		        # Draw and display the corners
		        cv.drawChessboardCorners(image, self.chessboard_dims, corners2, ret)
		        cv.imwrite('{}_chessboard.jpg'.format(file_name), image)

		        #cv.imshow('image', image)
		        #cv.waitKey(500)

	def Calibrate(self):
		ret, self.matrix, self.distortion_coefficients, self.rotation_vectors, self.translation_vectors = cv.calibrateCamera(self.object_points, 
																														     self.image_points, 
																														     gray.shape[::-1], None, None)   
	def Refine(self):
		# Refine the camera matrix
		self.refined_matrix, self.roi = cv.getOptimalNewCameraMatrix(self.matrix, self.distortion_coefficients, (self.width, self.height), 1, (self.width, self.height))

	def Undistort(self, load_path, save_path):
		image = cv.imread(load_path)
		result_image = cv.undistort(image, self.matrix, self.distortion_coefficients, None, self.refined_matrix)

		# Crop the image and save
		x, y, w, h = self.roi
		result_image = result_image[y:y + h, x:x + w]
		cv.imwrite(save_path, result_image)