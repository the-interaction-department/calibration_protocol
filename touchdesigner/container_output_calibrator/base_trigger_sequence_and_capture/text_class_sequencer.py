import cv2
import numpy as np

class Sequencer:

	def __init__(self):
		self.load_path = '{}/../assets/temp/{}'.format(project.folder, 'white.jpg')
		self.save_path = '{}/../assets/temp/{}'.format(project.folder, 'bounding.jpg')
		self.mask_color = (255, 255, 255)
		self.dilation_iterations = 1

	def Run(self):
		# Switch to all white
		if parent.Calibrator.par.Produceboundingmask:
			op.ProjectorOutputs.op('switch_projection_map').par.index = 1
			self.Calculate_bounds()

		op.Decoder.op('base_mask_outliers/moviefilein_bounding').par.reloadpulse.pulse()

		# Switch to patterns
		op.ProjectorOutputs.op('switch_projection_map').par.index = 0
		op('lfo_start').par.resetpulse.pulse()

	def Calculate_bounds(self, draw_contour=True, blur=False):
		op('switch_device').save(self.load_path)

		# Read image
		image = cv2.imread(self.load_path)
		image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		ret, thresh = cv2.threshold(image_gray, 127, 255, 0)
		image_result, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		# Find the contour with the largest area
		largest_contour = max(contours, key=cv2.contourArea)
		x, y, w, h = cv2.boundingRect(largest_contour)

		# Draw the contour or bounding rectangle
		blank_image = np.zeros((parent.Calibrator.par.Projectorresolution2, parent.Calibrator.par.Projectorresolution1, 3), np.uint8)
		if draw_contour:
			cv2.drawContours(blank_image, [largest_contour], 0, self.mask_color, cv2.FILLED)
		else:
			cv2.rectangle(blank_image, (x, y), (x + w, y + h), self.mask_color, cv2.FILLED)

		kernel = np.ones((5, 5), np.uint8)
		blank_image = cv2.dilate(blank_image, kernel, iterations=self.dilation_iterations)
		
		# Optionally blur the mask
		if blur:
			blank_image = cv2.GaussianBlur(blank_image, (5, 5), 0)

		cv2.imwrite(self.save_path, blank_image)