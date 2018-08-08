uniform vec2 u_grid_dims;

out vec4 o_color;

void main()
{
	const float divider = 1.0;

	// projector width and height
	float width = 100.0;
	float height = 50.0;
	float halfblock = 0.0;

	float pixelv, pixelh;

	if (gl_FragCoord.y < height / 2.0)
		pixelv = (gl_FragCoord.y - halfblock) / divider;
	else
		pixelv = (height - gl_FragCoord.y - halfblock) / divider;

	if (pixelv < 0.0)
		pixelv = 0.0;

	if (gl_FragCoord.x < width / 2.0)
		pixelh = (gl_FragCoord.x - halfblock) / divider;
	else
		pixelh = (width - gl_FragCoord.x - halfblock) / divider;

	if (pixelh < 0.0)
		pixelh = 0.0;

	vec4 color;

	if(pixelv < pixelh)
		color = vec4(vec3(pixelv), 1.0);
	else 
		color = vec4(vec3(pixelh), 1.0);

	o_color = TDOutputSwizzle(color);
}

