import os
import sys
import stl_uni as su




if __name__ == "__main__":
    os.chdir(sys.argv[1])
    for filename in sorted(os.listdir(sys.argv[1])):
        if filename.endswith(".stl"):

            vbmesh_un = su.get_uniq_pc(filename)
            midarray, centreX, centreY, mid, x, y, z = measure_vb(
                vbmesh_un, filename[:-4])
