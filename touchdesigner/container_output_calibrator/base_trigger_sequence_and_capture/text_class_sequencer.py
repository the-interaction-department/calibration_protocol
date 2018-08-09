import cv2
import numpy as np

class Sequencer:

	def __init__(self):
		pass

	def Run(self):
		# Switch to all white
		if parent.Calibrator.par.Produceboundingmask:
			op.ProjectorOutputs.op('switch_projection_map').par.index = 1
			self.Calculate_bounds()

		# Switch to patterns
		op.ProjectorOutputs.op('switch_projection_map').par.index = 0
		op('lfo_start').par.resetpulse.pulse()

	def Calculate_bounds(self):
		load_path = '{}/../assets/temp/{}'.format(project.folder, 'white.jpg')
		save_path = '{}/../assets/temp/{}'.format(project.folder, 'bounding.jpg')
		op('switch_device').save(load_path)

		# Read image
		image = cv2.imread(load_path)
		image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		ret, thresh = cv2.threshold(image_gray, 127, 255, 0)
		image_result, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		# Find the contour with the largest area
		largest_contour = max(contours, key = cv2.contourArea)
		x, y, w, h = cv2.boundingRect(largest_contour)

		# Draw the contour
		blank_image = np.zeros((parent.Calibrator.par.Projectorresolution2, parent.Calibrator.par.Projectorresolution1, 3), np.uint8)
		cv2.rectangle(blank_image, (x, y), (x + w, y + h), (255, 255, 255), cv2.FILLED)
		cv2.imwrite(save_path, blank_image)