uniform vec2 u_total_bits;
uniform int u_bits_to_use;
uniform vec2 u_projector_res;
uniform float u_threshold = 0.5;
out vec4 o_color;

// Reconstructs the gray code for the current pixel (MSB to LSB)
//
// Parameters:
// `number_of_bits`: the number of bits used along the current axis
// `offset`: an integer slice offset into the texture 3D containing captures
uint get_gray(int number_of_bits, int offset)
{
	uint gray = 0;
	int valid_patterns = u_bits_to_use * 2;
	
	for (int i = 0; i < number_of_bits; i += 2)
	{
		int array_slice = offset + i;
		float pixel_org = texture(sTD2DArrayInputs[0], vec3(vUV.st, array_slice)).r;
		float pixel_inv = texture(sTD2DArrayInputs[0], vec3(vUV.st, array_slice + 1)).r;

		float diff = pixel_org - pixel_inv;

		if (diff > u_threshold && i < valid_patterns) 
		{
			gray ^= 1;
		}
	
		// TODO: Implement inverses
		// else if (pixel > -threshold)
		// {
		// 	pixel is REJECTED: set it to -1.0
		// }

		if (i < number_of_bits - 2) 
		{
			gray <<= 1;
		}
	} 

	return gray;
}

uint gray_to_binary(uint num)
{
    uint mask = num;
    while (mask != 0)
    {
        mask >>= 1;
        num ^= mask;
    }
    return num;
}

void main()
{
	vec4 color = vec4(-1.0);

	// The number of patterns per axis times 2 (for the inverse)
	// TODO: When would the x and y differ? If you have an extremely non-uniform aspect ratio
	int patterns_x = int(u_total_bits) * 2;
	int patterns_y = int(u_total_bits) * 2; 

	// Get the value as calculated from the patterns and convert to binary
	uint gray_value_x = get_gray(patterns_x, 0);
	uint gray_value_y = get_gray(patterns_y, patterns_x);
	uint val_x = gray_to_binary(gray_value_x);
	uint val_y = gray_to_binary(gray_value_y);

	// Scale color from 0->1 then scale to native projector resolution
	color = vec4(val_x, val_y, 0.0, 1.0);
	color.xy /= max(u_projector_res.x, u_projector_res.y);
	color.xy *= u_projector_res;

	o_color = color;
}