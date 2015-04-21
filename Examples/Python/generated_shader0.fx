Texture2D map_0 : register( t0 );
Texture2D map_1 : register( t1 );
Texture2D map_2 : register( t2 );
Texture2D map_3 : register( t3 );
Texture2D map_4 : register( t4 );
Texture2D map_5 : register( t5 );
Texture2D map_6 : register( t6 );

SamplerState state_0 : register( s0 );
SamplerState state_1 : register( s1 );

cbuffer matrices : register( b0 )
{
matrix world_matrix;
matrix view_matrix;
matrix projection_matrix;
};

struct PerFragmentData
{
float2 tex_0;
float2 tex_1;
float4 vertexcolor_0;
float4 vertexcolor_1;
float4 vertexcolor_2;
float4 vertexcolor_3;
};

struct VS_Input
{
float4 position : POSITION;
float4 normal : NORMAL;
float4 tangent : TANGENT;
float4 bitangent : BINORMAL;

float2 tex_0 : TEXCOORD0;
float2 tex_1 : TEXCOORD1;
float4 vertexcolor_0 : COLOR0;
float4 vertexcolor_1 : COLOR1;
float4 vertexcolor_2 : COLOR2;
float4 vertexcolor_3 : COLOR3;
};

struct PS_Input
{
float4 position : SV_POSITION;
float4 normal : NORMAL;
float4 tangent : TANGENT;
float4 bitangent : BINORMAL;

float2 tex_0 : TEXCOORD0;
float2 tex_1 : TEXCOORD1;
float4 vertexcolor_0 : COLOR0;
float4 vertexcolor_1 : COLOR1;
float4 vertexcolor_2 : COLOR2;
float4 vertexcolor_3 : COLOR3;
};

float4 function_0_Diffuse_ShadingTextureNode( PerFragmentData fragdata )
{
float4 result = map_4.Sample( state_1, fragdata.tex_1  );
return result;
}

float4 function_1_Diffuse_ShadingColorNode( PerFragmentData fragdata )
{
float4 result = float4( 0.07500000, 0.36800000, 0.34700000, 1.00000000 );
return result;
}

float4 function_2_Diffuse_ShadingTextureNode( PerFragmentData fragdata )
{
float4 result = map_2.Sample( state_1, fragdata.tex_1  );
return result;
}

float4 function_3_Diffuse_ShadingInterpolateNode( PerFragmentData fragdata )
{
float4 rgba_interpolate_A = function_0_Diffuse_ShadingTextureNode( fragdata );
float4 rgba_interpolate_B = function_1_Diffuse_ShadingColorNode( fragdata );
float4 rgba_interpolate_C = function_2_Diffuse_ShadingTextureNode( fragdata );
float4 result = lerp( rgba_interpolate_A, rgba_interpolate_B, rgba_interpolate_C );
return result;
}

float4 function_4_Diffuse_ShadingTextureNode( PerFragmentData fragdata )
{
float4 result = map_6.Sample( state_1, fragdata.tex_1  );
return result;
}

float4 function_5_Diffuse_ShadingTextureNode( PerFragmentData fragdata )
{
float4 result = map_5.Sample( state_1, fragdata.tex_1  );
return result;
}

float4 function_6_Diffuse_ShadingTextureNode( PerFragmentData fragdata )
{
float4 result = map_3.Sample( state_1, fragdata.tex_1  );
return result;
}

float4 function_7_Diffuse_ShadingTextureNode( PerFragmentData fragdata )
{
float4 result = map_3.Sample( state_1, fragdata.tex_1  );
return result;
}

float4 function_8_Diffuse_ShadingTextureNode( PerFragmentData fragdata )
{
float4 result = map_0.Sample( state_1, fragdata.tex_1  );
return result;
}

float4 function_9_Diffuse_ShadingTextureNode( PerFragmentData fragdata )
{
float4 result = map_1.Sample( state_0, fragdata.tex_0  );
return result;
}

float4 function_10_Diffuse_ShadingInterpolateNode( PerFragmentData fragdata )
{
float4 rgba_interpolate_A = function_7_Diffuse_ShadingTextureNode( fragdata );
float4 rgba_interpolate_B = function_8_Diffuse_ShadingTextureNode( fragdata );
float4 rgba_interpolate_C = function_9_Diffuse_ShadingTextureNode( fragdata );
float4 result = lerp( rgba_interpolate_A, rgba_interpolate_B, rgba_interpolate_C );
return result;
}

float4 function_11_Diffuse_ShadingVertexColorNode( PerFragmentData fragdata )
{
float4 result = fragdata.vertexcolor_0;
return result;
}

float4 function_12_Diffuse_ShadingSubtractNode( PerFragmentData fragdata )
{
float4 rgba_subtract_A = function_11_Diffuse_ShadingVertexColorNode( fragdata );
float4 rgba_subtract_B = float4( 0.10000000, 0.10000000, 0.10000000, 0.00000000 );
float4 result = rgba_subtract_A - rgba_subtract_B;
return result;
}

