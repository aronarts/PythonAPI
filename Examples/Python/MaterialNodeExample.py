import SimplygonSDK as SDK
import SimplygonUtils as Utils
import os
import sys

#####################################
#
#  System:    Simplygon
#  File:      MaterialNodeExample.py
#  Language:  Python
#  Date:      $Date: 2014-10-30 14:36:00 $
#  Version:   $Revision: 2.2 $
#
#  Copyright (c) 2009 Donya Labs AB. All rights reserved.
#
#  This is private property, and it is illegal to copy or distribute in
#  any form, without written authorization by the copyright owner(s).
#
#####################################
#
#	#Description# 
#
#  This example shows how to use the material node network.
#
#  The RunExample() function will load a geometry and create a new 
#	material. A material node network is created and added to the diffuse
#  channel of the new material.
#
#  The example will go through different usages of the material nodes.
#
#	Material Node usage example 1 
#	Export GLSL/HLSL shader code from a material with a material node 
#  network.
#
#  Material Node usage example 2 
#	Preview the model with the material node network.
#
#  Material Node usage example 3
#	Reduce the geometry and create a mapping image for it to be able to
#	perform material casting.
#
#####################################

exampleName = "MaterialNodeExample"
def main( ):
    
    Utils.InitExample()
    SDK.InitErrorhandling();
    Utils.MoveAsset("MaterialNodeExampleAssets","dirt.jpg")
    Utils.MoveAsset("MaterialNodeExampleAssets","grass.jpg")
    Utils.MoveAsset("MaterialNodeExampleAssets","rock.jpg")
    Utils.MoveAsset("MaterialNodeExampleAssets","island.obj")
    Utils.MoveAsset("MaterialNodeExampleAssets","ice.png")
    Utils.MoveAsset("MaterialNodeExampleAssets","icemask.png")
    Utils.MoveAsset("MaterialNodeExampleAssets","noise.png")
    Utils.MoveAsset("MaterialNodeExampleAssets","water.png")

    # Set global variable. Using Orthonormal method for calculating
    # tangentspace.
    Utils.GetSDK().SetGlobalSetting( "DefaultTBNType" , SDK.SG_TANGENTSPACEMETHOD_ORTHONORMAL );

    # Run the example code
    RunExample(Utils.GetAssetPath("MaterialNodeExampleAssets", "island.obj"));

    Utils.DeinitExample();


def clamp(value, maxVal, minVal):
    return max(min(value, maxVal), minVal)

# Takes the existing texture coordinates level and copies it into a new texture coordinates level
# the second UV level is multiplied to get a higher frequency ( for tiling textures )
def SetupTexcoordLevels( newGeom ):
    # Get the tex_coords
    tex_coords_0 = newGeom.GetTexCoords( 0 );

    if( newGeom.GetTexCoords( 1 ) == None ):
        newGeom.AddTexCoords( 1 );
        tex_coords_1 = newGeom.GetTexCoords( 1 ) ;

        # Copy texcoords in level 0 to texcoords level 1 but multiply them to change frequency
        for i in range(0, tex_coords_0.GetItemCount()):
            tex_coords_1.SetItem( i, tex_coords_0.GetItem( i ) * 4.0 ); 

