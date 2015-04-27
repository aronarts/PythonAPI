# Simplygon Swig API Generator
==================================

## Introduction
This project generates a API that makes the Simplygon API accessible through python and c#.

## Requirements
- Swig (http://www.swig.org/)
- Python (https://www.python.org/downloads/), tested on 3.4 and 2.7

## Initial notes
- These bindings are work in progress.
- We are not necessarily experts on SWIG or the languages wrapped.
- If you have any opinions on how to do things better or pull requests it's greatly appreciated.

## Install instructions (Python)
- Install both SWIG and Python.
- Either you add them to the System path or you adjust the project file so that it points to the correct locations

## Getting started (Python)
- Set PYTHONPATH system variable to the root folder of Python.
- If you want to be able to build a debug version you need to compile python in debug mode and link to pythonXX_d.lib
- Right click SimplygonSDK.i and choose compile. This will generate the wrapper file.
- Compile the solution. This will generate _SimplygonSDK.pyd file and copy that and SimplygonSDK.py and copy both to the examples folder.
- Open one of the example scripts in IDLE (comes with Python) and run it.

## Notes (Python)
- The API is not completely wrapped and there is a fair amount of typemaps and extends that needs to be added.
- All inheritances needs to be replicated in SimplygonTypeMaps.i
- In order to allow downcasting in Python all parent classes needs to be extended with AsXXX functions in SimplygonExtensions.i
- A lot of return by reference parameters needs to mapped and handled in type maps.

## Install instructions (C#)
- Install SWIG
- Either add SWIG to the system path or update the visual studio project so it can be found
- Install Simplygon 6.2.520. If you use a different version, make sure you overwrite SimplygonSDK.h with the one from the Simplygon install directory
- Install your Simplygon License

## Building the C# Bindings (C#)
- Load APIGenerator.sln
- Force compile SimplygonSDK.i in the SimplygonCLRRuntime project to regenerate simplygon_swig.cpp and the c# wrappers
- Now build all projects and the
- SimplygonCLRRuntime.dll is the C dll that forwards calls to the API
- SimplygonSDKCLR.dll is the C# native layer of wrapper classes

## Running the examples (C#)
- In the examples directory there is a C# 
- After building the bindings you should be able to build and run the examples

## Notes (C#)
- The wrapping is currently incomplete.
- The key complication now is based on Simplygon using smart pointers meaning that each type exist both in its standard type and smart pointer type.
- In order to support using smart pointers where the standard type is required there are explicit type maps in the bottom of SimplygonExtensions.i adding implicit cast operators
- Note that inheritance is lost on the smart pointers meaning you potentially need to add cast operators for all parent classes of the smart pointers contained type
- If you need a temporary solution you can always call the __deref__() method on the smart pointer to get its contained pointer.
- The implemented casting are all done manually based on the Simplygon SDK examples ported. It is likely you will need to add more.
- In the future this should ideally be automatically generated or all smart pointers returned should be automatically dereferenced and held on to by C# instead.
- Enums are passed as int our uint in the Simplygon API requring type casting. Hopefully we can get this corrected in the SimplygonSDK.h header in the future.
- Smart pointer types have no inheritance there needs to be explicit casting to reach a parent class. It's implemented using the Utils.SimplygonCast<> function.
- Deinitialization of SimplygonSDK is currently not supported because it needs to be released after all references to any simplygon object and the C# garbage collector is non-deterministic. If this is important every Simplygon object need to be initiated in a using statement to guarantee it's released when it goes out of scope.

## Unity (C#)
- The C# wrappers have been successfully run in the Unity 5.0 editor for 64bit and it should work on different versions and platforms.
- To use them, drag both SimplygonCLRRuntime.dll and SimplygonSDKCLR.dll to Assets/Editor in the editor project. Also add Utils.cs if you want the cast operator
- There are sometimes compatibility issues with third party clr modules in unity and if everything fails you should be able to copy the raw cs files from SimplygonSDKCLR and let unity compile them for you.



