using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using SimplygonSDKCLR;
using BoneReductionExample;

namespace BoneReductionExample
{
    class BoneReductionExample
    {
        static void Main(string[] args)
        {
            // init SDK
            ISimplygonSDK sdk = Example.Example.InitExample();
            if (sdk == null)
            {
                return;
            }
            //MoveDirToExecutablePath(_T("RiggedSimplygonMan"), _T(""));

            // Run the example code
            RunExampleGenerateAndBendHelix(sdk);

            // deinit SDK
            //DeinitExample();

            return;
        }
        // total number of bones in the scene
        const int total_bone = 2;
        // number of bones influencing a vertex
        const int bone_count = 2;

        class Vector3D
        {
            public float x, y, z;
            public Vector3D(float _x, float _y, float _z)
            {
                x = _x;
                y = _y;
                z = _z;
            }
            public Vector3D(Vector3D v)
            {
                x = v.x;
                y = v.y;
                z = v.z;
            }
            public static Vector3D operator +(Vector3D v1, Vector3D v2)
            {
                return new Vector3D(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z);
            }
            public static Vector3D operator *(Vector3D v1, float s)
            {
                return new Vector3D(v1.x * s, v1.y * s, v1.z * s);
            }
            public static Vector3D operator *(float s, Vector3D v1)
            {
                return v1 * s;
            }
        }
        class Matrix4x4
        {
            float[] m;
            public Matrix4x4(float[] d)
            {
                m = d;
            }
            public Vector3D MultiplyPointVector(Vector3D vec)
            {
                Vector3D res = new Vector3D(0, 0, 0);
                res.x = vec.x * m[0 + 0 * 4] + vec.y * m[0 + 1 * 4] + vec.z * m[0 + 2 * 4] + m[0 + 3 * 4];
                res.y = vec.x * m[1 + 0 * 4] + vec.y * m[1 + 1 * 4] + vec.z * m[1 + 2 * 4] + m[1 + 3 * 4];
                res.z = vec.x * m[2 + 0 * 4] + vec.y * m[2 + 1 * 4] + vec.z * m[2 + 2 * 4] + m[2 + 3 * 4];
                return res;

            }
        }
        static Matrix4x4 GetMatrix4x4FromIMatrix(spMatrix4x4 src)
        {

            float[] srcElements = new float[16];
            src.GetElements(srcElements);
            return new Matrix4x4(srcElements);
        }

        static float GetRadFromDegrees(float deg)
        {
            return deg * (float)Math.PI / 180.0f;
        }

