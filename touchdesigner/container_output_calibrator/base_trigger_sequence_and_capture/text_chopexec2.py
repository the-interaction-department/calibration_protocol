def onValueChange(channel, sampleIndex, val, prev):
	# Output the patterns and capture the first image with pattern 0
	op.ProjectorOutputs.op('switch_projection_map').par.index = 0

	# Capture first image
	op('tex3d_captures').par.resetpulse.pulse()
	op('tex3d_captures').par.replaceindex = 0
	op('tex3d_captures').par.resetsinglepulse.pulse()