float4 function_13_Diffuse_ShadingClampNode( PerFragmentData fragdata )
{
float4 rgba_clamp_A = function_12_Diffuse_ShadingSubtractNode( fragdata );
float4 rgba_clamp_B = float4( 0.00000000, 0.00000000, 0.00000000, 1.00000000 );
float4 rgba_clamp_C = float4( 1.00000000, 1.00000000, 1.00000000, 1.00000000 );
float4 result = clamp(rgba_clamp_A, rgba_clamp_B, rgba_clamp_C);
return result;
}

float4 function_14_Diffuse_ShadingInterpolateNode( PerFragmentData fragdata )
{
float4 rgba_interpolate_A = function_6_Diffuse_ShadingTextureNode( fragdata );
float4 rgba_interpolate_B = function_10_Diffuse_ShadingInterpolateNode( fragdata );
float4 rgba_interpolate_C = function_13_Diffuse_ShadingClampNode( fragdata );
float4 result = lerp( rgba_interpolate_A, rgba_interpolate_B, rgba_interpolate_C );
return result;
}

float4 function_15_Diffuse_ShadingVertexColorNode( PerFragmentData fragdata )
{
float4 result = fragdata.vertexcolor_3;
return result;
}

float4 function_16_Diffuse_ShadingInterpolateNode( PerFragmentData fragdata )
{
float4 rgba_interpolate_A = function_5_Diffuse_ShadingTextureNode( fragdata );
float4 rgba_interpolate_B = function_14_Diffuse_ShadingInterpolateNode( fragdata );
float4 rgba_interpolate_C = function_15_Diffuse_ShadingVertexColorNode( fragdata );
float4 result = lerp( rgba_interpolate_A, rgba_interpolate_B, rgba_interpolate_C );
return result;
}

float4 function_17_Diffuse_ShadingVertexColorNode( PerFragmentData fragdata )
{
float4 result = fragdata.vertexcolor_2;
return result;
}

float4 function_18_Diffuse_ShadingInterpolateNode( PerFragmentData fragdata )
{
float4 rgba_interpolate_A = function_4_Diffuse_ShadingTextureNode( fragdata );
float4 rgba_interpolate_B = function_16_Diffuse_ShadingInterpolateNode( fragdata );
float4 rgba_interpolate_C = function_17_Diffuse_ShadingVertexColorNode( fragdata );
float4 result = lerp( rgba_interpolate_A, rgba_interpolate_B, rgba_interpolate_C );
return result;
}

float4 function_19_Diffuse_ShadingVertexColorNode( PerFragmentData fragdata )
{
float4 result = fragdata.vertexcolor_1;
return result;
}

float4 Sample_Diffuse( PerFragmentData fragdata )
{
float4 rgba_interpolate_A = function_3_Diffuse_ShadingInterpolateNode( fragdata );
float4 rgba_interpolate_B = function_18_Diffuse_ShadingInterpolateNode( fragdata );
float4 rgba_interpolate_C = function_19_Diffuse_ShadingVertexColorNode( fragdata );
float4 result = lerp( rgba_interpolate_A, rgba_interpolate_B, rgba_interpolate_C );
return result;
}

PS_Input VS_Main( VS_Input vertex )
{
PS_Input vs_out = ( PS_Input )0;

float4x4 world_view =  mul(world_matrix, view_matrix);
float4x4 model_view_projection = mul(world_view, projection_matrix);
vs_out.position = mul( vertex.position, model_view_projection);

vs_out.tex_0 = vertex.tex_0;
vs_out.tex_1 = vertex.tex_1;

vs_out.vertexcolor_0 = vertex.vertexcolor_0;
vs_out.vertexcolor_1 = vertex.vertexcolor_1;
vs_out.vertexcolor_2 = vertex.vertexcolor_2;
vs_out.vertexcolor_3 = vertex.vertexcolor_3;

vs_out.normal = vertex.normal;
vs_out.normal.w = 0.0;
vs_out.normal = mul( vs_out.normal, world_view  ) ;
vs_out.normal = normalize(vs_out.normal);

vs_out.tangent = vertex.tangent;
vs_out.tangent.w = 0.0;
vs_out.tangent = mul( vs_out.tangent, world_view);
vs_out.tangent = normalize(vs_out.tangent);

vs_out.bitangent = vertex.bitangent;
vs_out.bitangent.w = 0.0;
vs_out.bitangent = mul( vs_out.bitangent, world_view);	
vs_out.bitangent = normalize(vs_out.bitangent);
return vs_out;
}

float4 PS_Main( PS_Input frag ) : SV_TARGET
{
PerFragmentData fragdata;
float3 lightdir = normalize(float3(1.0,1.0,-1.0));
fragdata.tex_0 = frag.tex_0;
fragdata.tex_1 = frag.tex_1;
fragdata.vertexcolor_0 = frag.vertexcolor_0;
fragdata.vertexcolor_1 = frag.vertexcolor_1;
fragdata.vertexcolor_2 = frag.vertexcolor_2;
fragdata.vertexcolor_3 = frag.vertexcolor_3;
float4 outcolor = float4(0.0, 0.0, 0.0, 1.0);
outcolor += Sample_Diffuse(fragdata) * saturate(dot(frag.normal.xyz, lightdir));

return outcolor;
}
