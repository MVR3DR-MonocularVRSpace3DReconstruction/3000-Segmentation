import open3d as o3d
import numpy as np
import os
from plyfile import PlyData, PlyElement
import pandas as pd
import sys
#from mmdetection3d.demo import pc_seg_demo

def convert_ply(input_path, output_path):
    plydata = PlyData.read(input_path)  # read file
    print(plydata)
    data = plydata.elements[0].data  # read data
    data_pd = pd.DataFrame(data)  # convert to DataFrame
    data_np = np.zeros(data_pd.shape, dtype=np.float)  # initialize array to store data
    property_names = data[0].dtype.names  # read names of properties
    for i, name in enumerate(
            property_names):  # read data by property
        data_np[:, i] = data_pd[name]
        print(data_np)
    data_np.astype(np.float32).tofile(output_path)

np.set_printoptions(suppress=True) # 取消默认科学计数法，open3d无法读取科学计数法表示
plyfile=sys.argv[1]
outfile=sys.argv[2]
plyname = plyfile
plyfile2='./input/temp.ply'
plyfile='./input/'+plyfile+'.ply'
outfiletxt='./input/'+outfile + '.txt'
outfilenpy='./input/'+outfile + '.npy'
# ply to npy


plydata = o3d.io.read_point_cloud(plyfile)
plydata=plydata.voxel_down_sample(voxel_size=0.01) #downsample
plydata=plydata.remove_non_finite_points(True,True) #kill noise
o3d.io.write_point_cloud(plyfile2, plydata)
plydata = PlyData.read(plyfile2)  # 读取文件

data = plydata.elements[0].data  # 读取数据

data_pd = pd.DataFrame(data)  # 转换成DataFrame, 因为DataFrame可以解析结构化的数据
#data_pd.shape=(2049918,9)
data_np = np.zeros(data_pd.shape, dtype=np.float)  # 初始化储存数据的array
property_names = data[0].dtype.names  # 读取property的名字
for i, name in enumerate(property_names):  # 按property读取数据，这样可以保证读出的数据是同样的数据类型。
    data_np[:, i] = data_pd[name]
#data_np = [x,y,z,nx,ny,nz,r,g,b] 
xyz = data_np[:,0:3]
rgb = data_np[:,3:6]
#add label
labels=np.ones((xyz.shape[0],1))
xyzrgb=np.concatenate((xyz,rgb),axis=1)
xyzrgbl=np.concatenate((xyz,rgb,labels),axis=1)
#rgb 0~1
b = np.array([1 , 1, 1,255, 255, 255])
#npy > txt > pcd > ply
np.savetxt('./input/xyzrgb.txt',xyzrgb[:,:6]/b)
pcd =o3d.io.read_point_cloud('./input/xyzrgb.txt', format='xyzrgb') # 原npy文件中的数据正好是按x y z r g b进行排列
o3d.io.write_point_cloud("./input/xyzrgb.ply", pcd)

#ply > bin (mmd3d)
convert_ply("./input/xyzrgb.ply","./mmdetection3d/demo/data/s3dis/"+outfile+".bin")
#npy (pointnet2)
np.save('./Pointnet_Pointnet2_pytorch/data/s3dis/stanford_indoor3d/Area_5_'+outfile+'_1',xyzrgbl)

np.savetxt(outfiletxt,xyzrgbl)

os.remove("./input/xyzrgb.txt")
os.remove("./input/xyzrgb.ply")
os.remove("./input/temp.ply")

# mmd3d or pointnet2
print('==============================================================================\nmmd3d or pointnet2\n==============================================================================')
os.system("python ./mmdetection3d/demo/pc_seg_demo.py ./mmdetection3d/demo/data/s3dis/"+plyname+".bin ./mmdetection3d/configs/pointnet2/pointnet2_ssg_16x2_cosine_200e_scannet_seg-3d-20class.py ./mmdetection3d/checkpoints/pointnet2_ssg_16x2_cosine_200e_scannet_seg-3d-20class_20210514_143644-ee73704a.pth")

#class_segment
print('==============================================================================\nclass_segment\n==============================================================================')
np.save('./results/mmd3d/'+outfile+'/'+outfile,xyzrgbl)
os.system("python ./class_segment.py "+outfile) #outfile name (lab)


#individual_segment
print('==============================================================================\nindividual_segment\n==============================================================================')
pcd_class=['cabinet','floor','wall','other','desk','window','door','table','chair','sofa','bookshelf']
for Class in pcd_class:
    print(Class+'_segment\n')
    os.system("python ./individual_segment.py "+outfile+" "+Class+" 0.1 400")

