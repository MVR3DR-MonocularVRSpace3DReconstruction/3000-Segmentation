# -*-coding:utf-8 -*-
import os
import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
import sys
os.getcwd()
np.set_printoptions(suppress=True)
# test_data_dir = '/home/pi/PycharmProjects/learn/Open3D/examples/test_data'
# point_cloud_file_name = 'fragment.ply'
# point_cloud_file_path = os.path.join(test_data_dir, point_cloud_file_name)
#pointcloud_obj_path=sys.argv[1]+'.obj' #lab.obj
pointcloud_name= sys.argv[1] #lab
pointcloud_class=sys.argv[2] #chair table.....
pointcloud_txt='./results/class_segment/'+pointcloud_name+'/'+pointcloud_class+'.txt' #chair.txt (origin color)
#outfiletxt='./'+outfile + '.txt'
#outfilenpy='./'+outfile + '.npy'

# 讀取點雲
pcd =o3d.io.read_point_cloud(pointcloud_txt, format='xyzrgb')
xyz =np.loadtxt(pointcloud_txt) #(34516,6)
num_of_point = xyz.shape[0]

# 使用聚類演算法
# with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
#     labels = np.array(pcd.cluster_dbscan(eps=0.02, min_points=10, print_progress=True))
e=float(sys.argv[3])
m=int(sys.argv[4])
#dbscan return a list of label of each point after cluster_dbscan
visual = np.array(pcd.cluster_dbscan(eps=e, min_points=m, print_progress=True))
labels = (np.array(pcd.cluster_dbscan(eps=e, min_points=m, print_progress=True),dtype='int',ndmin=2)).T #(34516,)
max_label = labels.max()

# create list  chair0 chair1 chair2...
for _ in range(max_label):
    globals()[pointcloud_class+str(_)]=[]

# combine xyzrgb and label
xyzrgbl=np.array((np.concatenate((xyz,labels),axis=1)))

# individualize
for label in range(max_label): #each chair
    for _ in range(num_of_point): #search whole points 
        if int(xyzrgbl[_][6])== int(label): #append points to list           
            globals()[pointcloud_class+str(label)].append(xyzrgbl[_][:7])

#save
pointcloud_dir='./results/individual_segment/'+pointcloud_name
individual = pointcloud_dir+'/'+pointcloud_class
if not (os.path.isdir(pointcloud_dir)):
    os.mkdir(pointcloud_dir)
for label in range(max_label):
    np.savetxt(individual+'_'+str(label)+'.txt',np.array(globals()[pointcloud_class+str(label)])) # list > array > txt  
    pcdtmp =o3d.io.read_point_cloud(individual+'_'+str(label)+'.txt', format='xyzrgb') 
    o3d.io.write_point_cloud(individual+'_'+str(label)+'.ply', pcdtmp)

#求點雲的聚類數量
print(f"point cloud has {max_label + 1} clusters")

# 視覺化
# colors = plt.get_cmap("tab20")(visual / (max_label if max_label > 0 else 1))
# colors[visual < 0] = 0
# pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
# o3d.visualization.draw_geometries([pcd],
#                                   zoom=0.455,
#                                   front=[-0.4999, -0.1659, -0.8499],
#                                   lookat=[2.1813, 2.0619, 2.0999],
#                                   up=[0.1204, -0.9852, 0.1215])
