# PySurfSim

Framework for ultra-precision surface simulation.

## Description

This framework allows for the numerical simulation of nanoscale surfaces
generated by ultra-precision cutting processes.

### Functions

`gen_surface_mesh`: generate a surface mesh of equal height using lateral
    dimensions together with a resolution or a fixed number of points/pixels  
`apply_mesh_tool_to_workpiece`: apply a meshed tool function to a workpiece  
`slice_surface`: divide surface mesh into smaller patches  
`combine_surface`: combine patches into larger surface mesh  

### Classes

`MeshToolFlyCut`: class that provides the tool functions `get_z` and
`footprint` for a flycutting tool

## Usage

 1. Generate a new surface mesh using `gen_surface_mesh` or take a previously
    generated surface mesh as input
 2. Define tool apex positions as a mesh
 3. [Optional]: Divide surface mesh into smaller patches for parallel
    processing (e.g. via `joblib`) by using `slice_surface`
 4. Generate a tool object based on a tool class (e.g. `MeshToolFlyCut`) and
    apply it to the surface mesh at the defined tool positions using
    `apply_mesh_tool_to_workpiece`
 5. [Optional]: Combine previously sliced surfaces by using `combine_surface`

## Contact
Dr.-Ing. Lars Schönemann  
Germany  
lars.schoenemann@gmx.de

formerly  
Leibniz-Institute for Materials Engineering IWT  
Laboratory for Precision Machining LFM  
Badgasteiner Straße 3  
28359 Bremen  