# Compute vertex colors from the model that will be used to interpolate between textures
# and other nodes
def ComputeVertexColors( newGeom ):
    print("Computing vertex colors")

    threshold_water = 0.01; # At what height the water should end
    threshold_grass = 0.3; # At what height the grass should end
    threshold_dirt = 0.5; # At what height the dirt should end

    coords = newGeom.GetCoords();
    vertex_ids = newGeom.GetVertexIds();

    max_height = -sys.float_info.max;
    min_height = sys.float_info.max;
    #Find the max and min y-value of the geometry
    for i in range(0, coords.GetTupleCount()):
        current_height = coords.GetItem( i * 3 + 1 );

        if( current_height > max_height ):
            max_height = current_height;

        if( current_height < min_height ):
            min_height = current_height;

    if( newGeom.GetColors( 0 ).IsNull()):
        newGeom.AddColors( 0 );

    relative_height_vertex_color = newGeom.GetColors( 0 );

    if( newGeom.GetColors( 1 ).IsNull()):
        newGeom.AddColors( 1 );

    weight_water_vertex_color = newGeom.GetColors( 1 );

    if( newGeom.GetColors( 2 ).IsNull()):
        newGeom.AddColors( 2 );

    weight_grass_vertex_color = newGeom.GetColors( 2 );

    if( newGeom.GetColors( 3 ).IsNull()):
        newGeom.AddColors( 3 );
                   
    weight_dirt_vertex_color = newGeom.GetColors( 3 );

    for corner_id in range(0, newGeom.GetTriangleCount() * 3):
        v_id = vertex_ids.GetItem( corner_id );

        # Get the y component from the coordinates
        absolute_height = coords.GetItem( v_id * 3 + 1 );

        # Compute the relative height where the lowest model coordinate will be zero, and the highest will be one
        relative_height = ( absolute_height - min_height ) / ( max_height - min_height );

        # Compute the blend values between textures
        # For instance, the interpolate_water_grass vertex colors will be:
        # [0 . 1] between [zero height . threshold_water height]
        # and then 1 for all heights above the threshold_water height
        interpolate_water_grass = clamp( relative_height / threshold_water , 0.0, 1.0 );
        interpolate_grass_dirt = clamp( ( relative_height - threshold_water ) / ( threshold_grass - threshold_water ), 0.0, 1.0 );
        interpolate_dirt_rock = clamp( ( relative_height - threshold_grass ) / ( threshold_dirt - threshold_grass ), 0.0, 1.0 );

        relative_height_color = [relative_height, relative_height, relative_height, 1.0];
        blend_water_color = [interpolate_water_grass, interpolate_water_grass, interpolate_water_grass, 1.0];
        blend_grass_color = [interpolate_grass_dirt, interpolate_grass_dirt, interpolate_grass_dirt, 1.0];
        blend_dirt_color = [interpolate_dirt_rock, interpolate_dirt_rock, interpolate_dirt_rock, 1.0];

        # Add the blend values to the vertex color fields
        relative_height_vertex_color.SetTuple( corner_id, relative_height_color );
        weight_water_vertex_color.SetTuple( corner_id, blend_water_color );
        weight_grass_vertex_color.SetTuple( corner_id, blend_grass_color );
        weight_dirt_vertex_color.SetTuple( corner_id, blend_dirt_color );


# This function will use a few nodes to create a network of nodes that will
# resemble a mountain material
def CreateMountainNode():
    # Begin by creating texture nodes, setting which UV sets they will use
    # and the paths to their respective textures
    sdk = Utils.GetSDK()
    node_texture_icemask = sdk.CreateShadingTextureNode();
    node_texture_ice = sdk.CreateShadingTextureNode();
    node_texture_rock = sdk.CreateShadingTextureNode();

    level_0 = "0";
    level_1 = "1";
    
    node_texture_icemask.SetTexCoordSet( level_0 );
    node_texture_ice.SetTexCoordSet( level_1 );
    node_texture_rock.SetTexCoordSet( level_1 );
    

    node_texture_icemask.SetTextureName( Utils.GetAssetPath("MaterialNodeExampleAssets", "icemask.png") );
    node_texture_ice.SetTextureName( Utils.GetAssetPath("MaterialNodeExampleAssets", "ice.png") );
    node_texture_rock.SetTextureName( Utils.GetAssetPath("MaterialNodeExampleAssets", "rock.jpg") );

    # Create a vertex color node that will link to the 0:th vertex color index
    node_weights_relative_height = sdk.CreateShadingVertexColorNode();
    node_weights_relative_height.SetVertexColorIndex( 0 );

    # Blend between ice and rock using the ice mask
    node_masked_ice = sdk.CreateShadingInterpolateNode();
    node_masked_ice.SetInput( 0, node_texture_rock );
    node_masked_ice.SetInput( 1, node_texture_ice );
    node_masked_ice.SetInput( 2, node_texture_icemask );

    # Offset all the weights of the height slightly using a subtraction
    node_icyness = sdk.CreateShadingSubtractNode();
    node_icyness.SetInput( 0, node_weights_relative_height );
    node_icyness.SetDefaultParameter( 1, 0.1, 0.1, 0.1, 0.0);

    # Clamp the weights to remain between zero and one after the subtraction
    node_icyness_clamp = sdk.CreateShadingClampNode();
    node_icyness_clamp.SetInput( 0, node_icyness );
    node_icyness_clamp.SetDefaultParameter( 1, 0.0, 0.0, 0.0, 1.0);
    node_icyness_clamp.SetDefaultParameter( 2, 1.0, 1.0, 1.0, 1.0);

    # Blend between the rock texture and the already masked ice
    # based on the height of the mountains
    node_interpolate_mountain = sdk.CreateShadingInterpolateNode();
    node_interpolate_mountain.SetInput( 0, node_texture_rock );
    node_interpolate_mountain.SetInput( 1, node_masked_ice );
    node_interpolate_mountain.SetInput( 2, node_icyness_clamp );

    return node_interpolate_mountain;

