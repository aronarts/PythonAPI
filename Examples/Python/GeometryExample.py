import SimplygonSDK as SDK
import SimplygonUtils as Utils
import os

exampleName = "GeometryExample"

def main():
    Utils.InitExample()
    SDK.InitErrorhandling();
    # Run the example code
    print ("Generating example 1")
    RunExample1();
    print ("Generating example 2")
    RunExample2();
    print ("Generating example 3")
    RunExample3();
    print ("Done")
    Utils.DeinitExample();

def RunExample1():
    # 4 separate triangles, with 3 vertices each and 3 sets of UV coordinates each.
    # They make up 2 quads, where each quad have same set of UV coordinates.

    # Concept
    # Triangles, Corners and Vertices
    #
    #    v0______________v1    v3  v6______________v7    v9  
    #     |c0       c1  /     /|    |c6       c7  /     /|
    #     |           /     /c3|    |           /     /c9|
    #     |         /     /    |    |         /     /    |
    #     |  t0   /     /  t1  |    |  t2   /     /  t3  |
    #     |     /     /        |    |     /     /        |
    #     |c2 /     /c5      c4|    |c8 /     /c11    c10|
    #     | /     /____________|    | /     /____________| 
    #    v2     v5            v4   v8     v11            v10

    vertex_count = 12
    triangle_count = 4
    corner_count = triangle_count * 3

    # 4 triangles x 3 indices ( or 3 corners )
    corner_ids = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ]

    # 12 vertices with values for the x, y and z coordinates.
    vertex_coordinates = [[0.0,  0.0,  0.0],
                          [1.0,  0.0,  0.0],
                          [1.0,  1.0,  0.0],
                          [1.0,  1.0,  0.0],
                          [0.0,  1.0,  0.0],
                          [0.0,  0.0,  0.0],
                          [1.0,  0.0,  0.0],
                          [2.0,  0.0,  0.0],
                          [2.0,  1.0,  0.0],
                          [2.0,  1.0,  0.0],
                          [1.0,  1.0,  0.0],
                          [1.0,  0.0,  0.0]]

    # UV coordinates for all 12 corners.
    texture_coordinates = [  [0.0,  0.0],  
                             [1.0,  0.0],  
                             [1.0,  1.0],  

                             [1.0,  1.0],  
                             [0.0,  1.0],  
                             [0.0,  0.0],	 

                             [0.0,  0.0],  
                             [1.0,  0.0],  
                             [1.0,  1.0],  

                             [1.0,  1.0],  
                             [0.0,  1.0],  
                             [0.0,  0.0]]

    # Create the Geometry. All geometrydata will be loaded into this object
    geom = Utils.GetSDK().CreateGeometryData();

    # Array with vertex-coordinates. Will contain 3 real-values for each vertex in the geometry.
    coords = geom.GetCoords();             

    # Array with triangle-data. Will contain 3 ids for each corner of each triangle, so the triangles know what vertices to use.
    vertex_ids = geom.GetVertexIds();

    # Must add texture channel before adding data to it. 
    geom.AddTexCoords( 0 );
    texcoords = geom.GetTexCoords( 0 );

    # Set vertex- and triangle-counts for the Geometry. 
    # NOTE: The number of vertices and triangles has to be set before vertex- and triangle-data is loaded into the GeometryData.
    geom.SetVertexCount(vertex_count);
    geom.SetTriangleCount(triangle_count);
    # add vertex-coordinates to the Geometry. Each tuple contains the 3 coordinates for each vertex. x, y and z values.
    for i in range(0,vertex_count):
        coords.SetTuple(i , vertex_coordinates[i]);

    for i in range(0,corner_count):
        texcoords.SetTuple( i, texture_coordinates[i] );


    # Add triangles to the Geometry. Each triangle-corner contains the id for the vertex that corner uses.
    # SetTuple can also be used, but since the TupleSize of the vertex_ids array is 1, it would make no difference.
    # (This since the vertex_ids array is corner-based, not triangle-based.)
    for i in range(0,corner_count):
        vertex_ids.SetItem( i , corner_ids[i] );


    # Setup the Exporter for storing the reduced mesh to file
    objexp = Utils.GetSDK().CreateWavefrontExporter();


    outputPath = Utils.GetOutputPath(exampleName, "Quad.obj")
    objexp.SetExportFilePath( outputPath );
    objexp.SetSingleGeometry( geom );
    objexp.RunExport();

