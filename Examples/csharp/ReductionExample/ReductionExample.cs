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
            if(sdk == null)
            {
                return;
            }
            string assetRoot = @"../../../../../Assets/";
            string tempRoot = @"../../../../../temp/";
            Console.WriteLine("Running HQ Reduction");
            RunHighQualityReduction(sdk, assetRoot + "SimplygonMan.obj", tempRoot + "SimplygonMan_HQ_LOD");

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
	        reductionProcessor.SetGeometry( lodGeom );

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
	        uint featureFlagsMask = 0;
	        featureFlagsMask |= (uint)FeatureFlags.SG_FEATUREFLAGS_GROUP; //Respect borders between group ids
            featureFlagsMask |= (uint)FeatureFlags.SG_FEATUREFLAGS_MATERIAL; //Respect borders between material ids
            featureFlagsMask |= (uint)FeatureFlags.SG_FEATUREFLAGS_TEXTURE0; //Respect discontinuities in the first texcoord field
            featureFlagsMask |= (uint)FeatureFlags.SG_FEATUREFLAGS_SHADING; //Respect hard shading borders
	        reductionSettings.SetFeatureFlags( featureFlagsMask );

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
	        objExporter.SetExportFilePath( writeTo + ".obj");
	        objExporter.SetSingleGeometry( lodGeom ); //This is the geometry we set as the processing geom of the reducer
	        objExporter.SetMaterials( originalMaterials ); //Same material set as input
            if (!objExporter.RunExport())
            {
                Console.WriteLine("Failed to write target file");
            }

	        //Done! LOD created.

        }

  
        //static void RunReductionWithTextureCasting(string readFrom, string writeTo);
        //static void RunCascadedLodChainReduction(string readFrom, string writeToLod1, string writeToLod2, string writeToLod3);
    }
}