# This function will use a few nodes to create a network of nodes that will
# resemble a water material
def CreateWaterNode():
    # Begin by creating texture nodes, setting which UV sets they will use
    # and the paths to their respective textures
    sdk = Utils.GetSDK()
    node_texture_water = sdk.CreateShadingTextureNode();
    node_texture_noise = sdk.CreateShadingTextureNode();

    level_0 = "0";
    level_1 = "1";

    node_texture_water.SetTexCoordSet( level_1 );
    node_texture_noise.SetTexCoordSet( level_1 );

    node_texture_water.SetTextureName( Utils.GetAssetPath("MaterialNodeExampleAssets", "water.png") );
    node_texture_noise.SetTextureName( Utils.GetAssetPath("MaterialNodeExampleAssets", "noise.png") );

    # Create a color node which will simply be a static color
    node_color_water = sdk.CreateShadingColorNode();
    node_color_water.SetColor(0.075, 0.368, 0.347, 1.0);

    # Interpolate between the water texture and the water color
    # using the noise texture
    node_interpolate_water_color = sdk.CreateShadingInterpolateNode();
    node_interpolate_water_color.SetInput( 0, node_texture_water );
    node_interpolate_water_color.SetInput( 1, node_color_water );
    node_interpolate_water_color.SetInput( 2, node_texture_noise );

    return node_interpolate_water_color;

# Creates a material node network that uses different kinds of nodes
# to create a material for an island model
# It uses multiple textures with different uv sets
# and blends nodes using vertex colors and textures
def CreateIslandMaterialNodeNetwork():
    print("Creating shading network")
    # Create the mountain node
    node_mountain = CreateMountainNode();

    # Create the water node
    node_water = CreateWaterNode();

    sdk = Utils.GetSDK()

    # Define texture nodes, setting which UV sets they will use
    # and the paths to their respective textures
    node_texture_grass = sdk.CreateShadingTextureNode();
    node_texture_dirt = sdk.CreateShadingTextureNode();


    level_0 = "0";
    level_1 = "1";

    node_texture_dirt.SetTexCoordSet( level_1 );
    node_texture_grass.SetTexCoordSet( level_1 );

    node_texture_dirt.SetTextureName( "dirt.jpg" );
    node_texture_grass.SetTextureName( "grass.jpg" );

    # Create interpolation nodes 
    node_interpolate_water_land = sdk.CreateShadingInterpolateNode();
    node_interpolate_land_0 = sdk.CreateShadingInterpolateNode();
    node_interpolate_land_1 = sdk.CreateShadingInterpolateNode();

    node_weights_water_land = sdk.CreateShadingVertexColorNode();
    node_weights_water_land.SetVertexColorIndex( 1 );
    node_weights_interpolate_land_0 = sdk.CreateShadingVertexColorNode();
    node_weights_interpolate_land_0.SetVertexColorIndex( 2 );
    node_weights_interpolate_land_1 = sdk.CreateShadingVertexColorNode();
    node_weights_interpolate_land_1.SetVertexColorIndex( 3 );

    node_interpolate_land_1.SetInput( 0, node_texture_dirt );
    node_interpolate_land_1.SetInput( 1, node_mountain );
    node_interpolate_land_1.SetInput( 2, node_weights_interpolate_land_1 );

    node_interpolate_land_0.SetInput( 0, node_texture_grass );
    node_interpolate_land_0.SetInput( 1, node_interpolate_land_1 );
    node_interpolate_land_0.SetInput( 2, node_weights_interpolate_land_0 );

    node_interpolate_water_land.SetInput( 0, node_water );
    node_interpolate_water_land.SetInput( 1, node_interpolate_land_0 );
    node_interpolate_water_land.SetInput( 2, node_weights_water_land );

    return node_interpolate_water_land;


