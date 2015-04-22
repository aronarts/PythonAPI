#if defined(SWIGPYTHON)
%typemap(in) SimplygonSDK::real *tuple {
		int i;
		if (!PyList_Check($input))
		{
		  PyErr_SetString(PyExc_ValueError, "Expecting a list");
		  return NULL;
		}
		int listSize = (int)PyList_Size($input); //get size of the list
		$1 = (real*) malloc((listSize)*sizeof(real)); //allocate memory with the correct size
		for (i = 0; i < listSize; i++)
		{
			PyObject *s = PyList_GetItem($input,i);
			if (!PyFloat_Check(s))
			{
		      free($1);
		      PyErr_SetString(PyExc_ValueError, "List items must be floats");
		      return NULL;
			}
			$1[i] = (real)PyFloat_AsDouble(s); //put the value into the array
		}
}
%typemap(freearg) SimplygonSDK::real *tuple{
		if ($1) free($1);
}

// IN order to block memory leaks for const char * variables. Prevents setting the values.
%typemap(varin) const char * { 
   SWIG_Error(SWIG_AttributeError,"Variable $symname is read-only."); 
   SWIG_fail; 
} 

%typemap(in) intptr_t {
	$1 = PyInt_AsLong($input);
}

%typemap(in) unsigned int {
	$1 = (unsigned int)PyInt_AsLong($input);
}

//Converting an reference array to output instead.
%typemap(in, numinputs=0) SimplygonSDK::real dest_param[3] {
  real tmp[3];
  $1 = tmp;
}
%typemap(argout) SimplygonSDK::real dest_param[3]{
    PyObject *o = PyList_New(3);
    int i;
    for(i=0; i<3; i++)
    {
        PyList_SetItem(o, i, PyFloat_FromDouble($1[i]));
    }
    $result = o;
}

// The following type maps allows for both the interface object and smart pointers to be passed into the same function call.
// First we need to define a number of macros that allows for polymorphism in smart pointers. We do not need to declare allowed
// types for the interface objects as SWIG handles inheritance there, but all allowed smart pointers needs to be declared.
%define BeginAllowedTypes()
if (SWIG_ConvertPtr($input, (void **) &$1, $1_descriptor,0) == -1) {
	bool foundMatch = false;
	const char *inputType = $input->ob_type->tp_name;
	char errorMessage[1024];
	sprintf_s(errorMessage, 1024, "Faulty input object type: %s. The function only accepts parameters of the following types: ", inputType);
%enddef

%define AllowedType(TYPE)
	{
		sprintf_s(errorMessage, 1024, "%s %s,", errorMessage, "TYPE");
		TYPE *temp;
		if (!foundMatch && SWIG_ConvertPtr($input, (void **) &temp, $descriptor(SimplygonSDK::TYPE *),0) != -1) {
			$1 = temp->GetPointer(); 
			foundMatch = true;
		}
	}
%enddef

%define EndAllowedTypes()	
	if(!foundMatch)
	{
		PyErr_SetString(PyExc_ValueError,errorMessage);
		return NULL; 
	}
}
%enddef


