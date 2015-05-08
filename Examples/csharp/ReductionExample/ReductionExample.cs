using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Example;
using SimplygonSDKCLR;

namespace ReductionExample
{
    class ReductionExample
    {
        static void Main(string[] args)
        {
            ISimplygonSDK sdk = Example.Example.InitExample();
            if (sdk == null)
            {
                return;
            }
            string userProfileDirectory = System.Environment.GetEnvironmentVariable("USERPROFILE");
            string assetRoot = userProfileDirectory + @"/Documents/SimplygonSDK/SourceCode/Assets/";
            string tempRoot = @"../../../../../temp/";
            Console.WriteLine("Running HQ Reduction");
            RunHighQualityReduction(sdk, assetRoot + "SimplygonMan.obj", tempRoot + "SimplygonMan_HQ_LOD");
            Console.WriteLine("Running Material Reduction");
            RunReductionWithTextureCasting(sdk, assetRoot + "SimplygonMan.obj", "SimplygonMan_Rebaked_Materials_LOD");
            Console.WriteLine("Running Cascaded LOD Reduction");
            RunCascadedLodChainReduction(sdk, assetRoot + "SimplygonMan.obj", "SimplygonMan_Cascade_LOD1", "SimplygonMan_Cascade_LOD2", "SimplygonMan_Cascade_LOD3");
        }
        static void RunHighQualityReduction(ISimplygonSDK sdk, string readFrom, string writeTo)
        {
            spWavefrontImporter objReader = sdk.CreateWavefrontImporter();
            objReader.SetExtractGroups(false); //This makes the .obj reader import into a single geometry object instead of multiple
            objReader.SetImportFilePath(readFrom);
            if (!objReader.RunImport())
            {
                Console.WriteLine("Failed to read: " + readFrom);
                return;
            }
            spGeometryData originalGeom = objReader.GetFirstGeometry(); //Only contains a single geom, so "first" is fine
            spMaterialTable originalMaterials = objReader.GetMaterials();

            //Create a copy of the original geometry on which we will run the reduction
            spGeometryData lodGeom = originalGeom.NewCopy(true);

            // Create the reduction-processor, and set the geometry to reduce
            spReductionProcessor reductionProcessor = sdk.CreateReductionProcessor();
            reductionProcessor.SetGeometry(lodGeom);

            ///////////////////////////////////////////////////////////////////////////////////////////////
            // SETTINGS - Most of these are set to the same value by default, but are set anyway for clarity

            // The reduction settings object contains settings pertaining to the actual decimation
            spReductionSettings reductionSettings = reductionProcessor.GetReductionSettings();
            reductionSettings.SetEnablePreprocessing(true); //This enables the pre-processing block, which contains welding and t-junction removal
            reductionSettings.SetEnablePostprocessing(true); //This enables the post-processing block, which contains normal recalculation and mapping image generation
            reductionSettings.SetKeepSymmetry(true); //Try, when possible to reduce symmetrically
            reductionSettings.SetUseAutomaticSymmetryDetection(true); //Auto-detect the symmetry plane, if one exists. Can, if required, be set manually instead.
            reductionSettings.SetUseHighQualityNormalCalculation(true); //Drastically increases the quality of the LODs normals, at the cost of extra processing time.
            reductionSettings.SetReductionHeuristics((uint)ReductionHeuristics.SG_REDUCTIONHEURISTICS_CONSISTENT); //Choose between "fast" and "consistent" processing. Fast will look as good, but may cause inconsistent 
            //triangle counts when comparing MaxDeviation targets to the corresponding percentage targets.

            // The reducer uses a feature flags mask to tell it what kind of borders to respect during reduction.
            FeatureFlags featureFlagsMask = 0;
            featureFlagsMask |= FeatureFlags.SG_FEATUREFLAGS_GROUP; //Respect borders between group ids
            featureFlagsMask |= FeatureFlags.SG_FEATUREFLAGS_MATERIAL; //Respect borders between material ids
            featureFlagsMask |= FeatureFlags.SG_FEATUREFLAGS_TEXTURE0; //Respect discontinuities in the first texcoord field
            featureFlagsMask |= FeatureFlags.SG_FEATUREFLAGS_SHADING; //Respect hard shading borders
            reductionSettings.SetFeatureFlags((uint)featureFlagsMask);

            // The reducer uses importance weights for all features to decide where and how to reduce.
            // These are advanced settings and should only be changed if you have some specific reduction requirement
            /*reductionSettings.SetShadingImportance(2.f); //This would make the shading twice as important to the reducer as the other features.*/

            // The actual reduction triangle target are controlled by these three settings
            reductionSettings.SetStopCondition((uint)StopCondition.SG_STOPCONDITION_EITHER_IS_REACHED); //The reduction stops when either of the targets is reached
            reductionSettings.SetReductionRatio(0.5f); //Stops at 50% of the original triangle count
            reductionSettings.SetMaxDeviation(SimplygonSDK.REAL_MAX); //Stops when an error of the specified size has been reached. As set here it never happens.
            //This condition corresponds to the on-screen size target presented in the Simplygon GUI, with a simple formula to convert between the two.

            // The repair settings object contains settings for the pre-processing block
            spRepairSettings repairSettings = reductionProcessor.GetRepairSettings();
            repairSettings.SetTjuncDist(0.0f); //Removes t-junctions with distance 0.0f
            repairSettings.SetWeldDist(0.0f); //Welds overlapping vertices

            // The normal calculation settings deal with the normal-specific reduction settings
            spNormalCalculationSettings normalSettings = reductionProcessor.GetNormalCalculationSettings();
            normalSettings.SetReplaceNormals(false); //If true, this will turn off normal handling in the reducer and recalculate them all afterwards instead.
            //If false, the reducer will try to preserve the original normals as well as possible
            /*normalSettings.SetHardEdgeAngle( 60.f ); //If the normals are recalculated, this sets the hard-edge angle.*/

            //END SETTINGS 
            ///////////////////////////////////////////////////////////////////////////////////////////////


            // Run the actual processing. After this, the set geometry will have been reduced according to the settings
            reductionProcessor.RunProcessing();

            //Create an .obj exporter to save our result
            spWavefrontExporter objExporter = sdk.CreateWavefrontExporter();

            // Do the actual exporting
            objExporter.SetExportFilePath(writeTo + ".obj");
            objExporter.SetSingleGeometry(lodGeom); //This is the geometry we set as the processing geom of the reducer
            objExporter.SetMaterials(originalMaterials); //Same material set as input
            if (!objExporter.RunExport())
            {
                Console.WriteLine("Failed to write target file");
            }

            //Done! LOD created.

        }

