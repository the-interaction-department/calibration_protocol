class Refinement:

	def __init__(self):
		self.original = op('table_smoothed')
		self.smoothed = op('table_smoothed')
		self.rows = op('../grid_template').par.rows
		self.cols = op('../grid_template').par.cols
		self.thresh = parent().par.Smoothingthreshold
		self.Reset()

	def Reset(self):
		self.smoothed.text = op('sopto_original').text

	def Smooth(self):
		print('Smoothing...')
		for row_index in range(1, self.smoothed.numRows):
			grid_row = (row_index - 1) // self.cols
			grid_col = (row_index - 1) % self.cols

			# First, make sure this is an interior cell
			if grid_col > 0 and grid_col < (self.cols - 1) and grid_row > 0 and grid_row < (self.rows - 1):

					curr_u = float(self.original[row_index, 'uv(0)'].val)
					curr_v = float(self.original[row_index, 'uv(1)'].val)

					if curr_u > 0.0 and curr_v > 0.0:

						l_index = row_index - 1
						r_index = row_index + 1
						t_index = row_index + self.cols
						b_index = row_index - self.cols
						
						# Check l-r neighbors
						l_u = float(self.original[l_index, 'uv(0)'].val)
						r_u = float(self.original[r_index, 'uv(0)'].val)

						# Are the u-coordinates of each neighbor valid?
						if l_u > 0.0 and r_u > 0.0:
							if abs(curr_u - l_u) > self.thresh or abs(curr_u - r_u) > self.thresh:
								print('u-coordinate at row {} was invalid - deleting'.format(row_index))
								self.smoothed[row_index, 'uv(0)'] = -1.0


						# Check t-b neighbors
						t_v = float(self.original[t_index, 'uv(1)'].val)
						b_v = float(self.original[b_index, 'uv(1)'].val)

						# Are the u-coordinates of each neighbor valid?
						if t_v > 0.0 and b_v > 0.0:
							if abs(curr_v - t_v) > self.thresh or abs(curr_v - b_v) > self.thresh:
								print('v-coordinate at row {} was invalid - deleting'.format(row_index))
								self.smoothed[row_index, 'uv(1)'] = -1.0

	def lerp(self, v0, v1, t):
  		return v0 + t * (v1 - v0)

	def Fill(self):
		"""Attempts to fill holes in the grid mesh"""
		for row_index in range(1, self.smoothed.numRows):
			grid_row = (row_index - 1) // self.cols
			grid_col = (row_index - 1) % self.cols

			# First, make sure this is an interior cell
			if grid_col > 0 and grid_col < (self.cols - 1) and grid_row > 0 and grid_row < (self.rows - 1):

					curr_u = float(self.original[row_index, 'uv(0)'].val)
					curr_v = float(self.original[row_index, 'uv(1)'].val)

					# Fill horizontal
					if curr_u < 0.0:
						l_index = row_index - 1
						r_index = row_index + 1
						
						# Check l-r neighbors
						l_u = float(self.original[l_index, 'uv(0)'].val)
						r_u = float(self.original[r_index, 'uv(0)'].val)

						if l_u > 0.0 and r_u > 0.0:
							# Both neighbors are valid - simply interpolate between the two
							self.smoothed[row_index, 'uv(0)'] = (l_u + r_u) / 2.0

						elif l_u > 0.0 and r_u < 0.0:
							# Move rightwards until a non-zero u-coordinate is encountered
							next_index = r_index
							next_u = float(self.original[next_index, 'uv(0)'].val)
							count = 1

							while next_u < 0.0:
								next_index = next_index + 1
								next_grid_col = next_index % self.cols

								# Don't extend past the right col
								if next_grid_col > self.cols:
									break

								next_u = float(self.original[next_index, 'uv(0)'].val)
								count += 1

							self.smoothed[row_index, 'uv(0)'] = self.lerp(l_u, next_u, 1.0 / count)

						elif l_u < 0.0 and r_u > 0.0:
							# Move leftwards until a non-zero u-coordinate is encountered
							next_index = r_index
							next_u = float(self.original[next_index, 'uv(0)'].val)
							count = 1

							while next_u < 0.0:
								next_index = next_index - 1
								next_grid_col = next_index % self.cols

								# Don't extend past the right col
								if next_grid_col < 0:
									break

								next_u = float(self.original[next_index, 'uv(0)'].val)
								count += 1

							self.smoothed[row_index, 'uv(0)'] = self.lerp(r_u, next_u, 1.0 / count)

					# Fill vertical
					if curr_v < 0.0:
						t_index = row_index + self.cols
						b_index = row_index - self.cols

						# Check t-b neighbors
						t_v = float(self.original[t_index, 'uv(1)'].val)
						b_v = float(self.original[b_index, 'uv(1)'].val)

						if t_v > 0.0 and b_v > 0.0:
							# Both neighbors are valid - simply interpolate between the two
							self.smoothed[row_index, 'uv(1)'] = (t_v + b_v) / 2.0

						elif t_v > 0.0 and b_v < 0.0:
							# Move downwards until a non-zero v-coordinate is encountered
							next_index = b_index
							next_v = float(self.original[next_index, 'uv(1)'].val)
							count = 1

							while next_v < 0.0:
								next_index = next_index - self.cols
								next_grid_row = next_index // self.cols

								# Don't extend past the bottom row
								if next_grid_row < 0:
									break

								next_v = float(self.original[next_index, 'uv(1)'].val)
								count += 1

							self.smoothed[row_index, 'uv(1)'] = self.lerp(t_v, next_v, 1.0 / count)

						elif t_v < 0.0 and b_v > 0.0:
							# Move upwards until a non-zero v-coordinate is encountered
							next_index = t_index
							next_v = float(self.original[next_index, 'uv(1)'].val)
							count = 1

							while next_v < 0.0:
								next_index = next_index + self.cols
								next_grid_row = next_index // self.cols

								# Don't extend past the top row
								if next_grid_row > self.rows:
									break

								next_v = float(self.original[next_index, 'uv(1)'].val)
								count += 1

							self.smoothed[row_index, 'uv(1)'] = self.lerp(b_v, next_v, 1.0 / count)