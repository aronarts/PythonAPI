# Simplygon Python API Generator
==================================

## Introduction
This project generates a API that makes the Simplygon API accesible through python.

## Requirements
- Swig (http://www.swig.org/)
- Python (https://www.python.org/downloads/), tested on 3.4


## Install instructions
- Install both SWIG and Python.
- Either you add them to the System path or you adjust the project file so that it points to the correct locations

## Getting started
- If you want to be able to build a debug version you need to compile python in debug mode and link to pythonXX_d.lib
- Right click SimplygonSDK.i and choose compile. This will generate the wrapper file.
- Compile the solution. This will generate _SimplygonSDK.pyd file and copy that and SimplygonSDK.py and copy both to the examples folder.
- Open one of the example scripts in IDLE (comes with Python) and run it.

## Notes
- The API is not completely wrapped and there is a fair amount of typemaps and extends that needs to be added.
- All inheritances needs to be replicated in SimplygonTypeMaps.i
- In order to allow downcasting in Python all parent classes needs to be extended with AsXXX functions in SimplygonExtensions.i
- A lot of return by reference parameters needs to mapped and handled in type maps.

