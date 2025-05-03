# -------------------------------------------------------------------
# Copyright (C) 2020 Università degli studi di Milano-Bicocca, iralab
# Author: Daniele Cattaneo (d.cattaneo10@campus.unimib.it)
# Released under Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# http://creativecommons.org/licenses/by-nc-sa/4.0/
# -------------------------------------------------------------------
import argparse
import os
import gc
from tqdm import tqdm
import numpy as np
import torch
import open3d as o3d
from constant import *
from utils import *

# パラメータの読み込み
parser = argparse.ArgumentParser()
parser.add_argument('--sequence', '-s', default=0, type=int, help='sequence')
parser.add_argument('--map_folder', '-m', default=f'/workspace/kitti_maps', type=str, help='worldMap Folder')
parser.add_argument('--local_maps_dirname', '-l', default='local_maps', type=str, help='Folder to save the local_maps')
args = parser.parse_args()

# CUDAが利用可能か確認
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"使用デバイス: {device}")

def _to_camera(pcl, poses, id):
    cam2world = get_extrinsics(poses, id)
    world2cam = torch.from_numpy(np.linalg.inv(cam2world)).to(pcl.device)
    pcl_cam = torch.mm(pcl, world2cam.T)
    
    return pcl_cam

def main(args):
    # ポーズの読み込み
    seq = f'{args.sequence:02d}'
    seq_dir = f'{ROOT_DIR}/{seq}'
    output_dir = f'{seq_dir}/{args.local_maps_dirname}'
    poses_file = os.path.join(seq_dir, f'poses.txt')
    map_file = os.path.join(args.map_folder, f'{seq}.pcd')

    os.makedirs(output_dir, exist_ok=True)
    poses = load_poses(poses_file)
    
    # ワールドマップの読み込み
    print("ワールドマップを読み込んでいます...")
    worldMap = o3d.io.read_point_cloud(map_file)
    
    # torchに変換
    world_ptCloud = np.asarray(worldMap.points)
    world_ptCloud = torch.from_numpy(np.hstack((world_ptCloud, np.ones((world_ptCloud.shape[0], 1))))).to(device)
    world_colors = torch.from_numpy(np.asarray(worldMap.colors)).to(device)
    
    # CPUメモリの解放
    del worldMap
    gc.collect()
    
    img2CMRNet = load_Image2CMRNet(device)
    
    print(f"{len(poses)}フレームを処理しています...")
    for id in tqdm(range(len(poses))):
        # 点をカメラ座標に変換
        cam_ptCloud = _to_camera(world_ptCloud, poses, id)
        
        # GPUでマスクを適用
        mask = (cam_ptCloud[:, 0] > -25) & \
               (cam_ptCloud[:, 0] < 25) & \
               (cam_ptCloud[:, 2] > -10) & \
               (cam_ptCloud[:, 2] < 100)
        
        local_ptCloud = torch.mm(cam_ptCloud[mask], img2CMRNet.T)[:, :3].clone().cpu().numpy()
        local_colors = world_colors[mask].clone().cpu().numpy()
            
        # 結果を保存
        output_path = os.path.join(output_dir, f'{id:06d}.ply')
        save_ply(local_ptCloud, local_colors, output_path)
            
        
    # このイテレーションのGPUメモリを解放
    del cam_ptCloud, world_colors
    torch.cuda.empty_cache()

if __name__ == '__main__':
    main(args)