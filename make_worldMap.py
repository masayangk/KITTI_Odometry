import argparse
import gc
import os
from glob import glob
from tqdm import tqdm
import open3d as o3d
from constant import *
from utils import *

parser = argparse.ArgumentParser()
parser.add_argument('--sequence', '-s', default=0, type=int, help='sequence')
parser.add_argument('-v', '--voxel_size', default=0.10, type=float, help='Please enter the voxel_size. / Default: 0.10')
args = parser.parse_args()

is_static = lambda label: (label == LABELS['road']) | \
                          (label == LABELS['parking']) | \
                          (label == LABELS['sidewalk']) | \
                          (label == LABELS['other-ground']) | \
                          (label == LABELS['building']) | \
                          (label == LABELS['fence']) | \
                          (label == LABELS['other-structure']) | \
                          (label == LABELS['lane-marking']) | \
                          (label == LABELS['vegetation']) | \
                          (label == LABELS['trunk']) | \
                          (label == LABELS['terrain']) | \
                          (label == LABELS['pole']) | \
                          (label == LABELS['traffic-sign']) | \
                          (label == LABELS['other-object'])
                          
def _to_world(pcl, poses, velo2cam, id):
    cam2wld = get_extrinsics(poses, id)
    velo2wld = np.dot(cam2wld, velo2cam)
    pcl_wld = np.dot(pcl, velo2wld.T)
    
    return pcl_wld
    
def main(args):
    seq = f'{args.sequence:02d}'
    
    print(f'Processing {seq}')
    pcd_dir = f'/workspace/kitti_maps'
    os.makedirs(pcd_dir, exist_ok=True)
    pcd_path = f'{pcd_dir}/{seq}.pcd'
    bin_dir = f'{ROOT_DIR}/{seq}/velodyne'
    poses_path = f'{ROOT_DIR}/{seq}/poses.txt'
    calib_path = f'{ROOT_DIR}/{seq}/calib.txt'
    
    velo2cam = load_velodyne2camera(calib_path)
    poses = load_poses(poses_path)
    
    ptCloud_list: list = []
    clrCloud_list: list = []
    
    for id, (bin_path) in tqdm(enumerate(sorted(glob(f'{bin_dir}/*.bin')))):
        label_path = bin_path.replace('velodyne', 'labels').replace('.bin', '.label')
        pcl = load_bin(bin_path)
        labels = np.fromfile(label_path, dtype=np.uint32)
        colors = label2color(labels)
        pcl = pcl[is_static(labels)][::2]
        colors = colors[is_static(labels)][::2]
        pcl_wld = _to_world(pcl, poses, velo2cam, id)
        
        ptCloud_list.append(pcl_wld[:, :3])
        clrCloud_list.append(colors)
    
    ptCloud = np.vstack(ptCloud_list)
    clrCloud = np.vstack(clrCloud_list)
    
    # メモリ節約のために、リストをクリア
    del ptCloud_list, clrCloud_list
    gc.collect()
    
    save_pcd(ptCloud, clrCloud, pcd_path, args.voxel_size)
    
    # メモリ節約のために、最終データを解放
    del ptCloud, clrCloud
    gc.collect()
        
            
if __name__ == '__main__':
    main(args)
