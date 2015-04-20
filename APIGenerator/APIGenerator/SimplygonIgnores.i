// We need to ignore operator = as that will be handled by copy constructors
%ignore *::operator=;
// Ignore smart pointer cast operator as there is no equivalent in Python. Need to use GetPointer to get underlying object, or better even is a
// typemap can be written to automatically cast the smart pointer to the underlying object for each smart pointer class.
%ignore *::operator SimplygonSDK::IArray*;
%ignore *::operator SimplygonSDK::IBinaryExporter*;
%ignore *::operator SimplygonSDK::IBinaryImporter*;
%ignore *::operator SimplygonSDK::IBoneSettings*;
%ignore *::operator SimplygonSDK::IBoolArray*;
%ignore *::operator SimplygonSDK::IBoolData*;
%ignore *::operator SimplygonSDK::ICamera*;
%ignore *::operator SimplygonSDK::ICameraPath*;
%ignore *::operator SimplygonSDK::ICharArray*;
%ignore *::operator SimplygonSDK::ICharData*;
%ignore *::operator SimplygonSDK::IChartAggregator*;
%ignore *::operator SimplygonSDK::IChunkedImageData*;
%ignore *::operator SimplygonSDK::IColorCaster*;
%ignore *::operator SimplygonSDK::IDirectXRenderer*;
%ignore *::operator SimplygonSDK::IDisplacementCaster*;
%ignore *::operator SimplygonSDK::IDoubleArray*;
%ignore *::operator SimplygonSDK::IDoubleData*;
%ignore *::operator SimplygonSDK::IFieldData*;
%ignore *::operator SimplygonSDK::IFloatArray*;
%ignore *::operator SimplygonSDK::IFloatData*;
%ignore *::operator SimplygonSDK::IGeometryData*;
%ignore *::operator SimplygonSDK::IGeometryDataCollection*;
%ignore *::operator SimplygonSDK::IGeometryGroup*;
%ignore *::operator SimplygonSDK::IGeometryTangentCalculator*;
%ignore *::operator SimplygonSDK::IGeometryValidator*;
%ignore *::operator SimplygonSDK::IGraphicsExporter*;
%ignore *::operator SimplygonSDK::IGraphicsImporter*;
%ignore *::operator SimplygonSDK::IImageData*;
%ignore *::operator SimplygonSDK::IImageDataImporter*;
%ignore *::operator SimplygonSDK::IIntArray*;
%ignore *::operator SimplygonSDK::IIntData*;
%ignore *::operator SimplygonSDK::ILongArray*;
%ignore *::operator SimplygonSDK::ILongData*;
%ignore *::operator SimplygonSDK::IMappingImage*;
%ignore *::operator SimplygonSDK::IMappingImageMeshData*;
%ignore *::operator SimplygonSDK::IMappingImageSettings*;
%ignore *::operator SimplygonSDK::IMaterial*;
%ignore *::operator SimplygonSDK::IMaterialCaster*;
%ignore *::operator SimplygonSDK::IMaterialTable*;
%ignore *::operator SimplygonSDK::IMatrix4x4*;
%ignore *::operator SimplygonSDK::INormalCalculationSettings*;
%ignore *::operator SimplygonSDK::INormalCaster*;
%ignore *::operator SimplygonSDK::INormalRepairer*;
%ignore *::operator SimplygonSDK::IObjectCollection*;
%ignore *::operator SimplygonSDK::IOpacityCaster*;
%ignore *::operator SimplygonSDK::IPackedGeometryData*;
%ignore *::operator SimplygonSDK::IParameterizer*;
%ignore *::operator SimplygonSDK::IProcessingObject*;
%ignore *::operator SimplygonSDK::IRcharArray*;
%ignore *::operator SimplygonSDK::IRcharData*;
%ignore *::operator SimplygonSDK::IRealArray*;
%ignore *::operator SimplygonSDK::IRealData*;
%ignore *::operator SimplygonSDK::IReductionProcessor*;
%ignore *::operator SimplygonSDK::IReductionSettings*;
%ignore *::operator SimplygonSDK::IRemeshingProcessor*;
%ignore *::operator SimplygonSDK::IRemeshingSettings*;
%ignore *::operator SimplygonSDK::IRepairSettings*;
%ignore *::operator SimplygonSDK::IRhandleArray*;
%ignore *::operator SimplygonSDK::IRhandleData*;
%ignore *::operator SimplygonSDK::IRidArray*;
%ignore *::operator SimplygonSDK::IRidData*;
%ignore *::operator SimplygonSDK::IScene*;
%ignore *::operator SimplygonSDK::ISceneAggregator*;
%ignore *::operator SimplygonSDK::ISceneAggregatorSettings*;
%ignore *::operator SimplygonSDK::ISceneBone*;
%ignore *::operator SimplygonSDK::ISceneBoneTable*;
%ignore *::operator SimplygonSDK::ISceneLodGroup*;
%ignore *::operator SimplygonSDK::ISceneMesh*;
%ignore *::operator SimplygonSDK::ISceneNode*;
%ignore *::operator SimplygonSDK::ISceneNodeCollection*;
%ignore *::operator SimplygonSDK::ISettingsObject*;
%ignore *::operator SimplygonSDK::IShaderData*;
%ignore *::operator SimplygonSDK::IShadingAddNode*;
%ignore *::operator SimplygonSDK::IShadingClampNode*;
%ignore *::operator SimplygonSDK::IShadingColorNode*;
%ignore *::operator SimplygonSDK::IShadingCustomNode*;
%ignore *::operator SimplygonSDK::IShadingDivideNode*;
%ignore *::operator SimplygonSDK::IShadingFilterNode*;
%ignore *::operator SimplygonSDK::IShadingInterpolateNode*;
%ignore *::operator SimplygonSDK::IShadingMultiplyNode*;
%ignore *::operator SimplygonSDK::IShadingNode*;
%ignore *::operator SimplygonSDK::IShadingSubtractNode*;
%ignore *::operator SimplygonSDK::IShadingSwizzlingNode*;
%ignore *::operator SimplygonSDK::IShadingTextureNode*;
%ignore *::operator SimplygonSDK::IShadingVertexColorNode*;
%ignore *::operator SimplygonSDK::IShortArray*;
%ignore *::operator SimplygonSDK::IShortData*;
%ignore *::operator SimplygonSDK::IStringArray*;
%ignore *::operator SimplygonSDK::ITable*;
%ignore *::operator SimplygonSDK::ITexture*;
%ignore *::operator SimplygonSDK::ITextureTable*;
%ignore *::operator SimplygonSDK::ITransform3*;
%ignore *::operator SimplygonSDK::IUnsignedCharArray*;
%ignore *::operator SimplygonSDK::IUnsignedCharData*;
%ignore *::operator SimplygonSDK::IUnsignedIntArray*;
%ignore *::operator SimplygonSDK::IUnsignedIntData*;
%ignore *::operator SimplygonSDK::IUnsignedLongArray*;
%ignore *::operator SimplygonSDK::IUnsignedLongData*;
%ignore *::operator SimplygonSDK::IUnsignedShortArray*;
%ignore *::operator SimplygonSDK::IUnsignedShortData*;
%ignore *::operator SimplygonSDK::IValueArray*;
%ignore *::operator SimplygonSDK::IWavefrontExporter*;
%ignore *::operator SimplygonSDK::IWavefrontImporter*;
%ignore *::operator SimplygonSDK::IVertexColorBaker*;
%ignore *::operator SimplygonSDK::IVisibilitySettings*;
%ignore *::operator SimplygonSDK::IString*;
%ignore *::operator SimplygonSDK::IImpostorSettings*;
%ignore *::operator SimplygonSDK::IImpostorProcessor*;
%ignore *::operator SimplygonSDK::ISurfaceMapper*;
%ignore *::operator SimplygonSDK::IShadingStepNode*;
%ignore *::operator SimplygonSDK::IShadingMinNode*;
%ignore *::operator SimplygonSDK::IShadingMaxNode*;
%ignore *::operator SimplygonSDK::INormalAnalyzer*;
%ignore *::operator SimplygonSDK::IImageDataExporter*;
%ignore *::operator SimplygonSDK::IGeometryAnalyzer*;
%ignore *::operator SimplygonSDK::IUVAnalyzer*;

