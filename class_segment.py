import open3d as o3d
import numpy as np
import os
from plyfile import PlyData, PlyElement
import pandas as pd
import sys
pointcloud_obj_path=sys.argv[1] #lab
dir='./results/class_segment/'+sys.argv[1]
pointcloud_npy_path='./results/mmd3d/'+pointcloud_obj_path+'/'+pointcloud_obj_path+'.npy'
pointcloud_obj_path='./results/mmd3d/'+pointcloud_obj_path+'/'+pointcloud_obj_path+'_pred.obj'
pointclouds_origin = np.load(pointcloud_npy_path)
pointclouds=np.array([line.split()[:][1:7] for line in open(pointcloud_obj_path)],dtype='float')

cabinet=[] #0
floor=[] #1
wall=[] #2
other=[] #3
desk=[] #4
window=[] #5
door=[] #6
table=[] #7
chair=[] #8
sofa=[] #9
bookshelf=[] #10



b = np.array([1 , 1, 1,255, 255, 255])

i=0 #index of point
for pointcloud in pointclouds:   
    if (pointcloud[3:6]==[188.,189.,34.]).all(): #ok
        chair.append(pointclouds_origin[i][0:6]/b)
    elif (pointcloud[3:6]==[255.,152.,150.]).all(): #ok
        table.append(pointclouds_origin[i][0:6]/b)
    elif (pointcloud[3:6]==[31.,119.,180.]).all(): #ok
        cabinet.append(pointclouds_origin[i][0:6]/b)
    elif (pointcloud[3:6]==[196.,176.,221.]).all(): #ok
        window.append(pointclouds_origin[i][0:6]/b)
    elif (pointcloud[3:6]==[152.,223.,138.]).all(): #ok
        floor.append(pointclouds_origin[i][0:6]/b)
    elif (pointcloud[3:6]==[174.,199.,232.]).all(): #ok
        wall.append(pointclouds_origin[i][0:6]/b)
    elif (pointcloud[3:6]==[214.,39.,40.]).all(): #OK
        door.append(pointclouds_origin[i][0:6]/b)
    elif (pointcloud[3:6]==[82.,84.,163.]).all(): #OK
        other.append(pointclouds_origin[i][0:6]/b)
    elif (pointcloud[3:6]==[247.,182.,210.]).all(): #ok
        desk.append(pointclouds_origin[i][0:6]/b)
    elif (pointcloud[3:6]==[140.,86.,75]).all(): #
        sofa.append(pointclouds_origin[i][0:6]/b)
    elif (pointcloud[3:6]==[148.,103.,189.]).all(): #
        bookshelf.append(pointclouds_origin[i][0:6]/b)
    i+=1

# for pointcloud in pointclouds:   
#     if (pointcloud[3:6]==[255.,0.,0.]).all():
#         chair.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[170.,120.,200.]).all():
#         table.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[0.,255.,0.]).all():
#         cabinet.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[100.,100.,255.]).all():
#         window.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[0.,0.,255.]).all():
#         floor.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[0.,255.,255.]).all():
#         wall.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[200.,200.,100.]).all():
#         door.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[255.,255.,0.]).all():
#         other.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[255.,0.,255.]).all():
#         desk.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[200.,100.,100.]).all():
#         sofa.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[50.,50.,50.]).all():
#         clutter.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[200.,200.,200.]).all():
#         board.append(pointclouds_origin[i][0:6]/b)
#     elif (pointcloud[3:6]==[10.,200.,100.]).all():
#         bookshelf.append(pointclouds_origin[i][0:6]/b)
#     i+=1 

if not (os.path.isdir(dir)):
    os.mkdir(dir)
np.savetxt(dir+'/chair.txt',np.array(chair))
np.savetxt(dir+'/table.txt',np.array(table))
np.savetxt(dir+'/cabinet.txt',np.array(cabinet))
np.savetxt(dir+'/window.txt',np.array(window))
np.savetxt(dir+'/floor.txt',np.array(floor))
np.savetxt(dir+'/wall.txt',np.array(wall))
np.savetxt(dir+'/door.txt',np.array(door))
np.savetxt(dir+'/other.txt',np.array(other))
np.savetxt(dir+'/desk.txt',np.array(desk))
np.savetxt(dir+'/sofa.txt',np.array(sofa))
np.savetxt(dir+'/bookshelf.txt',np.array(bookshelf))



# ceiling=np.array(ceiling)
# colors=np.array([i/255 for i in ceiling[:,3:]]) 
# pcd = o3d.geometry.PointCloud()
# pcd.points=o3d.utility.Vector3dVector(ceiling[:,:3])
# pcd.colors=o3d.utility.Vector3dVector(colors)
# print(len(pcd.points))
# o3d.visualization.draw_geometries([pcd])
