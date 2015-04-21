%module SimplygonSDK

%{
#include "Logger.h"
#include "SimplygonSDK.h"
#include "SimplygonSDKLoader.h"

using namespace SimplygonSDK; 

namespace SimplygonSDK {


	/// Adds a location to look for the DLL in. This method must be called before calling Initialize()
	extern void AddSearchPath( const char *search_path );

	/// Clears the additional search locations to look for the DLL in.
	extern void ClearAdditionalSearchPaths();

	/// Loads and initializes the SDK
	extern int Initialize(LPCTSTR SDKPath  , LPCTSTR LicenseDataText  );

	/// Deinitializes the SDK, releases the DLL and all allocated memory
	extern void Deinitialize();

	/// Retrieves the error string of the error code.
	extern LPCTSTR GetError( int error_code );

	/// Retrieves the license system log, for when initializing
	extern int PollLog( LPTSTR dest , int max_len_dest );

	/// Run the license wizard process, to ease license integration
	extern int RunLicenseWizard( LPCTSTR batch_file );

	extern ISimplygonSDK *GetSDK();
#if defined(SWIGPYTHON)
	// Python specific stuff
	class error_handler : public SimplygonSDK::rerrorhandler
	{
	public:
		virtual void HandleError(
			IObject *object,
			const char *interfacename,
			const char *methodname,
			rid errortype,
			const char *errortext
			)
		{
			char tmp[1024];

			sprintf_s(tmp, 1024, "A SimplygonSDK error occured!\n");
			sprintf_s(tmp, 1024, "%s\tInterface: %s (%p)\n", tmp, interfacename, object);
			sprintf_s(tmp, 1024, "%s\tMethod: %s\n", tmp, methodname);
			sprintf_s(tmp, 1024, "%s\tError Type: %d\n", tmp, errortype);
			sprintf_s(tmp, 1024, "%s\tError Description: %s\n", tmp, errortext);
			PyErr_SetString(PyExc_ValueError,tmp);
		}
	} eh;

	extern void InitErrorhandling()
	{
		GetSDK()->SetErrorHandler(&eh);
	}
}
#endif // defined(SWIGPYTHON)

#if defined(SWIGCSHARP)
	// Csharp speficic stuff
	/*class error_handler : public SimplygonSDK::rerrorhandler
	{
	public:
		virtual void HandleError(
			IObject *object,
			const char *interfacename,
			const char *methodname,
			rid errortype,
			const char *errortext
			)
		{
			char tmp[1024];

			sprintf_s(tmp, 1024, "A SimplygonSDK error occured!\n");
			sprintf_s(tmp, 1024, "%s\tInterface: %s (%p)\n", tmp, interfacename, object);
			sprintf_s(tmp, 1024, "%s\tMethod: %s\n", tmp, methodname);
			sprintf_s(tmp, 1024, "%s\tError Type: %d\n", tmp, errortype);
			sprintf_s(tmp, 1024, "%s\tError Description: %s\n", tmp, errortext);
			PyErr_SetString(PyExc_ValueError,tmp);
		}
	} eh;*/

	extern void InitErrorhandling()
	{
		//GetSDK()->SetErrorHandler(&eh);
	}
}
#endif // defined(SWIGCSHARP)

%}

%include "SimplygonTypemaps.i"

%include "SimplygonIgnores.i"

%include "SimplygonExtensions.i"

%include "SimplygonSDK.h"

%include "SimplygonTemplates.i"

%include "SimplygonLoader.i"
