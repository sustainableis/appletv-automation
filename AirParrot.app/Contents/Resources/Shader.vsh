//
//  Shader.vsh
//  Board Game
//
//  Created by Jonathan Gerlach on 3/25/11.
//  Copyright 2011 Napkin Studio. All rights reserved.
//

attribute vec4 position;
attribute vec2 texture_vertex;

//varying vec4 colorVarying;
varying vec2 textureVarying;

uniform float translate;

void main()
{
    gl_Position = position;
    //gl_Position.y += sin(translate) / 2.0;

	textureVarying = texture_vertex;
}
