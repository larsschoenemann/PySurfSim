# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Ultra-precision surface simulation in python 

Copyright (C) 2022  Lars Schönemann
Leibniz Institut für Werkstofforientierte Technologien IWT, Bremen, Germany
"""
from importlib.metadata import version, PackageNotFoundError

from .apply_mesh_tool_to_workpiece import apply_mesh_tool_to_workpiece
from .combine_surface import combine_surface
from .export_surface import export_surface
from .gen_surface_mesh import gen_surface_mesh
from .gen_tool_mesh_with_offsets import gen_tool_mesh_with_offsets
from .helpers import pairwise, round_up_to_base, default_parameters
from .mesh_tool_fly_cut import MeshToolFlyCut
from .slice_surface import slice_surface

# compatability imports (uncomment these to mimic legacy interface)
# from .combine_surface import combine_surface as combineSurface  # pylint: disable=W0404
# from .apply_mesh_tool_to_workpiece import apply_mesh_tool_to_workpiece as applyMeshToolToWorkpiece  # pylint: disable=W0404
# from .export_surface import export_surface as exportSurface  # pylint: disable=W0404
# from .gen_surface_mesh import gen_surface_mesh as genSurfaceMesh  # pylint: disable=W0404
# from .gen_tool_mesh_with_offsets import gen_tool_mesh_with_offsets as genToolMeshWithOffsets  # pylint: disable=W0404
# from .mesh_tool_fly_cut import MeshToolFlyCut as meshToolFlyCut  # pylint: disable=W0404
# from .slice_surface import slice_surface as sliceSurface  # pylint: disable=W0404


try:
    __version__ = version('PySurfSim')
except PackageNotFoundError:
    # package is not installed
    pass
