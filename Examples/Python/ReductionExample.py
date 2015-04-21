import SimplygonSDK as SDK
import SimplygonUtils as Utils
import os
import math
#
#  System:    Simplygon
#  File:      ReductionExample.py
#  Language:  C++
#  Date:      $Date: 2014-10-27 14:36:00 $
#  Version:   $Revision: 6.0 $
#
#  Copyright (c) 2014 Donya Labs AB. All rights reserved.
#
#  This is private property, and it is illegal to copy or distribute in
#  any form, without written authorization by the copyright owner(s).
#
#####################################
#
#	#Description# An extensive reduction example
#
#	In this example we demonstrate 3 common usages for the Simplygon reducer
#	and explain good starting settings for the different usages.
#
#	First, we do a high-quality reduction using symmetry awareness and 
#	high-quality normal handling to 50%, explaining most of the commonly 
#	used settings along the way
#
#	Secondly, the mesh is again reduced to 50% and the 9 input materials
#	of the original are cast into a single output material, retaining all 
#	channels from the original material
#
#	Thirdly, a cascaded reduction chain is run using faster settings
#	to show how to setup a cascaded LOD chain. These reductions use
#	MaxDeviation set by on-screen size approximation instead of a triangle %
#
#


def main():
    Utils.InitExample()
    SDK.InitErrorhandling();
    # Before any specific processing starts, set global variables. 
    # Using Orthonormal method for calculating tangentspace.
    Utils.GetSDK().SetGlobalSetting( "DefaultTBNType" , SDK.SG_TANGENTSPACEMETHOD_ORTHONORMAL );

    currentDir = os.path.dirname(os.path.realpath(__file__))+"/"
    # Run HQ reduction example, reducing a single geometry to a single LOD
    print("Running HQ reduction... ");
    
    RunHighQualityReduction(currentDir+"Assets/SimplygonMan.obj", currentDir+"Output/SimplygonMan_Rebaked_Materials_LOD" );
    print("Done.\n");
    # Run reduction example that bakes all input materials into a single output material
    print("Running reduction with material baking... ");
    RunReductionWithTextureCasting(currentDir, "Assets/SimplygonMan.obj", "Output/SimplygonMan_Rebaked_Materials_LOD" );
    print("Done.\n");

    # Run a cascaded LOD chain generation
    print("Running cascaded LOD chain reduction... ");
    RunCascadedLodChainReduction(currentDir, "Assets/SimplygonMan.obj", "Output/SimplygonMan_Cascade_LOD1", "Output/SimplygonMan_Cascade_LOD2", "Output/SimplygonMan_Cascade_LOD3" );
    print("Done.\n");

    # Done!
    print("\nAll LODs complete, shutting down...");
    Utils.DeinitExample();

