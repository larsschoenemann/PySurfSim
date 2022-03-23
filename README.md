# PySurfSim
Framework for ultra-precision surface simulation.
## Description
This framework allows for the numerical simulation of nanoscale surfaces generated by ultra-precision cutting processes.

### Functions
`genSurfaceMesh`: generate a surface mesh of equal height using lateral dimensions together with a resolution or a fixed number of points/pixels  
`applyMeshToolToWorkpiece`: apply a meshed tool function to a workpiece  
`sliceSurface`: divide surface mesh into smaller patches  
`combineSurface`: combine patches into larger surface mesh  
`meshToolFlyCut`: class that provides the tool functions `getZ` and `footprint` for a flycutting tool

## Usage

 1. Generate a new surface mesh using `genSurfaceMesh` or take a previously generated surface mesh as input
 2. Define tool apex positions as a mesh
 3. [Optional]: Divide surface mesh into smaller patches for parallel processing (e.g. via `joblib`) by using `sliceSurface`
 4. Apply tool function (e.g. `meshToolFlyCut`) to the surface mesh at the defined tool positions using `applyMeshToolToWorkpiece`
 5. [Optional]: Combine previously sliced surfaces by using `combineSurface`


## Contact
Leibniz-Institute for Materials Engineering IWT  
Laboratory for Precision Machining LFM  
Dr.-Ing. Lars Sch�nemann  
Badgasteiner Stra�e 3  
28359 Bremen  
Germany  
schoenemann@iwt.uni-bremen.de
