//
//  Shader.fsh
//  RGB to YUV conversion
//
//  Created by David Stanfill on 3/11/12.
//  Copyright 2011 Napkin Studio. All rights reserved.
//

varying vec2 textureVarying;
uniform sampler2D s_texture;
const mat3 matrix = mat3(
0.255785156250000,   0.502160156250000,   0.097523437500000,
-0.147644000000000,  -0.289856000000000,   0.437500000000000,
0.437500000000000,  -0.366352000000000,  -0.071148000000000
);
const vec3 bias = vec3(0.062500000000000, 0.500000000000000, 0.500000000000000);
void main()
{
    vec3 tex = texture2D(s_texture, textureVarying).rgb;
    vec3 yuv = tex*matrix + bias;
    //float y =  0.257*tex.r + 0.504*tex.g + 0.098*tex.b + 0.0625;
    //float u = -0.148*tex.r - 0.291*tex.g + 0.439*tex.b + 0.5;
    //float v =  0.439*tex.r - 0.368*tex.g - 0.071*tex.b + 0.5;
    //gl_FragColor = vec4(yuv.zv,yuv.y,yuv.x,1);
    gl_FragColor = vec4(yuv.z,yuv.y,yuv.x,1);
    //gl_FragColor = vec4(0.5,0.5,0.5,0.5);
    //gl_FragColor = vec4(0.5,0.5,0.5,1);
}