def RunHighQualityReduction(readFrom, writeTo):
    # Load input geometry from file
    sdk = Utils.GetSDK()
    objReader = sdk.CreateWavefrontImporter();
    objReader.SetExtractGroups(False); #This makes the .obj reader import into a single geometry object instead of multiple
    objReader.SetImportFilePath(readFrom);
    if( not objReader.RunImport() ):
        return;

    # Get geometry and materials from importer
    originalGeom = objReader.GetFirstGeometry(); #Only contains a single geom, so "first" is fine
    originalMaterials = objReader.GetMaterials();

    #Create a copy of the original geometry on which we will run the reduction
    lodGeom = originalGeom.NewCopy(True);

    # Create the reduction-processor, and set the geometry to reduce
    reductionProcessor = sdk.CreateReductionProcessor();
    reductionProcessor.SetGeometry( lodGeom );

    ###############################################/
    # SETTINGS - Most of these are set to the same value by default, but are set anyway for clarity

    # The reduction settings object contains settings pertaining to the actual decimation
    reductionSettings = reductionProcessor.GetReductionSettings();
    reductionSettings.SetEnablePreprocessing(True); #This enables the pre-processing block, which contains welding and t-junction removal
    reductionSettings.SetEnablePostprocessing(True); #This enables the post-processing block, which contains normal recalculation and mapping image generation
    reductionSettings.SetKeepSymmetry(True); #Try, when possible to reduce symmetrically
    reductionSettings.SetUseAutomaticSymmetryDetection(True); #Auto-detect the symmetry plane, if one exists. Can, if required, be set manually instead.
    reductionSettings.SetUseHighQualityNormalCalculation(True); #Drastically increases the quality of the LODs normals, at the cost of extra processing time.
    reductionSettings.SetReductionHeuristics(SDK.SG_REDUCTIONHEURISTICS_CONSISTENT); #Choose between "fast" and "consistent" processing. Fast will look as good, but may cause inconsistent 
                                                                                                                                                              #triangle counts when comparing MaxDeviation targets to the corresponding percentage targets.

    # The reducer uses a feature flags mask to tell it what kind of borders to respect during reduction.
    featureFlagsMask = 0;
    featureFlagsMask |= SDK.SG_FEATUREFLAGS_GROUP; #Respect borders between group ids
    featureFlagsMask |= SDK.SG_FEATUREFLAGS_MATERIAL; #Respect borders between material ids
    featureFlagsMask |= SDK.SG_FEATUREFLAGS_TEXTURE0; #Respect discontinuities in the first texcoord field
    featureFlagsMask |= SDK.SG_FEATUREFLAGS_SHADING; #Respect hard shading borders
    reductionSettings.SetFeatureFlags( featureFlagsMask );

    # The reducer uses importance weights for all features to decide where and how to reduce.
    # These are advanced settings and should only be changed if you have some specific reduction requirement
    # reductionSettings->SetShadingImportance(2.f); #This would make the shading twice as important to the reducer as the other features.

    # The actual reduction triangle target are controlled by these three settings
    reductionSettings.SetStopCondition(SDK.SG_STOPCONDITION_EITHER_IS_REACHED); #The reduction stops when either of the targets is reached
    reductionSettings.SetReductionRatio(0.5); #Stops at 50% of the original triangle count
    reductionSettings.SetMaxDeviation(SDK.REAL_MAX); #Stops when an error of the specified size has been reached. As set here it never happens.
    #This condition corresponds to the on-screen size target presented in the Simplygon GUI, with a simple formula to convert between the two.

    # The repair settings object contains settings for the pre-processing block
    repairSettings = reductionProcessor.GetRepairSettings();
    repairSettings.SetTjuncDist(0.0); #Removes t-junctions with distance 0.0f
    repairSettings.SetWeldDist(0.0); #Welds overlapping vertices

    # The normal calculation settings deal with the normal-specific reduction settings
    normalSettings = reductionProcessor.GetNormalCalculationSettings();
    normalSettings.SetReplaceNormals(False); #If true, this will turn off normal handling in the reducer and recalculate them all afterwards instead.
                                                                                      #If false, the reducer will try to preserve the original normals as well as possible
    #normalSettings->SetHardEdgeAngle( 60.f ); #If the normals are recalculated, this sets the hard-edge angle.*/

    #END SETTINGS 
    ###############################################/


    # Run the actual processing. After this, the set geometry will have been reduced according to the settings
    reductionProcessor.RunProcessing();

    # For this reduction, the LOD will use the same material set as the original, and hence no further processing is required

    #Create an .obj exporter to save our result
    objExporter = sdk.CreateWavefrontExporter();


    # Do the actual exporting
    objExporter.SetExportFilePath( writeTo + ".obj");
    objExporter.SetSingleGeometry( lodGeom ); #This is the geometry we set as the processing geom of the reducer
    objExporter.SetMaterials( originalMaterials ); #Same material set as input
    objExporter.RunExport();

    #Done! LOD created.


