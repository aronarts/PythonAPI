using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using SimplygonSDKCLR;
using Example;

namespace RemeshingExample
{
    class RemeshingExamples
    {
        static void Main(string[] args)
        {
            ISimplygonSDK sdk = Example.Example.InitExample();
            if (sdk == null)
            {
                return;
            }
            sdk.SetGlobalSetting("DefaultTBNType", (int)TangentSpaceMethod.SG_TANGENTSPACEMETHOD_ORTHONORMAL);
            RunExample(sdk);

        }
        // Total number of LOD pairs to create
        const int num_lods = 2;

        // On-screen size of the LODs
        static readonly uint[] lod_sizes = {
	        300,
	        150
	        };

        // On-screen merge distances
        static readonly uint[] merge_distances = {
	        0,
	        8
	        };

        static bool run_remeshing_for_lod(ISimplygonSDK sdk, int lod_index, uint merge_distance)
        {
            string assetRoot = @"../../../../../Assets/";
            string tempRoot = @"../../../../../temp/";
            string output_filename = string.Format(tempRoot + "wall_lod{0}_merge{1}.obj", lod_index + 1, merge_distance);
            string output_material_filename = string.Format(tempRoot + "wall_lod{0}_merge{1}.mtl", lod_index + 1, merge_distance); 
            string output_diffuse_filename = string.Format(tempRoot + "wall_lod{0}_merge{1}_diffuse.png", lod_index + 1, merge_distance);
            string output_normals_filename = string.Format(tempRoot + "wall_lod{0}_merge{1}_normals.png", lod_index + 1, merge_distance);


            // Import source geometry
            spGeometryData geom;
            spMaterialTable materials;
            Console.WriteLine("Importing wavefront .obj file...\n");
            {
                // Run import
                spWavefrontImporter importer = sdk.CreateWavefrontImporter();
                importer.SetExtractGroups(false); // We only want one large geometry, no need to extract groups 

                importer.SetImportFilePath(assetRoot + "wall.obj");
                if (!importer.RunImport())
                {
                    Console.WriteLine("Could not open input test file");
                    return false;
                }

                // Get the only geometry and the materials
                geom = importer.GetFirstGeometry();
                materials = importer.GetMaterials();
            }

            // Make a copy of the geometry, we need the original for texture casting later.
            // The remesher will replace the data of the geometry after it has processed it.
            spGeometryData red_geom = geom.NewCopy(true);

            // Create a Scene-object and a SceneMesh-object. 
            // Place the red_geom into the SceneMesh, and then the SceneMesh as a child to the RootNode.
            spScene scene = sdk.CreateScene();
            spSceneMesh mesh = sdk.CreateSceneMesh();
            mesh.SetGeometry(red_geom);
            mesh.SetName(red_geom.GetName().GetText());
            scene.GetRootNode().AddChild(mesh);

            spMappingImage mapping_image;

            // Remesh it
            Console.WriteLine("Running remesher...\n");
            {
                spRemeshingProcessor remesher = sdk.CreateRemeshingProcessor();

                //  Set target on-screen size in pixels
                remesher.GetRemeshingSettings().SetOnScreenSize(lod_sizes[lod_index]);
                //  Set the on-screen merge distance in pixels. Holes smaller than this will be sealed
                //  and geometries closer to each other than this will be merged.
                remesher.GetRemeshingSettings().SetMergeDistance(merge_distance);
                //  Disable the cutting plane
                remesher.GetRemeshingSettings().SetUseGroundPlane(false);
                //	Set to generate mapping image for texture casting.
                remesher.GetMappingImageSettings().SetGenerateMappingImage(true);

                remesher.SetSceneRoot(scene.GetRootNode());
                remesher.RemeshGeometry();

                // Mapping image is needed later on for texture casting.
                mapping_image = remesher.GetMappingImage();
            }

            spSceneMesh topmesh = Utils.SimplygonCast<spSceneMesh>(scene.GetRootNode().GetChild(0), false);

            // Cast diffuse texture and normal map data into a new material
            //	Create new material table.
            spMaterialTable output_materials = sdk.CreateMaterialTable();
            //	Create new material for the table.
            spMaterial output_material = sdk.CreateMaterial();
            output_materials.AddMaterial(output_material);

            // Cast diffuse texture data
            {
                // Cast the data using a color caster
                spColorCaster cast = sdk.CreateColorCaster();
                cast.SetColorType(SimplygonSDK.SG_MATERIAL_CHANNEL_DIFFUSE);
                cast.SetSourceMaterials(materials);
                cast.SetMappingImage(mapping_image); // The mapping image we got from the remeshing process.
                cast.SetOutputChannels(3); // RGB, 3 channels! (1 would be for grey scale, and 4 would be for RGBA.)
                cast.SetOutputChannelBitDepth(8); // 8 bits per channel. So in this case we will have 24bit colors RGB.
                cast.SetDilation(10); // To avoid mip-map artifacts, the empty pixels on the map needs to be filled to a degree aswell.
                cast.SetOutputFilePath(output_diffuse_filename); // Where the texture map will be saved to file.
                cast.CastMaterials(); // Fetch!

                // set the material properties 
                // Set the diffuse multiplier for the texture. 1 means it will not differ from original texture,
                // For example: 0 would ignore a specified color and 2 would make a color twice as pronounced as the others.
                output_material.SetDiffuseRed(1);
                output_material.SetDiffuseGreen(1);
                output_material.SetDiffuseBlue(1);
                // Set material to point to created texture filename.
                output_material.SetTexture(SimplygonSDK.SG_MATERIAL_CHANNEL_DIFFUSE, output_diffuse_filename);
            }

            // cast normal map texture data
            {
                // cast the data using a color caster
                spNormalCaster cast = sdk.CreateNormalCaster();
                cast.SetSourceMaterials(materials);
                cast.SetMappingImage(mapping_image);
                cast.SetOutputChannels(3); // RGB, 3 channels! (But really the x, y and z values for the normal)
                cast.SetOutputChannelBitDepth(8);
                cast.SetDilation(10);
                cast.SetOutputFilePath(output_normals_filename);
                cast.CastMaterials();

                // Set material to point to created texture filename.
                output_material.SetTexture(SimplygonSDK.SG_MATERIAL_CHANNEL_NORMALS, output_normals_filename);
            }

            // export the remeshed geometry to an OBJ file
            Console.WriteLine("Exporting wavefront .obj file...\n");
            {
                spWavefrontExporter exporter = sdk.CreateWavefrontExporter();
                exporter.SetExportFilePath(output_filename);
                exporter.SetSingleGeometry(topmesh.GetGeometry());
                exporter.SetMaterials(output_materials);
                if (!exporter.RunExport())
                {
                    Console.WriteLine("Failed to write result");
                    return false;
                }
            }
            return true;
        }


        static bool RunExample(ISimplygonSDK sdk)
        {
            // run twice per LOD
            for (int i = 0; i < num_lods; ++i)
            {
                Console.WriteLine("\n-------------------------------------------\n");
                Console.WriteLine("LOD {0} of {1}.", i + 1, num_lods);
                Console.WriteLine("\n-------------------------------------------\n");
                //Remesh with constant pixel size, but different merge distances

                Console.WriteLine("\nRunning with merge distance = {0}...\n", merge_distances[0]);
                Console.WriteLine("------------------------------------\n");
                if (!run_remeshing_for_lod(sdk, i, merge_distances[0]))
                {
                    return false;
                }
                Console.WriteLine("\nRunning with merge distance = {0}...\n", merge_distances[1]);
                Console.WriteLine("--------------\n");
                if (!run_remeshing_for_lod(sdk, i, merge_distances[1]))
                {
                    return false;
                }
                Console.WriteLine("\n");
            }
            return true;
        }
    }
}