        static void RunReductionWithTextureCasting(ISimplygonSDK sdk, string readFrom, string writeTo)
        {
            // Load input geometry from file
            spWavefrontImporter objReader = sdk.CreateWavefrontImporter();
            objReader.SetExtractGroups(false); //This makes the .obj reader import into a single geometry object instead of multiple
            objReader.SetImportFilePath(readFrom);
            if (!objReader.RunImport())
            {
                Console.WriteLine("Failed to read: " + readFrom);
                return;
            }

            // Get geometry and materials from importer
            spGeometryData originalGeom = objReader.GetFirstGeometry(); //Only contains a single geom, so "first" is fine
            spMaterialTable originalMaterialTable = objReader.GetMaterials();

            // Create a copy of the original geometry on which we will run the reduction
            spGeometryData lodGeometry = originalGeom.NewCopy(true);

            // Create the reduction-processor, and set the geometry to reduce
            spReductionProcessor reductionProcessor = sdk.CreateReductionProcessor();
            reductionProcessor.SetGeometry(lodGeometry);


            ///////////////////////////////////////////////////////////////////////////////////////////////
            // SETTINGS - Most of these are set to the same value by default, but are set anyway for clarity

            // The reduction settings object contains settings pertaining to the actual decimation
            spReductionSettings reductionSettings = reductionProcessor.GetReductionSettings();
            reductionSettings.SetReductionHeuristics((uint)ReductionHeuristics.SG_REDUCTIONHEURISTICS_FAST); //Choose between "fast" and "consistent" processing.

            // The actual reduction triangle target are controlled by these three settings
            reductionSettings.SetStopCondition((uint)StopCondition.SG_STOPCONDITION_EITHER_IS_REACHED); //The reduction stops when either of the targets is reached
            reductionSettings.SetReductionRatio(0.5f); //Stops at 50% of the original triangle count
            reductionSettings.SetMaxDeviation(SimplygonSDK.REAL_MAX); //Stops when an error of the specified size has been reached. As set here it never happens.

            // The normal calculation settings deal with the normal-specific reduction settings
            spNormalCalculationSettings normalSettings = reductionProcessor.GetNormalCalculationSettings();
            normalSettings.SetReplaceNormals(true); //If true, this will turn off normal handling in the reducer and recalculate them all afterwards instead.
            normalSettings.SetHardEdgeAngle(70.0f); //If the normals are recalculated, this sets the hard-edge angle.

            // The Image Mapping Settings, specifically needed for the texture baking we are doing later
            spMappingImageSettings mappingSettings = reductionProcessor.GetMappingImageSettings();
            mappingSettings.SetGenerateMappingImage(true); //Without this we cannot fetch data from the original geometry, and thus not generate diffuse and normal-maps later on.
            mappingSettings.SetGenerateTexCoords(true);//Set to generate new texture coordinates.
            mappingSettings.SetMaxStretch(0.4f); //The higher the number, the fewer texture-borders.
            mappingSettings.SetGutterSpace(2); //Buffer space for when texture is mip-mapped, so color values don't blend over. Greatly influences packing efficiency
            mappingSettings.SetTexCoordLevel(0); //Sets the output texcoord level. For this asset, this will overwrite the original coords
            mappingSettings.SetWidth(1024);
            mappingSettings.SetHeight(1024);
            mappingSettings.SetMultisamplingLevel(2);

            //END SETTINGS 
            ///////////////////////////////////////////////////////////////////////////////////////////////


            // Run the actual processing. After this, the set geometry will have been reduced according to the settings
            reductionProcessor.RunProcessing();


            ///////////////////////////////////////////////////////////////////////////////////////////////
            // CASTING

            // Now, we need to retrieve the generated mapping image and use it to cast the old materials into a new one, for each channel.
            spMappingImage mappingImage = reductionProcessor.GetMappingImage();

            // Now, for each channel, we want to cast the 9 input materials into a single output material, with one texture per channel. 
            // First, create a new material table.
            spMaterialTable lodMaterialTable = sdk.CreateMaterialTable();
            // Create new material for the table.
            spMaterial lodMaterial = sdk.CreateMaterial();
            lodMaterial.SetName("SimplygonBakedMaterial");
            lodMaterialTable.AddMaterial(lodMaterial);
            // Cast diffuse and specular texture data with a color caster
            {
                // Set the material properties 
                lodMaterial.SetColor(SimplygonSDK.SG_MATERIAL_CHANNEL_AMBIENT, 0, 0, 0, 0);
                lodMaterial.SetColor(SimplygonSDK.SG_MATERIAL_CHANNEL_DIFFUSE, 1, 1, 1, 1);
                lodMaterial.SetColor(SimplygonSDK.SG_MATERIAL_CHANNEL_SPECULAR, 1, 1, 1, 128);
                //Note the 128 on the specular channels alpha. Simplygon bakes shininess
                //to the alpha channel of the specular map if the caster is set to 4 channel
                //output, and it is scaled between 0 and 1 internally. To get the correct
                //scale on the output, it should be multiplied by 128.

                // Cast the data using a color caster
                spColorCaster colorCaster = sdk.CreateColorCaster();
                colorCaster.SetSourceMaterials(originalMaterialTable);
                colorCaster.SetDestMaterial(lodMaterial); //This modulates the cast color with the base colors set for the dest material above.
                //It means the internal shininess is multiplied by 128 before baking to texture.
                colorCaster.SetMappingImage(mappingImage); //The mapping image we got from the reduction process.
                colorCaster.SetOutputChannelBitDepth(8); //8 bits per channel. So in this case we will have 24bit colors RGB.
                colorCaster.SetDilation(10); //To avoid mip-map artifacts, the empty pixels on the map needs to be filled to a degree as well.

                colorCaster.SetColorType(SimplygonSDK.SG_MATERIAL_CHANNEL_DIFFUSE);
                colorCaster.SetOutputChannels(3); //RGB, 3 channels! (1 would be for grey scale, and 4 would be for RGBA.)
                colorCaster.SetOutputFilePath("combinedDiffuseMap.png"); //Where the texture map will be saved to file.
                colorCaster.CastMaterials(); //Do the actual casting and write to texture.

                colorCaster.SetColorType(SimplygonSDK.SG_MATERIAL_CHANNEL_SPECULAR);
                colorCaster.SetOutputChannels(4); //RGBA, 4 channels! Stores spec power in A
                colorCaster.SetOutputFilePath("combinedSpecularMap.png"); //Where the texture map will be saved to file.
                colorCaster.CastMaterials(); //Do the actual casting and write to texture.


                lodMaterial.SetTexture(SimplygonSDK.SG_MATERIAL_CHANNEL_DIFFUSE, "combinedDiffuseMap.png"); //Set material to point to the texture we cast to above
                lodMaterial.SetTexture(SimplygonSDK.SG_MATERIAL_CHANNEL_SPECULAR, "combinedSpecularMap.png"); //Set material to point to the texture we cast to above
            }

            // Cast normal map texture data with the normal caster. This also compensates for any geometric errors that have appeared in the reduction process.
            {
                // cast the data using a normal caster
                spNormalCaster normalCaster = sdk.CreateNormalCaster();
                normalCaster.SetSourceMaterials(originalMaterialTable);
                normalCaster.SetMappingImage(mappingImage);
                normalCaster.SetOutputChannels(3); // RGB, 3 channels! (But really the x, y and z values for the normal)
                normalCaster.SetOutputChannelBitDepth(8);
                normalCaster.SetDilation(10);
                normalCaster.SetOutputFilePath("combinedNormalMap.png");
                normalCaster.SetFlipBackfacingNormals(false);
                normalCaster.SetGenerateTangentSpaceNormals(true);
                normalCaster.CastMaterials();

                // Set normal map of the created material to point to the combined normal map
                lodMaterial.SetTexture(SimplygonSDK.SG_MATERIAL_CHANNEL_NORMALS, "combinedNormalMap.png");
            }

            // END CASTING
            ///////////////////////////////////////////////////////////////////////////////////////////////

            //Create an .obj exporter to save our result
            spWavefrontExporter objExporter = sdk.CreateWavefrontExporter();

            // Generate the output filenames
            // Do the actual exporting
            objExporter.SetExportFilePath(writeTo + ".obj");
            objExporter.SetSingleGeometry(lodGeometry); //This is the geometry we set as the processing geom of the reducer
            objExporter.SetMaterials(lodMaterialTable); //Our new cast material
            if (!objExporter.RunExport())
            {
                Console.WriteLine("Failed to write target file");
            }

            //Done! LOD and material created.

        }
        static void RunCascadedLodChainReduction(ISimplygonSDK sdk, string readFrom, string writeToLod1, string writeToLod2, string writeToLod3)
        {
            // Load input geometry from file
            spWavefrontImporter objReader = sdk.CreateWavefrontImporter();
            objReader.SetExtractGroups(false); //This makes the .obj reader import into a single geometry object instead of multiple
            objReader.SetImportFilePath(readFrom);
            if (!objReader.RunImport())
                return;

            // Get geometry and materials from importer
            spGeometryData originalGeometry = objReader.GetFirstGeometry(); //Only contains a single geom, so "first" is fine
            spMaterialTable originalMaterialTable = objReader.GetMaterials();

            //Create a copy of the original geometry on which we will run the reduction
            spGeometryData lodGeometry = originalGeometry.NewCopy(true);

            // Create the reduction-processor, and set the geometry to reduce
            spReductionProcessor reductionProcessor = sdk.CreateReductionProcessor();
            reductionProcessor.SetGeometry(lodGeometry);


            ///////////////////////////////////////////////////////////////////////////////////////////////
            // SETTINGS 

            // The reduction settings object contains settings pertaining to the actual decimation
            spReductionSettings reductionSettings = reductionProcessor.GetReductionSettings();
            reductionSettings.SetReductionHeuristics((uint)ReductionHeuristics.SG_REDUCTIONHEURISTICS_FAST); //Choose between "fast" and "consistent" processing.

            // The normal calculation settings deal with the normal-specific reduction settings
            spNormalCalculationSettings normalSettings = reductionProcessor.GetNormalCalculationSettings();
            normalSettings.SetReplaceNormals(true); //If true, this will turn off normal handling in the reducer and recalculate them all afterwards instead.
            normalSettings.SetHardEdgeAngle(70.0f); //If the normals are recalculated, this sets the hard-edge angle.

            // The actual reduction triangle target are controlled by these three settings
            reductionSettings.SetStopCondition((uint)StopCondition.SG_STOPCONDITION_EITHER_IS_REACHED); //The reduction stops when either of the targets is reached
            reductionSettings.SetReductionRatio(0.0f); //Never stop at a triangle percentage, will hit MaxDeviation instead.


            //END SETTINGS 
            ///////////////////////////////////////////////////////////////////////////////////////////////

            //Create an .obj exporter to save our result
            spWavefrontExporter objExporter = sdk.CreateWavefrontExporter();
            objExporter.SetSingleGeometry(lodGeometry); //This is the geometry we set as the processing geom of the reducer
            objExporter.SetMaterials(originalMaterialTable); //Same materials as original

            //Set reduction targets using on-screen size to set the maximum deviation
            originalGeometry.CalculateExtents(true); //This calculates the bounds of the geometry
            float[] geometryInf = new float[3];
            float[] geometrySup = new float[3];
            originalGeometry.GetInf(geometryInf);
            originalGeometry.GetSup(geometrySup);
            float geometryDiagonalLength = (float)Math.Sqrt((double)((geometrySup[0] - geometryInf[0]) * (geometrySup[0] - geometryInf[0]) +
                (geometrySup[1] - geometryInf[1]) * (geometrySup[1] - geometryInf[1]) +
                (geometrySup[2] - geometryInf[2]) * (geometrySup[2] - geometryInf[2])));
            float[] maxDeviationTargets = new float[3]; //To find an approximate MaxDeviation for a pixelsize on screen, we just divide the diagonal by our wanted pixelsize
            maxDeviationTargets[0] = geometryDiagonalLength / 500.0f; //Gives a deviation of max 1 pixel at ~500 pixels on-screen
            maxDeviationTargets[1] = geometryDiagonalLength / 100.0f; //Gives a deviation of max 1 pixel at ~100 pixels on-screen
            maxDeviationTargets[2] = geometryDiagonalLength / 50.0f; //Gives a deviation of max 1 pixel at ~50 pixels on-screen

            //Generate the output filenames
            string[] outputGeomFilename = new string[3];
            outputGeomFilename[0] = writeToLod1 + ".obj";
            outputGeomFilename[1] = writeToLod2 + ".obj";
            outputGeomFilename[2] = writeToLod3 + ".obj";

            // Run the iterative processing, saving the output geometry after every process
            for (int reductionIteration = 0; reductionIteration < 3; ++reductionIteration)
            {
                // The geometry still uses the same pointer, so it does not need to be re-set for the exporter or reducer after each pass.
                reductionSettings.SetMaxDeviation(maxDeviationTargets[reductionIteration]); //Stops when an error of the specified size has been reached. 
                reductionProcessor.RunProcessing();

                // Do the exporting
                objExporter.SetMaterialFilePath(null); //Reset the material file path so it's set by ExportFilePath
                objExporter.SetExportFilePath(outputGeomFilename[reductionIteration]);
                if (!objExporter.RunExport())
                {
                    Console.WriteLine("Failed to write target file");
                }
            }

            //Done! 3 cascaded LODs created.

        }
    }
}
