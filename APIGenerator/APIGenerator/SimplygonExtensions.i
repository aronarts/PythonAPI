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
