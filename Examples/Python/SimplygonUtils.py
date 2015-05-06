import SimplygonSDK as SDK
import os, sys, shutil, ctypes.wintypes
currentDir = os.path.dirname(os.path.realpath(__file__))
def GetSDK():
    return SDK.GetSDK()

def exit_with_error(errorstr):
    raise RuntimeError(errorstr)

def InitExample():
    SDK.AddSearchPath( "..\\Build\\")
    SDK.AddSearchPath( "..\\..\\Build\\")
    SDK.AddSearchPath( "..\\..\\..\\Build\\")
    initval = SDK.Initialize()	
    if(initval != SDK.SG_ERROR_NOERROR):
        exit_with_error("Failed to initialize: "+SDK.GetError(initVal))
    print("Simplygon version: "+GetSDK().GetVersion()+" is loaded")


def DeinitExample():
    #Deinitialize the SDK
    SDK.Deinitialize()

def GetOutputPath(dir, assetName):
    outputDirectory = currentDir+"/Output/"+dir
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
    return outputDirectory+"/"+assetName

def GetSDKAssetDirPath():
    CSIDL_PERSONAL= 5
    SHGFP_TYPE_CURRENT= 0
    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
    path = buf.value+"/SimplygonSDK/SourceCode/Assets/"
    if not os.path.exists(path):
        raise Exception('Cannot find the Simplygon SDK assets. Is Simplygon correctly installed and the Examples extracted in Documents/SimplygonSDK?')
    return path

def GetSDKAssetPath(subDir, assetName):
    return GetSDKAssetDirPath()+subDir+"/"+assetName

def MoveAsset(subDir, assetName):
    sourceFile = GetSDKAssetPath(subDir,assetName)
    targetDirectory = GetAssetDirPath()+subDir
    if not os.path.exists(targetDirectory):
        os.makedirs(targetDirectory)
    targetFile = GetAssetPath(subDir, assetName);
    shutil.copyfile(sourceFile, targetFile)

def GetAssetDirPath():
    path = currentDir+"/../../Assets/";
    if not os.path.exists(path):
        os.makedirs(path)
    return path
    
def GetAssetPath(subDir, assetName):
    return GetAssetDirPath()+subDir+"/"+assetName
 

