class Raytracer:

	def __init__(self):
		width = parent.Calibrator.par.Cameraresolution1
		height = parent.Calibrator.par.Cameraresolution2

		self.projection_matrix = op.Scene.op('cam_default').projection(width, height)
		self.camera_matrix = op.Scene.op('cam_default').worldTransform
		self.pick_vals = op.Scene.op('constant_pick_vals')

		# mapu mapv
		self.pick_result = op.Scene.op('null_model_uvs')
		self.renderpick = op.Scene.op('renderpick')

		self.p2c = op('null_p2c')
		self.p2m = op('table_p2m')
		

		self.points = op('sopto_model_points')
		self.prims = op('sopto_model_prims')

	def Trace(self):
		self.p2m.clear()

		pixels = self.p2c.numpyArray()

		for ppx in range(self.p2c.width):
			for ppy in range(self.p2c.height):
				# Camera pixel coordinates are already normalized
				cpx, cpy, _, _ = pixels[ppy, ppx]

				if not cpx and not cpy:
					self.p2m.appendRow([ppx, ppy, -1.0, -1.0])
				else:
					# Set camera uv coordinates in render pick DAT
					self.pick_vals.par.value1 = cpx
					self.pick_vals.par.value2 = cpy

					# Grab results
					model_u = self.pick_result[1, 'mapu']
					model_v = self.pick_result[1, 'mapv']

					self.p2m.appendRow([ppx, ppy, model_u, model_v])
