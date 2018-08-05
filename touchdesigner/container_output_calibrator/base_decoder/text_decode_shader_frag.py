// The bit-depth of the gray code sequence (i.e. 4 bits) in each direction
uniform ivec2 u_bits;

// The number of bits to use (`u_bits - u_bits_to_use` bits will be ignored)
uniform int u_bits_to_use;

// The width and height of the projector
uniform vec2 u_projector_resolution;

// The threshold at which a pixel will be considered "on" versus "off" (usually around ~0.5)
uniform float u_threshold = 0.5;

layout(location = 0) out vec4 o_color;

// Reconstructs the gray code for the current pixel (MSB to LSB)
//
// Parameters:
// `number_of_bits`: the number of bits used in a particular orientation
// `offset`: an integer slice offset into the texture 3D containing captures
uint decode(int number_of_bits, int offset, inout bool valid)
{
	uint gray = 0;
	int valid_patterns = u_bits_to_use * 2;
	
	for (int i = 0; i < number_of_bits; i += 2)
	{
		int array_slice = offset + i;
		float pixel_org = texture(sTD2DArrayInputs[0], vec3(vUV.st, array_slice + 0)).r;
		float pixel_inv = texture(sTD2DArrayInputs[0], vec3(vUV.st, array_slice + 1)).r;

		float diff = pixel_org - pixel_inv;

		if (i < valid_patterns)
		{
			if (diff > u_threshold) 
			{
				gray ^= 1;
			}
			// else if (diff < -u_threshold)
			// {
			// 	// Do nothing...	
			// }
			// else 
			// {
			// 	valid = false;
			// 	break;
			// }
		}


		// Shift
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
	int patterns_x = u_bits.x * 2;
	int patterns_y = u_bits.y * 2; 

	// Get the value as calculated from the patterns and convert to decimal
	bool valid_x = true;
	uint gray_value_x = decode(patterns_x, 0, valid_x);
	bool valid_y = true;
	uint gray_value_y = decode(patterns_y, patterns_x, valid_y);

	uint val_x = gray_to_binary(gray_value_x);
	uint val_y = gray_to_binary(gray_value_y);

	// Scale color from [0..1] then scale to native projector resolution
	color = vec4(val_x, val_y, 0.0, 1.0);

	if (!valid_x || !valid_y)
	{
		color = vec4(-1.0, -1.0, -1.0, 1.0);
	}

	o_color = color;
}