        static void RunExampleGenerateAndBendHelix(ISimplygonSDK sdk)
        {
            // generate the initial tube geometry
            Console.WriteLine("Generating helix-shaped tube...\n");
            spScene scene = generate_simple_tube(sdk);
            spScene sceneCpy = generate_simple_tube(sdk);

            string tempRoot = @"../../../../../temp/";

            string outputPath = tempRoot + "original_tube.obj";
            //store the original data to a wavefront file
            save_geometry_to_file(sdk, scene, outputPath);


            //take a copy of the original geometry and do a bend and save to file
            bend_geometry(sdk, sceneCpy);
            outputPath = tempRoot + "original_bended_tube.obj";
            save_geometry_to_file(sdk, sceneCpy, outputPath);

            // now, reduce the geometry, using max deviation
            Console.WriteLine("Reducing using max deviation (Bone reduced by half)...\n");
            RunReductionProcessing(sdk, scene, 1.0f, 0.5f);

            outputPath = tempRoot + "reduced_tube.obj";
            // store the reduced geometry to a wavefront file
            save_geometry_to_file(sdk, scene, outputPath);

            // now, bend the reduced tube using the blend weights
            Console.WriteLine("Bending the reduced tube using blend...\n");
            bend_geometry(sdk, scene);

            outputPath = tempRoot + "bended_reduced_tube.obj";
            // store the reduced geometry to a wavefront file
            save_geometry_to_file(sdk, scene, outputPath);
        }
        //this function generates a fixed tube
        static spScene generate_simple_tube(ISimplygonSDK sdk)
        {
            const int vertex_count = 16;
            const int triangle_count = 24;
            const int corner_count = triangle_count * 3;

            //create a scene object
            spScene scene = sdk.CreateScene();

            // triangles x 3 indices ( or 3 corners )
            int[] corner_ids = { 0, 1, 4,
													 4, 1, 5,
													 5, 1, 6,
													 1, 2, 6,
													 6, 2, 3,
													 6, 3, 7,
													 7, 3, 0,
													 7, 0, 4,


													 4, 5, 8,
													 8, 5, 9,
													 9, 5, 10,
													 5, 6, 10,
													 10, 6, 7,
													 10, 7, 11,
													 11, 7, 4,
													 11, 4, 8,


													 8, 9, 12,
													 12, 9, 13,
													 13, 9, 14,
													 9, 10, 14,
													 14, 10, 11,
													 14, 11, 15,
													 15, 11, 8,
													 15, 8, 12 };

            // vertices with values for the x, y and z coordinates.
            float[] vertex_coordinates = {   1.0f,  0.0f,  1.0f,
														1.0f,  0.0f,  -1.0f,
														-1.0f,  0.0f,  -1.0f,
														-1.0f,  0.0f,  1.0f,

														1.0f,  15.0f,  1.0f,
														1.0f,  15.0f,  -1.0f,
														-1.0f,  15.0f,  -1.0f,
														-1.0f,  15.0f,  1.0f,

														1.0f,  20.0f,  1.0f,
														1.0f,  20.0f,  -1.0f,
														-1.0f,  20.0f,  -1.0f,
														-1.0f,  20.0f,  1.0f,
		
														1.0f,  35.0f,  1.0f,
														1.0f,  35.0f,  -1.0f,
														-1.0f,  35.0f,  -1.0f,
														-1.0f,  35.0f,  1.0f };

            spGeometryData geom = sdk.CreateGeometryData();

            //add bone weights and ids to geometry data (per vertex)
            geom.AddBoneWeights(2);

            spRealArray coords = geom.GetCoords();
            spRidArray vertex_ids = geom.GetVertexIds();


            spRealArray BoneWeights = geom.GetBoneWeights();
            spRidArray BoneIds = geom.GetBoneIds();

            geom.SetVertexCount(vertex_count);
            geom.SetTriangleCount(triangle_count);

            //create the bone table
            spSceneBoneTable scn_bone_table = scene.GetBoneTable();

            //create an array to store bone ids
            spRidArray bone_ids = sdk.CreateRidArray();


            //create root bone for the scene
            spSceneBone root_bone = sdk.CreateSceneBone();
            root_bone.SetName("root_bone");

            //add the bone to the scene bone table and get a bone id
            int root_bone_id = scn_bone_table.AddBone(root_bone);


            //a
            bone_ids.AddItem(root_bone_id);

            spSceneBone parent_bone = root_bone;

            //create bones and populate the scene bone table
            for (uint bone_index = 1; bone_index < total_bone; bone_index++)
            {

                spSceneBone bone = sdk.CreateSceneBone();
                bone.SetName("ChildBone");
                spTransform3 boneTransform = sdk.CreateTransform3();

                //SET UP BONE IN BIND POSE
                //translate the child bone to its corrent position relative to the parent bone
                boneTransform.AddTransformation(bone.GetRelativeTransform());
                boneTransform.PreMultiply();
                boneTransform.AddTranslation(0.0f, 17.5f, 0.0f);

                //store the relatvice transform
                bone.GetRelativeTransform().DeepCopy(boneTransform.GetMatrix());

                //add bone to the scene bone table
                int bone_id = scn_bone_table.AddBone(bone);

                //link bone to parent bone
                parent_bone.AddChild(bone);
                bone_ids.AddItem(bone_id);

                parent_bone = bone;

            }


            float[] v = new float[3];
            for (int i = 0; i < vertex_count; ++i)
            {
                v[0] = vertex_coordinates[i * 3];
                v[1] = vertex_coordinates[i * 3 + 1];
                v[2] = vertex_coordinates[i * 3 + 2];
                coords.SetTuple(i, v);
                //real blend_val = real((rid(i)/rid(4)))/real(3);
                float blend_val = 0.5f;
                float blend1 = 1.0f - blend_val;
                float blend2 = blend_val;

                int bone_id_1 = 0;
                int bone_id_2 = 1;


                if (i < 4)
                {
                    bone_id_2 = -1;
                    blend2 = 0;
                    blend1 = 1;
                }
                else if (i > 11)
                {
                    bone_id_1 = -1;
                    blend2 = 1;
                    blend1 = 0;
                }

                blend1 *= blend1;
                blend2 *= blend2;

                //set the bone weights to perform skining
                BoneWeights.SetItem((i * 2) + 0, blend1);
                BoneWeights.SetItem((i * 2) + 1, blend2);

                //set the bone ids influencing the vertex.
                BoneIds.SetItem((i * 2) + 0, bone_id_1);
                BoneIds.SetItem((i * 2) + 1, bone_id_2);
            }

            for (int i = 0; i < corner_count; ++i)
            {
                vertex_ids.SetItem(i, corner_ids[i]);
            }

            //create a scene mesh	
            spSceneMesh mesh = sdk.CreateSceneMesh();

            mesh.SetGeometry(geom);
            mesh.SetName("mesh");

            //get the root node of the scene and add the root_bone and mesh to the scene
            scene.GetRootNode().AddChild(mesh);
            scene.GetRootNode().AddChild(root_bone);
            return scene;
        }