def RunExample( readFrom ):
    sdk = Utils.GetSDK()

    output_geometry_filename = Utils.GetOutputPath(exampleName, "materialnodeexample.obj");
    output_diffuse_filename = Utils.GetOutputPath(exampleName, "materialnodeexampl_diffuse.png");
    # Load object from file
    objReader = sdk.CreateWavefrontImporter();
    objReader.SetImportFilePath(readFrom);
    if( not objReader.RunImport() ):
        raise RuntimeError("Failed to import: "+readFrom)

    # Store geometries in collection
    collection = objReader.GetGeometries();

    # Set up scene
    scene = sdk.CreateScene();

    # For all objects in the collection
    h = collection.GetFirstItem();
    while h != None:
        newGeom = collection.GetGeometryData(h);

        # Compute a few sets of vertex colors based on the height of the model
        # the colors will be used to blend between textures
        ComputeVertexColors( newGeom );

        # Setup UV sets
        SetupTexcoordLevels( newGeom );

        # Create node and assign geometry
        newMesh = sdk.CreateSceneMesh();
        newMesh.SetGeometry(newGeom);

        # Add object to root
        scene.GetRootNode().AddChild(newMesh);
        h = collection.GetNextItem(h)

    material_table = scene.GetMaterialTable();

    island_material = sdk.CreateMaterial();
    material_table.AddMaterial( island_material );

    texture_table = scene.GetTextureTable();

    Texs = [
            Utils.GetAssetPath("MaterialNodeExampleAssets", "dirt.jpg"),
            Utils.GetAssetPath("MaterialNodeExampleAssets", "grass.jpg"),
            Utils.GetAssetPath("MaterialNodeExampleAssets", "water.png"),
            Utils.GetAssetPath("MaterialNodeExampleAssets", "noise.png"),
            Utils.GetAssetPath("MaterialNodeExampleAssets", "icemask.png"),
            Utils.GetAssetPath("MaterialNodeExampleAssets", "ice.png"),
            Utils.GetAssetPath("MaterialNodeExampleAssets", "rock.jpg")
            ];

    for i in range(0,len(Texs)):
        texture = sdk.CreateTexture();
        texture.SetName( Texs[i] );
        texture.SetFilePath( Texs[i] );
        texture_table.AddTexture(texture);

    # Create a material node network consisting of an arbitrary amount of shading nodes
    exit_node = CreateIslandMaterialNodeNetwork();

    # Assign the exit node of the material node network to the diffuse channel in the island material
    island_material.SetShadingNetwork( SDK.cvar.SG_MATERIAL_CHANNEL_DIFFUSE, exit_node );
    
    # Try saving the scene to file, and reload it
    #island_material.PrintInfo();

    scene.SaveToFile(Utils.GetOutputPath(exampleName, "testscene.scene"));

    # delete and reload
    scene = sdk.CreateScene();
    scene.LoadFromFile(Utils.GetOutputPath(exampleName, "testscene.scene"));

    #island_material.PrintInfo();


    #scene.SaveToFile("testscene.scene");

    #################
    # Material Node usage example 1 
    # 
    # Export GLSL/HLSL shader code from a material with a material node 
    # network
    #
    # Once the material has node networks assigned to it,
    # we can generate a shader for it both in GLSL and HLSL.
    #

    # We create a shader data object
    island_shader = sdk.CreateShaderData();

    # We add the material to it
    island_shader.SetMaterial( island_material );

    # We tell the shader data object to traverse the material node tree 
    # and gather the information needed to create a shader from the nodes 
    island_shader.GenerateShaderData();

    # Once the GenerateShaderData() has been called, the shader data object
    # will contain the information needed to setup the renderer for the 
    # GLSL or HLSL shader

    # Get all the texture paths that should be loaded and sent to the shader
    # the textures should be uploaded to the shader at the texture slot 
    # corresponding to its position in the collection
    texture_paths_collection = island_shader.GetShaderInputTexturePaths();

    # Get the UV sets that should be uploaded to the shader
    # the slot in the array corresponds to the slot in the shader
    # the values in the array corresponds to the tex coord level being used
    UV_set_collection = island_shader.GetShaderInputUVSets();

    # Get the vertex colors that should be uploaded to the shader
    # the slot in the array corresponds to the slot in the shader
    # the values in the array corresponds to the vertex color field being used
    vertex_color_collection = island_shader.GetShaderInputVertexColors();

    # Get the entire shader code for HLSL and GLSL
    hlsl_code = island_shader.GetHLSLCode();
    glsl_vertex_code = island_shader.GetGLSLVertexCode();
    glsl_fragment_code = island_shader.GetGLSLFragmentCode();

    #Store the shaders to file in the current folder 
    file_hlsl = open( Utils.GetOutputPath(exampleName, "shader_hlsl.txt"), "wt" );
    file_hlsl.write( hlsl_code.GetText() );
    file_hlsl.close();
    file_glsl_vertex = open( Utils.GetOutputPath(exampleName, "shader_glsl_vertex.txt"), "wt" );
    file_glsl_vertex.write(glsl_vertex_code.GetText() );
    file_glsl_vertex.close();
    file_glsl_fragment = open( Utils.GetOutputPath(exampleName, "shader_glsl_fragment.txt"), "wt" );
    file_glsl_fragment.write(glsl_fragment_code.GetText() );
    file_glsl_fragment.close();

    #
    # End material node usage example 1
    #################

    #################
    # Material Node usage example 2 
    # 
    # Preview the model with the material node network 
    #
    # This example will render the model using DirectX 
    # A shader will be generated like above (but automatically)
    # And the renderer will automatically upload the textures, uv sets and
    # vertex colors channels to a shader at the proper slots.
    # 
    # Then we will render the model with the shader and store the frames
    # to file.
    #

    # Create a DirectX renderer
    #renderer = sdk.CreateDirectXRenderer();

    # Setup the previewer with the window dimensions
    #renderer.CreatePreviewer( 2048, 2048 );

    # Will take the first ( and in this case ONLY ) geometry in the scene
    # and load it into the renderer
    #for i in range(0, scene.GetRootNode().GetChildCount()):
    #    mesh = scene.GetRootNode().GetChild( i ) ;
    #    if( mesh.GetClass() != "ISceneMesh" ):
    #        continue;

    #   sceneMesh = mesh.AsSceneMesh()
    #   geom = sceneMesh.GetGeometry();

        # Send the geometry and the material table into the renderer
        # Make sure the material table has materials that have a material 
        # node network attached to it
    #    renderer.LoadGeometryDataWithMaterialShadingNetwork( geom, scene.GetMaterialTable() );
    #    break;

    # Create a camera path for the renderer
    cam_path = sdk.CreateCameraPath();

    # Create a spinning camera path, at radius 0.8 with 32 cameras
    cam_path.CreateSpinningCameraPath( 0.8, 32 );

    # Render the model with the material node network and store the frames
    #renderer.RenderAlongCameraPathAndStorePics( cam_path, "screenshot", "png" );

    #
    # End material node usage example 1
    #################

    #################
    # Material Node usage example 3
    # 
    # Reduce the geometry and create a mapping image for it to be able to 
    # perform material casting.
    # 
    # Cast the diffuse channel from the material node network to the new 
    # material.
    #

    # Reducer
    red = sdk.CreateReductionProcessor();
    red.SetSceneRoot(scene.GetRootNode());

    # Set the Repair Settings.
    repair_settings = red.GetRepairSettings();

    # Will take care of holes that are of size 0.2 or less, so small gaps etc are removed.
    repair_settings.SetWeldDist( 0.2 );
    repair_settings.SetTjuncDist( 0.2 );

    # Set the Reduction Settings.
    reduction_settings = red.GetReductionSettings();

    # Set the reduction ratios to 0.9, meaning that we keep 90% of the triangles
    reduction_settings.SetReductionRatio(0.9);

    # Set the Mapping Image Settings.
    mapping_settings = red.GetMappingImageSettings();
    # Without this we cannot fetch data from the original geometry
    mapping_settings.SetGenerateMappingImage( True );
    # Set to generate new texture coordinates.
    mapping_settings.SetGenerateTexCoords( True );
    # The higher the number, the fewer texture-borders.
    mapping_settings.SetMaxStretch( 0.1 );
    # Buffer space for when texture is mip-mapped, so color values dont blend over.
    mapping_settings.SetGutterSpace( 4 );

    # Set the new material texture dimensions
    mapping_settings.SetAutomaticTextureSize( False );
    mapping_settings.SetWidth( 2048 );
    mapping_settings.SetHeight( 2048 );
    mapping_settings.SetMultisamplingLevel( 2 );

    # Run the reduction
    print("Reducing geometry")
    red.RunProcessing();

    # Mapping image is needed for texture casting.
    mapping_image = red.GetMappingImage();

    # Create new material table.
    output_materials = sdk.CreateMaterialTable();

    #Create new material for the table.
    output_material = sdk.CreateMaterial();
    output_material.SetName( "output_material" );

    #Add the new material to the table
    output_materials.AddMaterial( output_material );

    # Cast the diffuse texture data using a color caster
    cast = sdk.CreateColorCaster();
    cast.SetColorType( SDK.cvar.SG_MATERIAL_CHANNEL_DIFFUSE ); #Select the diffuse channel from the original material 

    cast.SetSourceMaterials( scene.GetMaterialTable() );
    cast.SetSourceTextures( scene.GetTextureTable() );
    cast.SetMappingImage( mapping_image ); # The mapping image we got from the reduction process.
    cast.SetOutputChannels( 3 ); # RGB, 3 channels! (1 would be for grey scale, and 4 would be for RGBA.)
    cast.SetOutputChannelBitDepth( 8 ); # 8 bits per channel. So in this case we will have 24bit colors RGB.
    cast.SetDilation( 10 ); # To avoid mip-map artifacts, the empty pixels on the map needs to be filled to a degree as well.
    cast.SetOutputFilePath( output_diffuse_filename ); # Where the texture map will be saved to file.
    print("Right now this example crashes in CastMaterials")
    cast.CastMaterials(); # Fetch! ERROR: It gets stuck somewhere in this operation right now.

    # Set the material properties 
    # Set the diffuse multiplier for the texture. 1 means it will not differ from original texture
    output_material.SetColor(SDK.cvar.SG_MATERIAL_CHANNEL_DIFFUSE, 1.0, 1.0, 1.0, 1.0 );

    # Set material to point to the created texture filename.
    output_material.SetTexture( SDK.cvar.SG_MATERIAL_CHANNEL_DIFFUSE , output_diffuse_filename );
    objexp = sdk.CreateWavefrontExporter();

    objexp.SetExportFilePath( output_geometry_filename );
    objexp.SetGeometries(collection);
    objexp.SetMaterials( output_materials );
    objexp.RunExport();

    #
    # End material node usage example 1
    #################

main()