// Don't generate api classes for the interfaces, only for the smart pointers. Keeps the size down.
%ignore IArray;
%ignore IBinaryExporter;
%ignore IBinaryImporter;
%ignore IBoneSettings;
%ignore IBoolArray;
%ignore IBoolData;
%ignore ICamera;
%ignore ICameraPath;
%ignore ICharArray;
%ignore ICharData;
%ignore IChartAggregator;
%ignore IChunkedImageData;
%ignore IColorCaster;
%ignore IDirectXRenderer;
%ignore IDisplacementCaster;
%ignore IDoubleArray;
%ignore IDoubleData;
%ignore IFieldData;
%ignore IFloatArray;
%ignore IFloatData;
%ignore IGeometryData;
%ignore IGeometryDataCollection;
%ignore IGeometryGroup;
%ignore IGeometryTangentCalculator;
%ignore IGeometryValidator;
%ignore IGraphicsExporter;
%ignore IGraphicsImporter;
%ignore IImageData;
%ignore IImageDataImporter;
%ignore IIntArray;
%ignore IIntData;
%ignore ILongArray;
%ignore ILongData;
%ignore IMappingImage;
%ignore IMappingImageMeshData;
%ignore IMappingImageSettings;
%ignore IMaterial;
%ignore IMaterialCaster;
%ignore IMaterialTable;
%ignore IMatrix4x4;
%ignore INormalCalculationSettings;
%ignore INormalCaster;
%ignore INormalRepairer;
%ignore IObjectCollection;
%ignore IOpacityCaster;
%ignore IPackedGeometryData;
%ignore IParameterizer;
%ignore IProcessingObject;
%ignore IRcharArray;
%ignore IRcharData;
%ignore IRealArray;
%ignore IRealData;
%ignore IReductionProcessor;
%ignore IReductionSettings;
%ignore IRemeshingProcessor;
%ignore IRemeshingSettings;
%ignore IRepairSettings;
%ignore IRhandleArray;
%ignore IRhandleData;
%ignore IRidArray;
%ignore IRidData;
%ignore IScene;
%ignore ISceneAggregator;
%ignore ISceneAggregatorSettings;
%ignore ISceneBone;
%ignore ISceneBoneTable;
%ignore ISceneLodGroup;
%ignore ISceneMesh;
%ignore ISceneNode;
%ignore ISceneNodeCollection;
%ignore ISettingsObject;
%ignore IShaderData;
%ignore IShadingAddNode;
%ignore IShadingClampNode;
%ignore IShadingColorNode;
%ignore IShadingCustomNode;
%ignore IShadingDivideNode;
%ignore IShadingFilterNode;
%ignore IShadingInterpolateNode;
%ignore IShadingMultiplyNode;
%ignore IShadingNode;
%ignore IShadingSubtractNode;
%ignore IShadingSwizzlingNode;
%ignore IShadingTextureNode;
%ignore IShadingVertexColorNode;
%ignore IShortArray;
%ignore IShortData;
%ignore IStringArray;
%ignore ITable;
%ignore ITexture;
%ignore ITextureTable;
%ignore ITransform3;
%ignore IUnsignedCharArray;
%ignore IUnsignedCharData;
%ignore IUnsignedIntArray;
%ignore IUnsignedIntData;
%ignore IUnsignedLongArray;
%ignore IUnsignedLongData;
%ignore IUnsignedShortArray;
%ignore IUnsignedShortData;
%ignore IValueArray;
%ignore IWavefrontExporter;
%ignore IWavefrontImporter;
%ignore IVertexColorBaker;
%ignore IVisibilitySettings;
%ignore IString;
%ignore IImpostorSettings;
%ignore IImpostorProcessor;
%ignore ISurfaceMapper;
%ignore IShadingStepNode;
%ignore IShadingMinNode;
%ignore IShadingMaxNode;
%ignore INormalAnalyzer;
%ignore IImageDataExporter;
%ignore IGeometryAnalyzer;
%ignore IUVAnalyzer;


