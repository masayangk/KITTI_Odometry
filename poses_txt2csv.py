import argparse
from utils import * 

parser = argparse.ArgumentParser()
parser.add_argument('--sequence', '-s', default=0, type=int, help='sequence')
parser.add_argument('--start', '-st', default=0, type=int, help='start scene')
parser.add_argument('--num_scene', '-n', default=None, type=int, help='start scene')
parser.add_argument('--mode', '-m', default='train', type=str, help='train or val or test')
args = parser.parse_args()

def main(args):
    seq = f'{args.sequence:02d}'
    mode = f'{args.mode}'
    
    input_path = f'{ROOT_DIR}/{seq}/poses.txt'
    output_path = f'{ROOT_DIR}/{seq}/poses_{mode}.csv'
    poses = load_poses(input_path)
    RTs = matrix2RT(poses)
    save_csv(RTs, output_path, args.start, args.num_scene)

if __name__=='__main__':
    main(args)
    