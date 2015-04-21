using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using SimplygonSDKCLR;

namespace Example
{
    public class Example
    {
        static public ISimplygonSDK InitExample()
        {
           	// Initiate
	        SimplygonSDK.AddSearchPath( "..\\Build\\");
	        SimplygonSDK.AddSearchPath( "..\\..\\Build\\");
	        SimplygonSDK.AddSearchPath( "..\\..\\..\\Build\\");
	        int initval = SimplygonSDK.Initialize();
	        if( initval != (int)(ErrorCodes.SG_ERROR_NOERROR) )
		    {
		        Console.WriteLine("Failed to initialize");
                return null;
		    }
            //sg->SetErrorHandler(&eh);
            return SimplygonSDK.GetSDK();
        }
    }
}
