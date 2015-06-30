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
        exit_with_error("Failed to initialize: "+SDK.GetError(initval))
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

def MoveAssetDir(subDir):
    sourceDir = GetSDKAssetDirPath()+subDir
    targetDirectory = GetAssetDirPath()+subDir
    if os.path.exists(targetDirectory): #We need to remove existing dir first
        shutil.rmtree(targetDirectory)
    shutil.copytree(sourceDir, targetDirectory)

	
def GetAssetDirPath():
    path = currentDir+"/../../Assets/";
    if not os.path.exists(path):
        os.makedirs(path)
    return path
    
def GetAssetPath(subDir, assetName):
    return GetAssetDirPath()+subDir+"/"+assetName

def GetMatrix4x4FromIMatrix( src ):
    srcElements[16];
    src.GetElements(srcElements);
    return SDK.Matrix4x4(srcElements);