def RunExample2():

    # Same as RunExample1, but now the vertices are shared among the triangles.
    
    # Concept
    # Triangles, Corners and Vertices
    #
    #    v0______________v1_____________v4
    #     |c0       c1 / |c6       c7 / |	 	 
    #     |          / c3|          / c9|
    #     |        /     |        /     |	 	 
    #     |  t0  /   t1  |  t2  /   t3  |	 	 
    #     |    /         |    /         |	 	 
    #     |c2/ c5      c4|c8/ c11    c10|
    #     |/_____________|/_____________|
    #    v2              v3             v5
    
    vertex_count = 6;
    triangle_count = 4;
    corner_count = triangle_count * 3;

    corner_ids = [ 0, 1, 2, 0, 2, 3, 1, 4, 5, 1, 5, 2 ];

    vertex_coordinates = [[0.0,  0.0,  0.0],
                            [1.0,  0.0,  0.0],
                            [1.0,  1.0,  0.0],
                            [0.0,  1.0,  0.0],
                            [2.0,  0.0,  0.0],
                            [2.0,  1.0,  0.0]];

    texture_coordinates = [[0.0,  0.0],
                             [1.0,  0.0],  
                             [1.0,  1.0],  

                             [1.0,  1.0],  
                             [0.0,  1.0],  
                             [0.0,  0.0],	 

                             [0.0,  0.0],  
                             [1.0,  0.0],  
                             [1.0,  1.0],  

                             [1.0,  1.0],  
                             [0.0,  1.0],  
                             [0.0,  0.0]];


    geom = Utils.GetSDK().CreateGeometryData();

    coords = geom.GetCoords();

    vertex_ids = geom.GetVertexIds();

    geom.AddTexCoords( 0 );
    texcoords = geom.GetTexCoords( 0 );

    geom.SetVertexCount(vertex_count);
    geom.SetTriangleCount(triangle_count);
	
    for i in range(0,vertex_count):
        coords.SetTuple(i , vertex_coordinates[i]);

    for i in range(0,corner_count):
        texcoords.SetTuple( i, texture_coordinates[i] );

    for i in range(0,corner_count):
        vertex_ids.SetItem( i , corner_ids[i] );

    # Setup the Exporter for storing the reduced mesh to file
    objexp = Utils.GetSDK().CreateWavefrontExporter()

    outputPath = Utils.GetOutputPath(exampleName, "Quad2.obj");
    objexp.SetExportFilePath( outputPath );
    objexp.SetSingleGeometry( geom );
    objexp.RunExport();


def RunExample3():

    # Same as RunExample1, but now all corner-data is stored as vertex-data, in a packet format.
    # Since the 2 vertices where the quads meet dont share same UV, they will be 2 separate vertices, 
    # so 4 vertices / quad as opposed to 6 / quad in RunExample1, and only 6 for whole mesh in RunExample2.


    # Concept
    #
    #    v0______________v1  v4______________v5
    #     |            / |    |            / | 
    #     |          /   |    |          /   |
    #     |        /     |    |        /     | 
    #     |  t0  /   t1  |    |  t2  /   t3  | 
    #     |    /         |    |    /         | 
    #     |  /           |    |  /           |
    #     |/_____________|    |/_____________|
    #    v2              v3  v6              v7


    vertex_count = 8;
    triangle_count = 4;
    corner_count = triangle_count * 3;

    # 4 triangles x 3 indices ( or 3 corners )
    corner_ids  = [  0, 1, 2,0, 2, 3,4, 5, 6, 4, 6, 7 ];

    # 8 vertices with values for the x, y and z coordinates.
    vertex_coordinates  = [ [0.0,  0.0,  0.0],
                            [1.0,  0.0,  0.0],
                            [1.0,  1.0,  0.0],
                            [0.0,  1.0,  0.0],
                            [1.0,  0.0,  0.0],
                            [2.0,  0.0,  0.0],
                            [2.0,  1.0,  0.0],
                            [1.0,  1.0,  0.0] ];

    # UV coordinates for all 8 vertices.
    texture_coordinates = [  [0.0,  0.0],  
                             [1.0,  0.0],  
                             [1.0,  1.0],  
                             [0.0,  1.0],  
                             [0.0,  0.0],  
                             [1.0,  0.0],  
                             [1.0,  1.0],  
                             [0.0,  1.0]];

    # Create the PackedGeometry. All geometrydata will be loaded into this object
    geom = Utils.GetSDK().CreatePackedGeometryData();

    # Set vertex- and triangle-counts for the Geometry. 
    # NOTE: The number of vertices and triangles has to be set before vertex- and triangle-data is loaded into the GeometryData.
    geom.SetVertexCount(vertex_count);
    geom.SetTriangleCount(triangle_count);
    
    # Array with vertex-coordinates. Will contain 3 real-values for each vertex in the geometry.
    coords = geom.GetCoords();

    # Array with triangle-data. Will contain 3 ids for each corner of each triangle, so the triangles know what vertices to use.
    vertex_ids = geom.GetVertexIds();

    # Must add texture channel before adding data to it. 
    geom.AddTexCoords( 0 );
    texcoords = geom.GetTexCoords( 0 );

    # add vertex-coordinates to the Geometry. Each tuple contains the 3 coordinates for each vertex. x, y and z values.
    for i in range(0,vertex_count):
        coords.SetTuple( i , vertex_coordinates[i] );
        texcoords.SetTuple( i, texture_coordinates[i] );

    
    # Add triangles to the Geometry. Each triangle-corner contains the id for the vertex that corner uses.
    # SetTuple can also be used, but since the TupleSize of the vertex_ids array is 1, it would make no difference.
    # (This since the vertex_ids array is corner-based, not triangle-based.)
    for i in range(0,corner_count):
        vertex_ids.SetItem( i , corner_ids[i] );

    # Setup the Exporter for storing the reduced mesh to file
    objexp = Utils.GetSDK().CreateWavefrontExporter()

    outputPath = Utils.GetOutputPath(exampleName, "Quad3.obj");
    objexp.SetExportFilePath( outputPath );
    objexp.SetSingleGeometry( geom.NewUnpackedCopy() );
    objexp.RunExport();

main()