def RunReductionWithTextureCasting(currentDir, readFrom, writeTo):
    # Load input geometry from file
    sdk = Utils.GetSDK()
    objReader = sdk.CreateWavefrontImporter();
    objReader.SetExtractGroups(False); #This makes the .obj reader import into a single geometry object instead of multiple
    objReader.SetImportFilePath(currentDir+readFrom);
    if( not objReader.RunImport() ):
        return;

    # Get geometry and materials from importer
    originalGeom = objReader.GetFirstGeometry(); #Only contains a single geom, so "first" is fine
    originalMaterialTable = objReader.GetMaterials();

    # Create a copy of the original geometry on which we will run the reduction
    lodGeometry = originalGeom.NewCopy(True);

    # Create the reduction-processor, and set the geometry to reduce
    reductionProcessor = sdk.CreateReductionProcessor();
    reductionProcessor.SetGeometry( lodGeometry);


    ###############################################/
    # SETTINGS - Most of these are set to the same value by default, but are set anyway for clarity

    # The reduction settings object contains settings pertaining to the actual decimation
    reductionSettings = reductionProcessor.GetReductionSettings();
    reductionSettings.SetReductionHeuristics(SDK.SG_REDUCTIONHEURISTICS_FAST); #Choose between "fast" and "consistent" processing.

    # The actual reduction triangle target are controlled by these three settings
    reductionSettings.SetStopCondition(SDK.SG_STOPCONDITION_EITHER_IS_REACHED); #The reduction stops when either of the targets is reached
    reductionSettings.SetReductionRatio(0.5); #Stops at 50% of the original triangle count
    reductionSettings.SetMaxDeviation(SDK.REAL_MAX); #Stops when an error of the specified size has been reached. As set here it never happens.

    # The normal calculation settings deal with the normal-specific reduction settings
    normalSettings = reductionProcessor.GetNormalCalculationSettings();
    normalSettings.SetReplaceNormals(True); #If true, this will turn off normal handling in the reducer and recalculate them all afterwards instead.
    normalSettings.SetHardEdgeAngle( 70 ); #If the normals are recalculated, this sets the hard-edge angle.

    # The Image Mapping Settings, specifically needed for the texture baking we are doing later
    mappingSettings = reductionProcessor.GetMappingImageSettings();
    mappingSettings.SetGenerateMappingImage( True ); #Without this we cannot fetch data from the original geometry, and thus not generate diffuse and normal-maps later on.
    mappingSettings.SetGenerateTexCoords( True );#Set to generate new texture coordinates.
    mappingSettings.SetMaxStretch( 0.2 ); #The higher the number, the fewer texture-borders.
    mappingSettings.SetGutterSpace( 1 ); #Buffer space for when texture is mip-mapped, so color values don't blend over. Greatly influences packing efficiency
    mappingSettings.SetTexCoordLevel(0); #Sets the output texcoord level. For this asset, this will overwrite the original coords
    mappingSettings.SetWidth( 1024 );
    mappingSettings.SetHeight( 1024 );
    mappingSettings.SetMultisamplingLevel( 2 );

    #END SETTINGS 
    ###############################################


    # Run the actual processing. After this, the set geometry will have been reduced according to the settings
    reductionProcessor.RunProcessing();


    ###############################################
    # CASTING

    # Now, we need to retrieve the generated mapping image and use it to cast the old materials into a new one, for each channel.
    mappingImage = reductionProcessor.GetMappingImage();

    # Now, for each channel, we want to cast the 9 input materials into a single output material, with one texture per channel. 
    # First, create a new material table.
    lodMaterialTable = sdk.CreateMaterialTable();
    # Create new material for the table.
    lodMaterial = sdk.CreateMaterial();
    lodMaterial.SetName( "SimplygonBakedMaterial" );
    lodMaterialTable.AddMaterial( lodMaterial );
    # Cast diffuse and specular texture data with a color caster
    # Set the material properties 
    lodMaterial.SetColor( SDK.cvar.SG_MATERIAL_CHANNEL_AMBIENT , 0 , 0 , 0 , 0 );
    lodMaterial.SetColor( SDK.cvar.SG_MATERIAL_CHANNEL_DIFFUSE , 1 , 1 , 1 , 1 );
    lodMaterial.SetColor( SDK.cvar.SG_MATERIAL_CHANNEL_SPECULAR , 1 , 1 , 1 , 128 );
    #Note the 128 on the specular channels alpha. Simplygon bakes shininess
    #to the alpha channel of the specular map if the caster is set to 4 channel
    #output, and it is scaled between 0 and 1 internally. To get the correct
    #scale on the output, it should be multiplied by 128.

    # Cast the data using a color caster
    colorCaster = sdk.CreateColorCaster();
    colorCaster.SetSourceMaterials( originalMaterialTable );
    colorCaster.SetDestMaterial( lodMaterial ); #This modulates the cast color with the base colors set for the dest material above.
                                                                                             #It means the internal shininess is multiplied by 128 before baking to texture.
    colorCaster.SetMappingImage( mappingImage ); #The mapping image we got from the reduction process.
    colorCaster.SetOutputChannelBitDepth( 8 ); #8 bits per channel. So in this case we will have 24bit colors RGB.
    colorCaster.SetDilation( 10 ); #To avoid mip-map artifacts, the empty pixels on the map needs to be filled to a degree as well.

    colorCaster.SetColorType( SDK.cvar.SG_MATERIAL_CHANNEL_DIFFUSE ); 
    colorCaster.SetOutputChannels( 3 ); #RGB, 3 channels! (1 would be for grey scale, and 4 would be for RGBA.)
    colorCaster.SetOutputFilePath( currentDir+"output/combinedDiffuseMap.png" ); #Where the texture map will be saved to file.
    colorCaster.CastMaterials(); #Do the actual casting and write to texture.

    colorCaster.SetColorType( SDK.cvar.SG_MATERIAL_CHANNEL_SPECULAR ); 
    colorCaster.SetOutputChannels( 4 ); #RGBA, 4 channels! Stores spec power in A
    colorCaster.SetOutputFilePath( currentDir+"output/combinedSpecularMap.png" ); #Where the texture map will be saved to file.
    colorCaster.CastMaterials(); #Do the actual casting and write to texture.


    lodMaterial.SetTexture( SDK.cvar.SG_MATERIAL_CHANNEL_DIFFUSE , currentDir+"output/combinedDiffuseMap.png" ); #Set material to point to the texture we cast to above
    lodMaterial.SetTexture( SDK.cvar.SG_MATERIAL_CHANNEL_SPECULAR , currentDir+"output/combinedSpecularMap.png" ); #Set material to point to the texture we cast to above
    

    # Cast normal map texture data with the normal caster. This also compensates for any geometric errors that have appeared in the reduction process.
    # cast the data using a normal caster
    normalCaster = sdk.CreateNormalCaster();
    normalCaster.SetSourceMaterials( originalMaterialTable );
    normalCaster.SetMappingImage( mappingImage );
    normalCaster.SetOutputChannels( 3 ); # RGB, 3 channels! (But really the x, y and z values for the normal)
    normalCaster.SetOutputChannelBitDepth( 8 ); 
    normalCaster.SetDilation( 10 );
    normalCaster.SetOutputFilePath( currentDir+"output/combinedNormalMap.png" );
    normalCaster.SetFlipBackfacingNormals( True );
    normalCaster.SetGenerateTangentSpaceNormals( True );
    normalCaster.CastMaterials();

    # Set normal map of the created material to point to the combined normal map
    lodMaterial.SetTexture( SDK.cvar.SG_MATERIAL_CHANNEL_NORMALS , currentDir+"output/combinedNormalMap.png" );

    # END CASTING
    ###############################################/


    # Set all material IDs to 0, since we now only use 1 material for the entire geometry.
    materialIdsArray = lodGeometry.GetMaterialIds();
    for i in range(0, lodGeometry.GetTriangleCount()):
        materialIdsArray.SetItem( i, 0 );

    #Create an .obj exporter to save our result
    objExporter = sdk.CreateWavefrontExporter();

    # Generate the output filenames
    objExporter.SetExportFilePath( writeTo + ".obj");
    objExporter.SetSingleGeometry( lodGeometry ); #This is the geometry we set as the processing geom of the reducer
    objExporter.SetMaterials( lodMaterialTable ); #Our new cast material
    objExporter.RunExport();

    #Done! LOD and material created.


