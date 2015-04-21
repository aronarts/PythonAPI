using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using SimplygonSDKCLR;
using System.Runtime.InteropServices;

namespace GeometryExample
{
    class GeometryExample
    {
        static void Main(string[] args)
        {
            String licensePath = @"C:\Users\David\AppData\Local\DonyaLabs\SimplygonSDK\Simplygon_5_license.dat";
            if (!File.Exists(licensePath))
            {
                Console.WriteLine("License file not found");
            }
            string licenseString = File.ReadAllText(licensePath);
            SimplygonSDK.AddSearchPath(@"c:\Program Files\SimplygonSDK");
            int res = SimplygonSDK.Initialize(null, licenseString);
            if (res != 0)
            {
                Console.WriteLine("Simplygon inititialization failed with error: " + res);
                return;
            }
            ISimplygonSDK sdk = SimplygonSDK.GetSDK();
            Console.WriteLine("Simplygon version: " + sdk.GetVersion());
            RunHighQualityReduction(sdk, @"c:\temp\out");
        }
        public static T SimplygonCast<T>(object from, bool cMemoryOwn)
        {
            System.Reflection.MethodInfo CPtrGetter = from.GetType().GetMethod("getCPtr", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static);
            return CPtrGetter == null ? default(T) : (T)System.Activator.CreateInstance
            (
                typeof(T),
                System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance,
                null,
                new object[] { ((HandleRef)CPtrGetter.Invoke(null, new object[] { from })).Handle, cMemoryOwn },
                null
            );
        }

        private static void RunHighQualityReduction(ISimplygonSDK SDK, string writeTo)
        {
    
            const int vertex_count = 12;
	        const int triangle_count = 4;
	        const int corner_count = triangle_count * 3;

        	// 4 triangles x 3 indices ( or 3 corners )
	        int[] corner_ids = { 0, 1, 2,
													 3, 4, 5,
													 6, 7, 8,
													 9, 10, 11 };

	        // 12 vertices with values for the x, y and z coordinates.
	        float[] vertex_coordinates  = {   0.0f,  0.0f,  0.0f,
													    1.0f,  0.0f,  0.0f,
													    1.0f,  1.0f,  0.0f,

													    1.0f,  1.0f,  0.0f,
													    0.0f,  1.0f,  0.0f,
													    0.0f,  0.0f,  0.0f,

														1.0f,  0.0f,  0.0f,
													    2.0f,  0.0f,  0.0f,
													    2.0f,  1.0f,  0.0f,
		
														2.0f,  1.0f,  0.0f,
													    1.0f,  1.0f,  0.0f,
													    1.0f,  0.0f,  0.0f  };

            spGeometryData g = SDK.CreateGeometryData();
            spRealArray coords = g.GetCoords();
            spRidArray ids = g.GetVertexIds();
            g.SetVertexCount(vertex_count);
            g.SetTriangleCount(triangle_count);
            for (int i = 0; i < vertex_count; ++i)
            {
                //coords.SetTuple(i, vertex_coordinates[i * 3]);
                //coords[i] = vertex_coordinates[i * 3];
                float[] v = {0.0f, 0.0f, 0.0f};
                for(int j = 0; j < 3; ++j) {
                    v[j] = vertex_coordinates[i*3 + j];
                }
                
                coords.SetTuple(i, v);
            }
            for (int i = 0; i < corner_ids.Length; ++i)
            {
                ids.SetItem(i, corner_ids[i]);
            }

            // Create the reduction-processor, and set which scene to reduce
            using (var reductionProcessor = SDK.CreateReductionProcessor())
            {
                spScene scene = SDK.CreateScene();
                spSceneNode root = scene.GetRootNode();
                spSceneMesh meshNode = SDK.CreateSceneMesh();
                meshNode.SetGeometry(g);
                //auto meshTransform = meshNode->GetRelativeTransform();
                //meshTransform->SetToTranslationTransform(100, 0, 0);
                root.AddChild(meshNode);
                reductionProcessor.SetSceneRoot(root);


                ///////////////////////////////////////////////////////////////////////////////////////////////
                // SETTINGS - Most of these are set to the same value by default, but are set anyway for clarity

                // The reduction settings object contains settings pertaining to the actual decimation
                var reductionSettings = reductionProcessor.GetReductionSettings();
                reductionSettings.SetKeepSymmetry(true); //Try, when possible to reduce symmetrically
                reductionSettings.SetUseAutomaticSymmetryDetection(true); //Auto-detect the symmetry plane, if one exists. Can, if required, be set manually instead.
                reductionSettings.SetUseHighQualityNormalCalculation(true); //Drastically increases the quality of the LODs normals, at the cost of extra processing time.
                reductionSettings.SetReductionHeuristics((uint)ReductionHeuristics.SG_REDUCTIONHEURISTICS_CONSISTENT); //Choose between "fast" and "consistent" processing. Fast will look as good, but may cause inconsistent 
                //triangle counts when comparing MaxDeviation targets to the corresponding percentage targets.

                // The reducer uses importance weights for all features to decide where and how to reduce.
                // These are advanced settings and should only be changed if you have some specific reduction requirement
                //reductionSettings.SetShadingImportance(2.f); //This would make the shading twice as important to the reducer as the other features./

                // The actual reduction triangle target are controlled by these settings
                reductionSettings.SetStopCondition((uint)StopCondition.SG_STOPCONDITION_EITHER_IS_REACHED);//The reduction stops when any of the targets below is reached
                reductionSettings.SetReductionRatio(0.5f); //Targets at 50% of the original triangle count
                reductionSettings.SetMaxDeviation(float.MaxValue); //Targets when an error of the specified size has been reached. As set here it never happens.

                // The repair settings object contains settings to fix the geometries
                var repairSettings = reductionProcessor.GetRepairSettings();
                repairSettings.SetTjuncDist(0.0f); //Removes t-junctions with distance 0.0f
                repairSettings.SetWeldDist(0.0f); //Welds overlapping vertices

                // The normal calculation settings deal with the normal-specific reduction settings
                var normalSettings = reductionProcessor.GetNormalCalculationSettings();
                normalSettings.SetReplaceNormals(false); //If true, this will turn off normal handling in the reducer and recalculate them all afterwards instead.
                //If false, the reducer will try to preserve the original normals as well as possible
                //normalSettings.SetHardEdgeAngle( 60.f ); //If the normals are recalculated, this sets the hard-edge angle./

                //END SETTINGS 
                ///////////////////////////////////////////////////////////////////////////////////////////////

                // Run the actual processing. After this, the set geometry will have been reduced according to the settings
                reductionProcessor.RunProcessing();

                // For this reduction, the LOD will use the same material set as the original, and hence no further processing is required

                //Create an .obj exporter to save our result
                using (var objExporter = SDK.CreateWavefrontExporter())
                {

                    // Generate the output filenames
                    string outputGeomFilename = writeTo + ".obj";
                    ISceneMesh topmesh = SimplygonCast<ISceneMesh>(scene.GetRootNode().GetChild(0), false);
		            

                    // Do the actual exporting
                    objExporter.SetExportFilePath(outputGeomFilename);
                    objExporter.SetSingleGeometry(topmesh.GetGeometry()); //This is the geometry we set as the processing geom of the reducer, retaining the materials in the original scene
                    objExporter.RunExport();

                    //Done! LOD created.
                }
            }
        }

    }
    
}
