#if defined(SWIGCSHARP)
typedef char* LPCTSTR;
typedef char* LPTSTR;
	/*%typemap(in) LPCTSTR, LPTSTR {
	   $1 = (const char**)($input);
	}
	
	%typemap(out) LPCTSTR, LPTSTR{
	   $result = (const char**)($1);	
	} */
#endif // defined(SWIGCSHARP)

namespace SimplygonSDK {
	

	// Declare types that can be converted

#if defined(SWIGPYTHON)
	%typemap(in) LPCTSTR, LPTSTR {
	   $1 = PyString_AsString($input);
	}
	
	%typemap(out) LPCTSTR, LPTSTR{
	   $result = PyString_FromString($1);	
	} 
#endif // defined(SWIGPYTHON)




	/// Adds a location to look for the DLL in. This method must be called before calling Initialize()
	extern void AddSearchPath( const char * search_path );

	/// Clears the additional search locations to look for the DLL in.
	extern void ClearAdditionalSearchPaths();

	/// Loads and initializes the SDK
	extern int Initialize(LPCTSTR SDKPath = NULL, LPCTSTR LicenseDataText = NULL);

	/// Deinitializes the SDK, releases the DLL and all allocated memory
	extern void Deinitialize();

	/// Retrieves the error string of the error code.
	extern LPCTSTR GetError( int error_code );

	/// Retrieves the license system log, for when initializing
	extern int PollLog( LPTSTR dest , int max_len_dest );

	/// Run the license wizard process, to ease license integration
	extern int RunLicenseWizard( LPCTSTR batch_file);

	extern ISimplygonSDK *GetSDK();

	extern void InitErrorhandling();

}