def RunCascadedLodChainReduction(currentDir, readFrom, writeToLod1, writeToLod2, writeToLod3):
    # Load input geometry from file
    sdk = Utils.GetSDK()
    objReader = sdk.CreateWavefrontImporter();
    objReader.SetExtractGroups(False); #This makes the .obj reader import into a single geometry object instead of multiple
    objReader.SetImportFilePath(currentDir+readFrom);
    if( not objReader.RunImport() ):
        return;

    # Get geometry and materials from importer
    originalGeometry = objReader.GetFirstGeometry(); #Only contains a single geom, so "first" is fine
    originalMaterialTable = objReader.GetMaterials();

    #Create a copy of the original geometry on which we will run the reduction
    lodGeometry = originalGeometry.NewCopy(True);

    # Create the reduction-processor, and set the geometry to reduce
    reductionProcessor = sdk.CreateReductionProcessor();
    reductionProcessor.SetGeometry( lodGeometry );


    ###############################################/
    # SETTINGS 

    # The reduction settings object contains settings pertaining to the actual decimation
    reductionSettings = reductionProcessor.GetReductionSettings();
    reductionSettings.SetReductionHeuristics(SDK.SG_REDUCTIONHEURISTICS_FAST); #Choose between "fast" and "consistent" processing.

    # The normal calculation settings deal with the normal-specific reduction settings
    normalSettings = reductionProcessor.GetNormalCalculationSettings();
    normalSettings.SetReplaceNormals(True); #If true, this will turn off normal handling in the reducer and recalculate them all afterwards instead.
    normalSettings.SetHardEdgeAngle( 70 ); #If the normals are recalculated, this sets the hard-edge angle.

    # The actual reduction triangle target are controlled by these three settings
    reductionSettings.SetStopCondition(SDK.SG_STOPCONDITION_EITHER_IS_REACHED); #The reduction stops when either of the targets is reached
    reductionSettings.SetReductionRatio(0.0); #Never stop at a triangle percentage, will hit MaxDeviation instead.


    #END SETTINGS 
    ###############################################/

    #Create an .obj exporter to save our result
    objExporter = sdk.CreateWavefrontExporter();
    objExporter.SetSingleGeometry( lodGeometry ); #This is the geometry we set as the processing geom of the reducer
    objExporter.SetMaterials(originalMaterialTable); #Same materials as original

    #Set reduction targets using on-screen size to set the maximum deviation
    originalGeometry.CalculateExtents(True); #This calculates the bounds of the geometry
    geometryInf = originalGeometry.GetInf();
    geometrySup = originalGeometry.GetSup();
    geometryDiagonalLength = math.sqrt((geometrySup[0] - geometryInf[0]) * (geometrySup[0] - geometryInf[0]) + 
                                                                            (geometrySup[1] - geometryInf[1]) * (geometrySup[1] - geometryInf[1]) + 
                                                                            (geometrySup[2] - geometryInf[2]) * (geometrySup[2] - geometryInf[2]));
    #To find an approximate MaxDeviation for a pixelsize on screen, we just divide the diagonal by our wanted pixelsize
    maxDeviationTargets = [
        geometryDiagonalLength / 500, #Gives a deviation of max 1 pixel at ~500 pixels on-screen
        geometryDiagonalLength / 100, #Gives a deviation of max 1 pixel at ~100 pixels on-screen
        geometryDiagonalLength / 50] #Gives a deviation of max 1 pixel at ~50 pixels on-screen
    
    #Generate the output filenames
    outputGeomFilename = [currentDir+writeToLod1, currentDir+writeToLod2, currentDir+writeToLod3]

    # Run the iterative processing, saving the output geometry after every process
    for reductionIteration in range(0,3):
        # The geometry still uses the same pointer, so it does not need to be re-set for the exporter or reducer after each pass.
        reductionSettings.SetMaxDeviation(maxDeviationTargets[reductionIteration]); #Stops when an error of the specified size has been reached. 
        reductionProcessor.RunProcessing();

        # Do the exporting
        objExporter.SetMaterialFilePath(None); #Reset the material file path so it's set by ExportFilePath
        objExporter.SetExportFilePath( outputGeomFilename[reductionIteration] );
        objExporter.RunExport();

    #Done! 3 cascaded LODs created.

main()

