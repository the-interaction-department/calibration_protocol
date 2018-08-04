// The bit-depth of the gray code sequence (i.e. 4 bits)
uniform int u_bits;

// The absolute index of the current pattern, accounting for orientation and inversion
uniform int u_absolute_index;

// The total number of patterns per orientation (horizontal / vertical)
uniform int u_images_per_orientation; 

// The current orientation (`true` if horizontal, `false` otherwise)
uniform bool u_orientation; 

layout(location = 0) out vec4 o_color;

// Converts a binary (decimal) number to gray code: see https://en.wikipedia.org/wiki/Gray_code
uint binary_to_gray(uint num)
{
    return num ^ (num >> 1u);
}

void main()
{
    float axis = u_orientation ? vUV.s : vUV.t;
    
    // Because we are showing each pattern AND its inverse we divide the index by 2
    int relative_index = u_images_per_orientation - u_absolute_index;
    relative_index = int(floor((u_absolute_index + 2) / 2.0));

    // The total number of possible unique gray codes 
    // for the given bit-depth
    int possible_unique = int(pow(2.0, u_bits));

    // Divide the space into a number of tiles equal to the
    // total number of patterns that will be used
    float scaled = float(possible_unique) * axis; 
    float sequence_index = floor(scaled);

    // Convert the tile coords to the corresponding grey code 
    uint num = uint(sequence_index);
    uint gray = binary_to_gray(num);

    // Is the bit at position `u_absolute_index` on or off for 
    // the gray code corresponding to tile `ipos`?
    uint on_or_off = gray;
    for (uint bit_position = 0; bit_position < (u_bits - relative_index); ++bit_position)
    {
        on_or_off >>= 1;
    }
    on_or_off &= 1;
    vec4 color = vec4(vec3(on_or_off), 1.0);

    // Invert odd patterns
    if (u_absolute_index % 2 != 0) 
    {
        color.rgb = 1.0 - color.rgb;
    }

    o_color = TDOutputSwizzle(color);
}
