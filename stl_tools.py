from stl import mesh
import numpy as np


def get_uniq_pc(fname):
    #return unique point cloud taking points from each triangle

    vbmesh = mesh.Mesh.from_file(fname)
    allvbmesh = np.concatenate((vbmesh.v0, vbmesh.v1, vbmesh.v2), axis=0)
    mesh_uniq = np.unique(allvbmesh, axis=0)
    return mesh_uniq


def get_mid_array(mesh_uniq, thickness, axis):

    if axis == 'x' or axis == 'X':
        axisnum = 0
    if axis == 'y' or axis == 'Y':
        axisnum = 1
    if axis == 'z' or axis == 'Z':
        axisnum = 2

    zmin = min(mesh_uniq[:, axisnum])
    zmax = max(mesh_uniq[:, axisnum])
    mid = (zmax - zmin) / 2 + zmin
    count = 0
    for i in range(len(mesh_uniq)):
        if (mesh_uniq[i, axisnum] <= mid + (thickness / 2)
                and mesh_uniq[i, axisnum] >= mid - (thickness / 2)):
            count += 1

    midarray = np.zeros((count, 3))
    a = 0
    for i in range(len(mesh_uniq)):
        if (mesh_uniq[i, axisnum] <= mid + (thickness / 2)
                and mesh_uniq[i, axisnum] >= mid - (thickness / 2)):
            midarray[a] = mesh_uniq[i]
            a += 1

    return midarray