// Additional cast operators that needs to be ignored
%ignore *::operator const value_type*;
%ignore *::operator const rchar*;

// Ignore deprecated stuff in the api header (is it possible to detect the SGDEPRECATED tag?)
// and autogenerate this?
%ignore SimplygonSDK::SG_MATERIAL_TEXTURE_AMBIENT;
%ignore SimplygonSDK::SG_BONES_PER_VERTEX;
%ignore SimplygonSDK::SG_MATERIAL_TEXTURE_DIFFUSE;
%ignore SimplygonSDK::SG_MATERIAL_TEXTURE_SPECULAR;
%ignore SimplygonSDK::SG_MATERIAL_TEXTURE_OPACITY;
%ignore SimplygonSDK::SG_MATERIAL_TEXTURE_EMISSIVE;
%ignore SimplygonSDK::SG_MATERIAL_TEXTURE_NORMALS;
%ignore SimplygonSDK::SG_MATERIAL_TEXTURE_GROUPIDS;
%ignore SimplygonSDK::SG_MATERIAL_TEXTURE_DISPLACEMENT;
%ignore SimplygonSDK::IGeometryData::RemoveBoneIds();
%ignore SimplygonSDK::IGeometryData::GetTriangleVertices();
%ignore SimplygonSDK::IGeometryData::GetSpecularColors();
%ignore SimplygonSDK::IGeometryData::CopyTriangleVertex( IGeometryData *source , rid dest_id , rid src_id );
%ignore SimplygonSDK::IGeometryData::RemoveUserTriangleVertexField(const char * );
%ignore SimplygonSDK::IGeometryData::CopyCombineTriangleVertices( IGeometryData *source , rid dest_id , rid src_id_1 , rid src_id_2 , real alpha );
%ignore SimplygonSDK::IGeometryData::AddUserTriangleVertexField( IValueArray *field );
%ignore SimplygonSDK::IGeometryData::CopyCombine3TriangleVertices( IGeometryData *source , rid dest_id , rid src_id_1 , rid src_id_2 , rid src_id_3 , real alpha_1 , real alpha_2 );
%ignore SimplygonSDK::IGeometryData::GetUserTriangleVertexField(const char * name );
%ignore SimplygonSDK::IGeometryData::AddBitangents( rid level );
%ignore SimplygonSDK::IGeometryData::AddBoneIds( unsigned int level );
%ignore SimplygonSDK::IGeometryData::AddBaseTypeUserTriangleVertexField( rid base_type , const char * name , unsigned int tuple_size );
%ignore SimplygonSDK::IGeometryData::AddDiffuseColors();
%ignore SimplygonSDK::IGeometryData::RemoveDiffuseColors();
%ignore SimplygonSDK::IGeometryData::GetDiffuseColors();
%ignore SimplygonSDK::IGeometryData::AddSpecularColors();
%ignore SimplygonSDK::IGeometryData::RemoveSpecularColors();
%ignore SimplygonSDK::IGeometryData::RemoveBitangents( rid level );
%ignore SimplygonSDK::IPackedGeometryData::RemoveSpecularColors();
%ignore SimplygonSDK::IPackedGeometryData::AddDiffuseColors();
%ignore SimplygonSDK::IPackedGeometryData::GetSpecularColors();
%ignore SimplygonSDK::IPackedGeometryData::RemoveDiffuseColors();
%ignore SimplygonSDK::IPackedGeometryData::RemoveBitangents( rid level );
%ignore SimplygonSDK::IPackedGeometryData::AddSpecularColors();
%ignore SimplygonSDK::IPackedGeometryData::AddBitangents( rid level );
%ignore SimplygonSDK::IPackedGeometryData::GetDiffuseColors();