        // This function stores the data into an .obj file
        static bool save_geometry_to_file(ISimplygonSDK sdk, spScene scene, string filepath)
        {
            // create the wavefront exporter
            spWavefrontExporter exp = sdk.CreateWavefrontExporter();

            // set the geometry
            exp.SetScene(scene);


            // set file path
            exp.SetExportFilePath(filepath);

            // export to file
            return exp.RunExport();
        }

        static void bend_geometry(ISimplygonSDK sdk, spScene scene)
        {
            // The two bones that influence the vertices
            //spMatrix4x4 sp_bone1;

            spGeometryData geom = Utils.SimplygonCast<spSceneMesh>(scene.GetRootNode().GetChild(0)).GetGeometry();

            // get the bone weights field and ids
            spRealArray boneWeights = geom.GetBoneWeights();
            spRidArray boneIds = geom.GetBoneIds();

            // get the Coordinates field
            spRealArray Coords = geom.GetCoords();

            // now, transform all vertices' coordinates using the bones
            for (int v = 0; v < Coords.GetTupleCount(); ++v)
            {
                Vector3D vtx = new Vector3D(Coords.GetItem(v * 3 + 0), Coords.GetItem(v * 3 + 1), Coords.GetItem(v * 3 + 2));

                uint no = boneIds.GetItemCount();

                int bone_id_1 = boneIds.GetItem(v * 2 + 0);
                int bone_id_2 = boneIds.GetItem(v * 2 + 1);

                spSceneBone bone_1;
                spSceneBone bone_2;

                Matrix4x4 b1gtMat;
                Matrix4x4 b2gtMat;

                Vector3D vtx1 = new Vector3D(vtx);
                Vector3D vtx2 = new Vector3D(vtx);

                if (bone_id_1 != -1)
                {

                    bone_1 = scene.GetBoneTable().GetBone(bone_id_1);

                    //retrieve the global transform of the bone in bind space
                    spMatrix4x4 rootGlobalTransform = sdk.CreateMatrix4x4();
                    bone_1.EvaluateDefaultGlobalTransformation(rootGlobalTransform);

                    //apply transfrom to animate bone
                    spTransform3 bone1_transform = sdk.CreateTransform3();
                    bone1_transform.AddTransformation(rootGlobalTransform);
                    bone1_transform.AddRotation(GetRadFromDegrees(-30), 1, 0, 0);
                    rootGlobalTransform = bone1_transform.GetMatrix();

                    //apply transform
                    b1gtMat = GetMatrix4x4FromIMatrix(rootGlobalTransform);
                    vtx1 = b1gtMat.MultiplyPointVector(vtx);

                }

                if (bone_id_2 != -1)
                {
                    bone_2 = scene.GetBoneTable().GetBone(bone_id_2);

                    spMatrix4x4 boneGlobalTransform = sdk.CreateMatrix4x4();
                    bone_2.EvaluateDefaultGlobalTransformation(boneGlobalTransform);

                    spTransform3 bone2_transform = sdk.CreateTransform3();

                    //transform into bone2's local space and apply transform
                    bone2_transform.PreMultiply();
                    boneGlobalTransform.Invert();
                    bone2_transform.AddTransformation(boneGlobalTransform);
                    bone2_transform.AddRotation(GetRadFromDegrees(-30), 1, 0, 0);
                    bone2_transform.AddTranslation(0.0f, 17.5f, 0.0f);

                    //apply transform of the first bone
                    bone2_transform.AddRotation(GetRadFromDegrees(-30), 1, 0, 0);

                    //get the global transform matrix for the animation pose
                    boneGlobalTransform = bone2_transform.GetMatrix();
                    b2gtMat = GetMatrix4x4FromIMatrix(boneGlobalTransform);

                    //apply transform to the vertex
                    vtx2 = b2gtMat.MultiplyPointVector(vtx);
                }

                //get the bone weights from the geometry data
                float blend1 = boneWeights.GetItem(v * 2 + 0);
                float blend2 = boneWeights.GetItem(v * 2 + 1);

                // normalize the blend
                float blend_scale = 1.0f / (blend1 + blend2);
                blend1 *= blend_scale;
                blend2 *= blend_scale;


                // do a linear blend
                vtx = vtx1 * blend1 + vtx2 * blend2;

                // store in coordinates
                Coords.SetItem(v * 3 + 0, vtx.x);
                Coords.SetItem(v * 3 + 1, vtx.y);
                Coords.SetItem(v * 3 + 2, vtx.z);
            }
        }
        static void RunReductionProcessing(ISimplygonSDK sdk, spScene scene, float max_dev, float keep_bone_ratio)
        {
            // Create the reduction processor. Set the scene that is to be processed
            spReductionProcessor red = sdk.CreateReductionProcessor();
            red.SetScene(scene);

            ///////////////////////////////////////////////////
            //	Set the bone settings
            spBoneSettings boneSettings = red.GetBoneSettings();

            // Reduce bones based on percentage of bones in the scene.
            // Bone lod process tells the reduction processor the method
            // to use for bone reduction.
            boneSettings.SetBoneReductionTargets((uint)BoneReductionTargets.SG_BONEREDUCTIONTARGET_BONERATIO | (uint)BoneReductionTargets.SG_BONEREDUCTIONTARGET_ONSCREENSIZE);

            // Set the ratio of bones to keep in the scene
            boneSettings.SetBoneRatio(.5f);
            boneSettings.SetOnScreenSize(500);

            ///////////////////////////////////////////////////
            //
            // Set the Repair Settings. Current settings will mean that all visual gaps will remain in the geometry and thus 
            // hinder the reduction on geometries that contains gaps, holes and t-junctions.
            spRepairSettings repair_settings = red.GetRepairSettings();

            // Only vertices that actually share the same position will be welded together
            repair_settings.SetWeldDist(0.0f);

            // Only t-junctions with no actual visual distance will be fixed.
            repair_settings.SetTjuncDist(0.0f);

            ///////////////////////////////////////////////////
            //
            // Set the Reduction Settings.
            spReductionSettings reduction_settings = red.GetReductionSettings();

            // These flags will make the reduction process respect group and material setups, 
            // as well as preserve UV coordinates.

            // Reduce until we reach max deviation.
            reduction_settings.SetMaxDeviation(max_dev);

            ///////////////////////////////////////////////////
            //
            // Set the Normal Calculation Settings.
            spNormalCalculationSettings normal_settings = red.GetNormalCalculationSettings();

            // Will completely recalculate the normals.
            normal_settings.SetReplaceNormals(true);
            normal_settings.SetHardEdgeAngleInRadians(3.14159f * 90.0f / 180.0f);

            // Run the process
            red.RunProcessing();
        }

    }
}
