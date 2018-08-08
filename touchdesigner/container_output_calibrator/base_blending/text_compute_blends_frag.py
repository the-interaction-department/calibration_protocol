layout (location = 0) out vec4 o_color;

uniform int u_solve_for;
uniform float u_gamma;

void main()
{
    float brightness_a = max(0.0, texture(sTD2DInputs[0], vUV.st).r);
    float brightness_b = max(0.0, texture(sTD2DInputs[1], vUV.st).r);
    float total = 0.0;

    if(brightness_a > 0.0)
    {
		total = brightness_a + brightness_b;
    }
    else
    {
    	total = brightness_a;
    }

    float pct = brightness_a / total;
    pct = pow(pct, u_gamma);

    vec4 color = vec4(vec3(pct), 1.0);
    o_color = TDOutputSwizzle(color);
}