%typemap(in) SimplygonSDK::IArray * {
  BeginAllowedTypes()
  AllowedType(spArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IBinaryExporter * {
  BeginAllowedTypes()
  AllowedType(spBinaryExporter)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IBinaryImporter * {
  BeginAllowedTypes()
  AllowedType(spBinaryImporter)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IBoneSettings * {
  BeginAllowedTypes()
  AllowedType(spBoneSettings)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IBoolArray * {
  BeginAllowedTypes()
  AllowedType(spBoolArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IBoolData * {
  BeginAllowedTypes()
  AllowedType(spBoolData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ICamera * {
  BeginAllowedTypes()
  AllowedType(spCamera)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ICameraPath * {
  BeginAllowedTypes()
  AllowedType(spCameraPath)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ICharArray * {
  BeginAllowedTypes()
  AllowedType(spCharArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ICharData * {
  BeginAllowedTypes()
  AllowedType(spCharData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IChartAggregator * {
  BeginAllowedTypes()
  AllowedType(spChartAggregator)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IChunkedImageData * {
  BeginAllowedTypes()
  AllowedType(spChunkedImageData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IColorCaster * {
  BeginAllowedTypes()
  AllowedType(spColorCaster)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IDirectXRenderer * {
  BeginAllowedTypes()
  AllowedType(spDirectXRenderer)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IDisplacementCaster * {
  BeginAllowedTypes()
  AllowedType(spDisplacementCaster)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IDoubleArray * {
  BeginAllowedTypes()
  AllowedType(spDoubleArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IDoubleData * {
  BeginAllowedTypes()
  AllowedType(spDoubleData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IFieldData * {
  BeginAllowedTypes()
  AllowedType(spFieldData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IFloatArray * {
  BeginAllowedTypes()
  AllowedType(spFloatArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IFloatData * {
  BeginAllowedTypes()
  AllowedType(spFloatData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IGeometryData * {
  BeginAllowedTypes()
  AllowedType(spGeometryData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IGeometryDataCollection * {
  BeginAllowedTypes()
  AllowedType(spGeometryDataCollection)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IGeometryGroup * {
  BeginAllowedTypes()
  AllowedType(spGeometryGroup)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IGeometryTangentCalculator * {
  BeginAllowedTypes()
  AllowedType(spGeometryTangentCalculator)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IGeometryValidator * {
  BeginAllowedTypes()
  AllowedType(spGeometryValidator)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IGraphicsExporter * {
  BeginAllowedTypes()
  AllowedType(spGraphicsExporter)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IGraphicsImporter * {
  BeginAllowedTypes()
  AllowedType(spGraphicsImporter)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IImageData * {
  BeginAllowedTypes()
  AllowedType(spImageData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IImageDataImporter * {
  BeginAllowedTypes()
  AllowedType(spImageDataImporter)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IIntArray * {
  BeginAllowedTypes()
  AllowedType(spIntArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IIntData * {
  BeginAllowedTypes()
  AllowedType(spIntData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ILongArray * {
  BeginAllowedTypes()
  AllowedType(spLongArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ILongData * {
  BeginAllowedTypes()
  AllowedType(spLongData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IMappingImage * {
  BeginAllowedTypes()
  AllowedType(spMappingImage)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IMappingImageMeshData * {
  BeginAllowedTypes()
  AllowedType(spMappingImageMeshData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IMappingImageSettings * {
  BeginAllowedTypes()
  AllowedType(spMappingImageSettings)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IMaterial * {
  BeginAllowedTypes()
  AllowedType(spMaterial)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IMaterialCaster * {
  BeginAllowedTypes()
  AllowedType(spMaterialCaster)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IMaterialTable * {
  BeginAllowedTypes()
  AllowedType(spMaterialTable)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IMatrix4x4 * {
  BeginAllowedTypes()
  AllowedType(spMatrix4x4)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::INormalCalculationSettings * {
  BeginAllowedTypes()
  AllowedType(spNormalCalculationSettings)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::INormalCaster * {
  BeginAllowedTypes()
  AllowedType(spNormalCaster)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::INormalRepairer * {
  BeginAllowedTypes()
  AllowedType(spNormalRepairer)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IObjectCollection * {
  BeginAllowedTypes()
  AllowedType(spObjectCollection)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IOpacityCaster * {
  BeginAllowedTypes()
  AllowedType(spOpacityCaster)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IPackedGeometryData * {
  BeginAllowedTypes()
  AllowedType(spPackedGeometryData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IParameterizer * {
  BeginAllowedTypes()
  AllowedType(spParameterizer)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IProcessingObject * {
  BeginAllowedTypes()
  AllowedType(spProcessingObject)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IRcharArray * {
  BeginAllowedTypes()
  AllowedType(spRcharArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IRcharData * {
  BeginAllowedTypes()
  AllowedType(spRcharData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IRealArray * {
  BeginAllowedTypes()
  AllowedType(spRealArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IRealData * {
  BeginAllowedTypes()
  AllowedType(spRealData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IReductionProcessor * {
  BeginAllowedTypes()
  AllowedType(spReductionProcessor)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IReductionSettings * {
  BeginAllowedTypes()
  AllowedType(spReductionSettings)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IRemeshingProcessor * {
  BeginAllowedTypes()
  AllowedType(spRemeshingProcessor)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IRemeshingSettings * {
  BeginAllowedTypes()
  AllowedType(spRemeshingSettings)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IRepairSettings * {
  BeginAllowedTypes()
  AllowedType(spRepairSettings)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IRhandleArray * {
  BeginAllowedTypes()
  AllowedType(spRhandleArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IRhandleData * {
  BeginAllowedTypes()
  AllowedType(spRhandleData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IRidArray * {
  BeginAllowedTypes()
  AllowedType(spRidArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IRidData * {
  BeginAllowedTypes()
  AllowedType(spRidData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IScene * {
  BeginAllowedTypes()
  AllowedType(spScene)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ISceneAggregator * {
  BeginAllowedTypes()
  AllowedType(spSceneAggregator)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ISceneAggregatorSettings * {
  BeginAllowedTypes()
  AllowedType(spSceneAggregatorSettings)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ISceneBone * {
  BeginAllowedTypes()
  AllowedType(spSceneBone)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ISceneBoneTable * {
  BeginAllowedTypes()
  AllowedType(spSceneBoneTable)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ISceneLodGroup * {
  BeginAllowedTypes()
  AllowedType(spSceneLodGroup)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ISceneMesh * {
  BeginAllowedTypes()
  AllowedType(spSceneMesh)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ISceneNode * {
	BeginAllowedTypes()
	AllowedType(spSceneNode)
	AllowedType(spSceneMesh)
	AllowedType(spSceneLodGroup)
	AllowedType(spSceneBone)
	EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ISceneNodeCollection * {
  BeginAllowedTypes()
  AllowedType(spSceneNodeCollection)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ISettingsObject * {
  BeginAllowedTypes()
  AllowedType(spSettingsObject)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShaderData * {
  BeginAllowedTypes()
  AllowedType(spShaderData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingAddNode * {
  BeginAllowedTypes()
  AllowedType(spShadingAddNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingClampNode * {
  BeginAllowedTypes()
  AllowedType(spShadingClampNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingColorNode * {
  BeginAllowedTypes()
  AllowedType(spShadingColorNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingCustomNode * {
  BeginAllowedTypes()
  AllowedType(spShadingCustomNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingDivideNode * {
  BeginAllowedTypes()
  AllowedType(spShadingDivideNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingFilterNode * {
  BeginAllowedTypes()
  AllowedType(spShadingFilterNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingInterpolateNode * {
  BeginAllowedTypes()
  AllowedType(spShadingInterpolateNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingMultiplyNode * {
  BeginAllowedTypes()
  AllowedType(spShadingMultiplyNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingNode * {
  BeginAllowedTypes()
  AllowedType(spShadingNode)
  AllowedType(spShadingFilterNode)
  AllowedType(spShadingTextureNode)
  AllowedType(spShadingSwizzlingNode)
  AllowedType(spShadingColorNode)
  AllowedType(spShadingAddNode)
  AllowedType(spShadingSubtractNode)
  AllowedType(spShadingMultiplyNode)
  AllowedType(spShadingDivideNode)
  AllowedType(spShadingClampNode)
  AllowedType(spShadingDivideNode)
  AllowedType(spShadingVertexColorNode)
  AllowedType(spShadingCustomNode)
  AllowedType(spShadingInterpolateNode)  
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingSubtractNode * {
  BeginAllowedTypes()
  AllowedType(spShadingSubtractNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingSwizzlingNode * {
  BeginAllowedTypes()
  AllowedType(spShadingSwizzlingNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingTextureNode * {
  BeginAllowedTypes()
  AllowedType(spShadingTextureNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShadingVertexColorNode * {
  BeginAllowedTypes()
  AllowedType(spShadingVertexColorNode)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShortArray * {
  BeginAllowedTypes()
  AllowedType(spShortArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IShortData * {
  BeginAllowedTypes()
  AllowedType(spShortData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IStringArray * {
  BeginAllowedTypes()
  AllowedType(spStringArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ITable * {
  BeginAllowedTypes()
  AllowedType(spTable)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ITexture * {
  BeginAllowedTypes()
  AllowedType(spTexture)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ITextureTable * {
  BeginAllowedTypes()
  AllowedType(spTextureTable)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::ITransform3 * {
  BeginAllowedTypes()
  AllowedType(spTransform3)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IUnsignedCharArray * {
  BeginAllowedTypes()
  AllowedType(spUnsignedCharArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IUnsignedCharData * {
  BeginAllowedTypes()
  AllowedType(spUnsignedCharData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IUnsignedIntArray * {
  BeginAllowedTypes()
  AllowedType(spUnsignedIntArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IUnsignedIntData * {
  BeginAllowedTypes()
  AllowedType(spUnsignedIntData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IUnsignedLongArray * {
  BeginAllowedTypes()
  AllowedType(spUnsignedLongArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IUnsignedLongData * {
  BeginAllowedTypes()
  AllowedType(spUnsignedLongData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IUnsignedShortArray * {
  BeginAllowedTypes()
  AllowedType(spUnsignedShortArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IUnsignedShortData * {
  BeginAllowedTypes()
  AllowedType(spUnsignedShortData)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IValueArray * {
  BeginAllowedTypes()
  AllowedType(spValueArray)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IWavefrontExporter * {
  BeginAllowedTypes()
  AllowedType(spWavefrontExporter)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IWavefrontImporter * {
  BeginAllowedTypes()
  AllowedType(spWavefrontImporter)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IVertexColorBaker * {
  BeginAllowedTypes()
  AllowedType(spVertexColorBaker)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IVisibilitySettings * {
  BeginAllowedTypes()
  AllowedType(spVisibilitySettings)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IString * {
  BeginAllowedTypes()
  AllowedType(spString)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IImpostorProcessor * {
  BeginAllowedTypes()
  AllowedType(spImpostorProcessor)
  EndAllowedTypes()
}
%typemap(in) SimplygonSDK::IImpostorSettings * {
  BeginAllowedTypes()
  AllowedType(spImpostorSettings)
  EndAllowedTypes()
}
#endif // defined(SWIGPYTHON)

#if defined(SWIGCSHARP)
// Map tuples to c# arrays
%include "arrays_csharp.i"
%apply float INPUT[]  {float *tuple}
%apply float OUTPUT[]  {float *dest_param}
%apply float OUTPUT[]  {float dest_param[3]}
%apply float OUTPUT[]  {float dest_param[16]}
%apply int INPUT[]  {int *tuple}
%apply int OUTPUT[]  {int *dest_param}
%apply bool INPUT[]  {bool *tuple}
%apply bool OUTPUT[]  {bool *dest_param}
%apply double INPUT[]  {double *tuple}
%apply double OUTPUT[]  {double *dest_param}
%apply long INPUT[]  {long *tuple}
%apply long OUTPUT[]  {long *dest_param}
%apply short INPUT[]  {short *tuple}
%apply short OUTPUT[]  {short *dest_param}
%apply unsigned char INPUT[]  {unsigned char *tuple}
%apply unsigned char OUTPUT[]  {unsigned char *dest_param}
%apply unsigned int INPUT[]  {unsigned int *tuple}
%apply unsigned int OUTPUT[]  {unsigned int *dest_param}
%apply unsigned long INPUT[]  {unsigned long *tuple}
%apply unsigned long OUTPUT[]  {unsigned long *dest_param}
%apply unsigned short INPUT[]  {unsigned short *tuple}
%apply unsigned short OUTPUT[]  {unsigned short *dest_param}

%include "stdint.i"
#endif // defined(SWIGCSHARP)