"""
def MoveAsset(assetName, assetDirPath, targetDirectory):

    std::vector<std::basic_string<TCHAR>> folders = stringSplit(currentWorkingDirectory.c_str(),_T('\\'));

    //look for 
    std::vector<std::basic_string<TCHAR>>::iterator it;
    for ( it=folders.begin() ; it < folders.end(); it++ )
            {
            pathToAssetsFolder+=*it;
            pathToAssetsFolder+=_T("\\");
            if(*it == _T("Build") )
                    {
                    break;
                    }
            }

    pathToAssetsFolder+=_T("..\\Assets\\");
    if(assetDirPath != _T(""))
            pathToAssetsFolder+=assetDirPath;
    pathToAssetsFolder+=assetName;
    currentWorkingDirectory+=assetName;


CopyFile(pathToAssetsFolder.c_str(),currentWorkingDirectory.c_str(), FALSE);




//src path should be relative to the assets folder
void MoveDirToExecutablePath(std::basic_string<TCHAR> dirPathSrc, std::basic_string<TCHAR> dirPathDest)
	{


		std::basic_string<TCHAR> pathToAssetsFolder;
		std::basic_string<TCHAR> currentWorkingDirectory = GetExecutablePath();
		std::basic_string<TCHAR> destinationPath;

		
		SetCurrentDirectory(currentWorkingDirectory.c_str());
		//if assetDirPath is empty use currentworking directory to move to assets dir

		std::vector<std::basic_string<TCHAR>> folders_src = stringSplit(currentWorkingDirectory.c_str(),_T('\\'));

		std::vector<std::basic_string<TCHAR>> folders_dest = stringSplit(currentWorkingDirectory.c_str(),_T('\\'));

		folders_src.push_back(_T(".."));
		folders_src.push_back(_T(".."));

		
			{
			std::vector<std::basic_string<TCHAR>>::reverse_iterator it;
			std::vector<std::string> reverse_path;
			int remove_next_counter = 0;

			for ( it = folders_src.rbegin() ; it < folders_src.rend(); it++ )
				{
				if(*it == _T("..") )
					{
					remove_next_counter++;
					}
				else if(remove_next_counter > 0 )
					{
					remove_next_counter--;
					}
				else
					{
					reverse_path.push_back(*it);
					//pathToAssetsFolder+=*it;
					//pathToAssetsFolder+=_T("\\");
					}
				}

			for(int i = (int)reverse_path.size() - 1 ; i >= 0 ; --i)
				{
				pathToAssetsFolder += reverse_path[i];
				pathToAssetsFolder += _T("\\");
				}
			}

			{
			std::vector<std::basic_string<TCHAR>>::reverse_iterator it;
			std::vector<std::string> reverse_path;
			int remove_next_counter = 0;

			for ( it = folders_dest.rbegin() ; it < folders_dest.rend(); it++ )
				{
				if(*it == _T("..") )
					{
					remove_next_counter++;
					}
				else if(remove_next_counter > 0 )
					{
					remove_next_counter--;
					}
				else
					{
					reverse_path.push_back(*it);
					//pathToAssetsFolder+=*it;
					//pathToAssetsFolder+=_T("\\");
					}
				}

			for(int i = (int)reverse_path.size() - 1 ; i >= 0 ; --i)
				{
				destinationPath += reverse_path[i];
				destinationPath += _T("\\");
				}
			}

			pathToAssetsFolder+=_T("Assets\\");
			pathToAssetsFolder+=dirPathSrc;

			destinationPath += dirPathDest;
		
			
		//MoveFileEx(pathToAssetsFolder.c_str(),currentWorkingDirectory.c_str(), MOVEFILE_COPY_ALLOWED);

		//printf("assets folder: %s\n", pathToAssetsFolder.c_str());
		//printf("output folder: %s \n", destinationPath.c_str());

		/*printf("Initialized \n");*/

		HWND handle = NULL;
		//IsWindow(handle);
		
		SHFILEOPSTRUCT  fileOpObj;
		fileOpObj.hwnd = handle;
		pathToAssetsFolder += '\0';
		destinationPath += '\0';

		LPCTSTR c01 = pathToAssetsFolder.c_str();
		LPCTSTR c1 = destinationPath.c_str();

		//check if destination path already exits delete folder

		
		

		
		fileOpObj.pFrom = pathToAssetsFolder.c_str();
		fileOpObj.pTo = destinationPath.c_str();



		fileOpObj.wFunc = FO_COPY;
		fileOpObj.fFlags = FOF_MULTIDESTFILES | FOF_SILENT;

		SHFileOperation(&fileOpObj);
	


	}





std::vector<std::basic_string<TCHAR>> stringSplit(LPCTSTR source, TCHAR delim)
	{
		std::basic_string<TCHAR> tempString(source);
		//std::basic_string<TCHAR> delimStr(delim);
		std::basic_string<TCHAR> buffer;
		std::stringstream stringStream(tempString);
		std::vector<std::basic_string<TCHAR>> stringCollection;

		
		while(std::getline(stringStream,buffer,delim))
			{
			if(buffer != _T(""))
				stringCollection.push_back(buffer);
			}

		return stringCollection;
		
	}

bool contains(std::vector<std::basic_string<TCHAR>> strCollection, std::basic_string<TCHAR> val)
	{
	 std::vector<std::basic_string<TCHAR>>::iterator it;
	for ( it=strCollection.begin() ; it < strCollection.end(); it++ )
		{
			if(*it == val )
				return true;
		}

	return false;
	}

"""
