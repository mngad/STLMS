from stl import mesh
import numpy as np

def get_uniq_pc(fname):
    #return unique point cloud taking points from each triangle

    vbmesh = mesh.Mesh.from_file(fname)
    allvbmesh = np.concatenate((vbmesh.v0, vbmesh.v1, vbmesh.v2), axis=0)
    vbmesh_un = np.unique(allvbmesh, axis=0)
    return vbmesh_un
