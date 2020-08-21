from stl import mesh
import numpy as np


def reposition(mesh):
    # takes the mesh and makes it start at 0, 0, 0 so all mesh positions are
    # positive
    #

    x_extent = get_extent(mesh, 0)
    y_extent = get_extent(mesh, 1)
    z_extent = get_extent(mesh, 2)

    xmin = min(x_extent)
    ymin = min(y_extent)
    zmin = min(z_extent)

    return_array = np.zeros((len(mesh), 3))

    count = 0
    for i in range(len(mesh)):
        return_array[count][0] = mesh[i][0] + abs(xmin)
        count += 1

    count = 0
    for i in range(len(mesh)):
        return_array[count][1] = mesh[i][1] + abs(ymin)
        count += 1

    count = 0
    for i in range(len(mesh)):
        return_array[count][2] = mesh[i][2] + abs(zmin)
        count += 1

    return return_array


def get_uniq_pc(fname):
    # return unique point cloud taking points from each triangle

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


def get_extent(mesh_uniq, axis):
    # reurns a list of 2 values, minimum and maximum of an axis

    extent = []
    extent.append(mesh_uniq[0, axis])
    extent.append(mesh_uniq[0, axis])

    for i in range(len(mesh_uniq)):
        if (mesh_uniq[i, axis] < extent[0]):
            extent[0] = mesh_uniq[i, axis]
        if (mesh_uniq[i, axis] > extent[1]):
            extent[1] = mesh_uniq[i, axis]

    return extent


def boundingorigin(mesh_un):
    # returns origin of cube

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


def get_half_points(mesh_uniq, which_half, extent, axis):
    # returns mesh points from left or right half
    # which_half = bool of 0 = left, 1 = right

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


def get_condyle(mesh_uniq, extent_y, half):
    # Takes half the points (ie. roughly one condyle) measures some percentage
    # from the back to find the condyle width

    if(half == 0):
        length = abs(extent_y[1] - extent_y[0])
        instep_point = (length * 0.15) + extent_y[0]

        a = 0

        for i in range(len(mesh_uniq)):
            if(mesh_uniq[i, 1] < instep_point):
                a += 1

        temp_mesh_array = np.zeros((a, 3))

        count = 0
        for i in range(len(mesh_uniq)):
            if(mesh_uniq[i, 1] < instep_point):
                temp_mesh_array[count] = mesh_uniq[i]
                count += 1

        inside_condyle_bound = get_extent(temp_mesh_array, 0)[0]
        b = 0

        for i in range(len(mesh_uniq)):
            if(mesh_uniq[i, 0] > inside_condyle_bound):
                b += 1

        FW_mesh_array = np.zeros((b, 3))

        count = 0
        for i in range(len(mesh_uniq)):
            if(mesh_uniq[i, 0] > inside_condyle_bound):
                FW_mesh_array[count] = mesh_uniq[i]
                count += 1

        return FW_mesh_array

    if(half == 1):
        length = abs(extent_y[1] - extent_y[0])
        instep_point = (length * 0.15) + extent_y[0]
        a = 0

        for i in range(len(mesh_uniq)):
            if(mesh_uniq[i, 1] < instep_point):
                a += 1

        temp_mesh_array = np.zeros((a, 3))

        count = 0
        for i in range(len(mesh_uniq)):
            if(mesh_uniq[i, 1] < instep_point):
                temp_mesh_array[count] = mesh_uniq[i]
                count += 1
        inside_condyle_bound = get_extent(temp_mesh_array, 0)[1]
        b = 0

        for i in range(len(mesh_uniq)):
            if(mesh_uniq[i, 0] < inside_condyle_bound):
                b += 1

        FW_mesh_array = np.zeros((b, 3))

        count = 0
        for i in range(len(mesh_uniq)):
            if(mesh_uniq[i, 0] < inside_condyle_bound):
                FW_mesh_array[count] = mesh_uniq[i]
                count += 1

        return FW_mesh_array


def split_into_thirds(mesh, axis):
    # Split mesh into thirds along a specific axis

    mesh_extent = get_extent(mesh, axis)
    mesh_third = abs(mesh_extent[1] - mesh_extent[0]) / 3
    b = 0
    for i in range(len(mesh)):
        if(mesh[i, axis] < mesh_extent[0] + mesh_third):
            b += 1

    mesh_array_one = np.zeros((b, 3))

    count = 0
    for i in range(len(mesh)):
        if(mesh[i, axis] < mesh_extent[0] + mesh_third):
            mesh_array_one[count] = mesh[i]
            count += 1

    b = 0
    for i in range(len(mesh)):
        if(mesh[i, axis] < mesh_extent[0] + (mesh_third*2) and
           mesh[i, axis] > mesh_extent[0] + (mesh_third * 1)):
            b += 1

    mesh_array_two = np.zeros((b, 3))

    count = 0
    for i in range(len(mesh)):
        if(mesh[i, axis] < mesh_extent[0] + (mesh_third * 2) and
           mesh[i, axis] > mesh_extent[0] + (mesh_third * 1)):
            mesh_array_two[count] = mesh[i]
            count += 1

    b = 0
    for i in range(len(mesh)):
        if(mesh[i, axis] < mesh_extent[0] + (mesh_third * 3) and
           mesh[i, axis] > mesh_extent[0] + (mesh_third * 2)):
            b += 1

    mesh_array_three = np.zeros((b, 3))

    count = 0
    for i in range(len(mesh)):
        if(mesh[i, axis] < mesh_extent[0] + (mesh_third * 3) and
           mesh[i, axis] > mesh_extent[0] + (mesh_third * 2)):
            mesh_array_three[count] = mesh[i]
            count += 1

    mesharray_thirds = []
    mesharray_thirds.append(mesh_array_one)
    mesharray_thirds.append(mesh_array_two)
    mesharray_thirds.append(mesh_array_three)

    return mesharray_thirds


