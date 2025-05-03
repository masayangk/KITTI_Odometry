import os
import gc
import csv
import torch
import numpy as np
from scipy.spatial.transform import Rotation
import open3d as o3d
from constant import *

def matrix2RT(poses, scalar_first: bool = False) -> list:
    RT_list = []
    for id in range(len(poses)):
        mat4x4 = get_extrinsics(poses, id)
        transl = mat4x4[:3, 3]
        rot_matrix = mat4x4[:3, :3]
        quat = Rotation.from_matrix(rot_matrix).as_quat(scalar_first=scalar_first)
        RT_list.append(np.hstack((transl, quat)).tolist())

    return RT_list

def save_csv(RT_list, csv_path, start=0, num_scene=None):
    if num_scene is not None:
        end = start + num_scene - 1
    else:
        end = len(RT_list) - 1
    
    save_list = []
    for timestamp, (RT) in enumerate(RT_list):
        if timestamp < start:
            continue
        elif timestamp > end:
            break
        else:
            save_list.append([f'{timestamp:06d}'] + RT)

    with open(csv_path, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp','x','y','z','qx','qy','qz','qw'])
        writer.writerows(save_list)
        
def load_velodyne2camera(txt_path: str) -> np.ndarray:
    if os.path.exists(txt_path):
        with open(txt_path, mode='r') as f:
            lines = f.readlines()
            velo2cam = np.asarray(lines[4].split(' ')[1:]).astype(np.float64).reshape(3, 4)
            velo2cam = np.vstack((velo2cam, np.array([0, 0, 0, 1])))
    else:
        raise FileNotFoundError
        
    return velo2cam

def load_Image2CMRNet(device) -> torch.Tensor:
    img2CMRNet = np.eye(4)
    rot_matrix = Rotation.from_euler('XYZ', RPY_CMRNET2IMAGE, degrees=True).as_matrix()
    img2CMRNet[:3, :3] = rot_matrix
    img2CMRNet = torch.from_numpy(img2CMRNet).to(device)
    
    return img2CMRNet

def load_poses(txt_path):
    if os.path.exists(txt_path):
        with open(txt_path, mode='r') as f:
            poses = f.readlines()
    else:
        raise FileNotFoundError
    
    return poses
    
def get_extrinsics(poses, id):
    extrinsics = np.asarray(poses[id].split(' ')).astype(np.float64).reshape(3, 4)
    extrinsics = np.vstack((extrinsics, np.array([0, 0, 0, 1])))
        
    return extrinsics      

def label2color(labels):
    colors = np.zeros((labels.shape[0], 3), dtype=np.uint8)
    for key in LABELS.keys():
        colors[labels == LABELS[key]] = COLORS[LABELS[key]]
        
    return colors

def load_bin(bin_path):
    pcl = np.fromfile(bin_path, dtype=np.float32)
    pcl = pcl.reshape((-1, 4))
    pcl = pcl[:, :3]
    pcl = np.hstack((pcl, np.ones((pcl.shape[0], 1))))
    
    return pcl
    
def save_pcd(pcl, colors, save_path, voxel_size):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pcl)
    
    # pclとcolorsのメモリ解放
    del pcl
    gc.collect()  # ガーベジコレクションでメモリ解放

    pcd.colors = o3d.utility.Vector3dVector(colors / 255)
    
    # colorsのメモリ解放
    del colors
    gc.collect()
    
    o3d.io.write_point_cloud(save_path, pcd.voxel_down_sample(voxel_size=voxel_size))
    
def save_ply(pcl, colors, save_path):
    ply = o3d.geometry.PointCloud()
    ply.points = o3d.utility.Vector3dVector(pcl)
    ply.colors = o3d.utility.Vector3dVector(colors)
    o3d.io.write_point_cloud(save_path, ply)