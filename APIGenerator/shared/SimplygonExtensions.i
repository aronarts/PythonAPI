//Adding operator[] to all the rdata types
%extend SimplygonSDK::rdata<IBoolData>
{
    IBoolData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<ICharData>
{
    ICharData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IDoubleData>
{
    IDoubleData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IFloatData>
{
    IFloatData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IIntData>
{
    IIntData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<ILongData>
{
    ILongData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IRealData>
{
    IRealData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IRidData>
{
    IRidData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IShortData>
{
    IShortData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IUnsignedCharData>
{
    IUnsignedCharData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IUnsignedIntData>
{
    IUnsignedIntData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IUnsignedLongData>
{
    IUnsignedLongData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IUnsignedShortData>
{
    IUnsignedShortData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IRcharData>
{
    IRcharData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}
%extend SimplygonSDK::rdata<IRhandleData>
{
    IRhandleData::value_type __getitem__(unsigned int i) 
	{
        return (*($self))[i];
    }
}

//////////////////////////////////////////////////
// The following extensions enables downcasting of objects in Python. Each parent class needs to be extended so that they can be
// cast into deriving classes at the whim of the user.
////////////////////////////////////////////////////
%extend SimplygonSDK::CountedPointer<ISceneNode>
{
    SimplygonSDK::CountedPointer<ISceneMesh> AsSceneMesh() 
	{
        return CountedPointer<ISceneMesh>(ISceneMesh::SafeCast(*$self));
    }

	SimplygonSDK::CountedPointer<ISceneLodGroup> AsSceneLodGroup() 
	{
        return CountedPointer<ISceneLodGroup>(ISceneLodGroup::SafeCast(*$self));
    }
	
	SimplygonSDK::CountedPointer<ISceneBone> AsSceneBone() 
	{
        return CountedPointer<ISceneBone>(ISceneBone::SafeCast(*$self));
    }
}
#if defined(SWIGCSHARP)
// These are cast operators for c#
%typemap(cscode) SimplygonSDK::IGeometryData %{
	public static implicit operator IGeometryData(spGeometryData d) {
		return d.__deref__();
	}
%}
%typemap(cscode) SimplygonSDK::ISceneNode %{
	public static implicit operator ISceneNode(spSceneNode d) {
		return d.__deref__();
	}
	public static implicit operator ISceneNode(spSceneMesh d) {
		return d.__deref__();
	}
	public static implicit operator ISceneNode(spSceneBone d) {
		return d.__deref__();
	}
%}
%typemap(cscode) SimplygonSDK::ISceneMesh %{
	public static implicit operator ISceneMesh(spSceneMesh d) {
		return d.__deref__();
	}
%}
%typemap(cscode) SimplygonSDK::IMaterialTable %{
	public static implicit operator IMaterialTable(spMaterialTable d) {
		return d.__deref__();
	}
%}
%typemap(cscode) SimplygonSDK::IMaterial %{
	public static implicit operator IMaterial(spMaterial d) {
		return d.__deref__();
	}
%}
%typemap(cscode) SimplygonSDK::IMappingImage %{
	public static implicit operator IMappingImage(spMappingImage d) {
		return d.__deref__();
	}
%}
%typemap(cscode) SimplygonSDK::ISceneBone %{
	public static implicit operator ISceneBone(spSceneBone d) {
		return d.__deref__();
	}
%}

%typemap(cscode) SimplygonSDK::IMatrix4x4 %{
	public static implicit operator IMatrix4x4(spMatrix4x4 d) {
		return d.__deref__();
	}
%}


%typemap(csattributes) SimplygonSDK::FeatureFlags "[Flags]"
%typemap(csimports) SimplygonSDK::FeatureFlags
%{
using System;
%}

#endif // defined(SWIGCSHARP)