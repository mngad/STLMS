from stl import mesh
import numpy as np


def get_uniq_pc(fname):
    #return unique point cloud taking points from each triangle

    fullmesh = mesh.Mesh.from_file(fname)
    allmesh = np.concatenate((fullmesh.v0, fullmesh.v1, fullmesh.v2), axis=0)
    mesh_uniq = np.unique(allmesh, axis=0)
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
    if(thickness == "all"):
        thickness = zmax
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

#reurns a list of 2 values, minimum and maximum of an axis
def get_extent(mesh_uniq, axis):
    extent = []
    extent.append(mesh_uniq[0, axis])
    extent.append(mesh_uniq[0, axis])


    for i in range(len(mesh_uniq)):
        if ( mesh_uniq[i,axis] < extent[0]): extent[0] = mesh_uniq[i,axis]
        if ( mesh_uniq[i,axis] > extent[1]): extent[1] = mesh_uniq[i,axis]

    return extent

#returns origin of cube
def boundingorigin(mesh_un):

    origin = (get_extent(mesh_un, 0)[0],
        get_extent(mesh_un, 1)[0],
        get_extent(mesh_un, 2)[0])

    return origin

def boundingsize(mesh_un):
    origin = (get_extent(mesh_un, 0)[0],
        get_extent(mesh_un, 1)[0],
        get_extent(mesh_un, 2)[0])

    size = (get_extent(mesh_un, 0)[1] - origin[0],
        get_extent(mesh_un, 1)[1] - origin[1],
        get_extent(mesh_un, 2)[1] - origin[2])

    return size

#returns mesh points from left or right half
# which_half = bool of 0 = left, 1 = right
def get_half_points(mesh_uniq, which_half, extent, axis):


    halfway_val = (extent[1] + extent[0]) / 2

    a = 0

    for i in range(len(mesh_uniq)):
        if(which_half == 0):
            if(mesh_uniq[i, axis] < halfway_val):
                a += 1
        else:
            if(mesh_uniq[i, axis] > halfway_val):
                a += 1

    half_mesh_array = np.zeros((a, 3))

    count = 0
    for i in range(len(mesh_uniq)):
        # print("a = " + str(a) + ", i = " + str(i))
        if(which_half == 0):
            if(mesh_uniq[i, axis] < halfway_val):
                half_mesh_array[count] = mesh_uniq[i]
                count += 1
        else:
            if(mesh_uniq[i, axis] > halfway_val):
                half_mesh_array[count] = mesh_uniq[i]
                count += 1


    return half_mesh_array
