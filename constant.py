import numpy as np

ROOT_DIR = '/workspace/dataset'
# ROOT_DIR = '/home/kato/KITTI_Odometry'

# 点群のラベル
LABELS = {
    "unlabeled": 0,
    "outlier": 1,
    "car": 10,
    "bicycle": 11,
    "bus": 13,
    "motorcycle": 15,
    "on-rails": 16,
    "truck": 18,
    "other-vehicle": 20,
    "person": 30,
    "bicyclist": 31,
    "motorcyclist": 32,
    "road": 40,
    "parking": 44,
    "sidewalk": 48,
    "other-ground": 49,
    "building": 50,
    "fence": 51,
    "other-structure": 52,
    "lane-marking": 60,
    "vegetation": 70,
    "trunk": 71,
    "terrain": 72,
    "pole": 80,
    "traffic-sign": 81,
    "other-object": 99,
    "moving-car": 252,
    "moving-bicyclist": 253,
    "moving-person": 254,
    "moving-motorcyclist": 255,
    "moving-on-rails": 256,
    "moving-bus": 257,
    "moving-truck": 258,
    "moving-other-vehicle": 259
}

# ラベルの色
COLORS = {
    0: np.array([0, 0, 0], dtype=np.uint8),
    1: np.array([0, 0, 255], dtype=np.uint8),
    10: np.array([245, 150, 100], dtype=np.uint8),
    11: np.array([245, 230, 100], dtype=np.uint8),
    13: np.array([250, 80, 100], dtype=np.uint8),
    15: np.array([150, 60, 30], dtype=np.uint8),
    16: np.array([255, 0, 0], dtype=np.uint8),
    18: np.array([180, 30, 80], dtype=np.uint8),
    20: np.array([255, 0, 0], dtype=np.uint8),
    30: np.array([30, 30, 255], dtype=np.uint8),
    31: np.array([200, 40, 255], dtype=np.uint8),
    32: np.array([90, 30, 150], dtype=np.uint8),
    40: np.array([255, 0, 255], dtype=np.uint8),
    44: np.array([255, 150, 255], dtype=np.uint8),
    48: np.array([75, 0, 75], dtype=np.uint8),
    49: np.array([75, 0, 175], dtype=np.uint8),
    50: np.array([0, 200, 255], dtype=np.uint8),
    51: np.array([50, 120, 255], dtype=np.uint8),
    52: np.array([0, 150, 255], dtype=np.uint8),
    60: np.array([170, 255, 150], dtype=np.uint8),
    70: np.array([0, 175, 0], dtype=np.uint8),
    71: np.array([0, 60, 135], dtype=np.uint8),
    72: np.array([80, 240, 150], dtype=np.uint8),
    80: np.array([150, 240, 255], dtype=np.uint8),
    81: np.array([0, 0, 255], dtype=np.uint8),
    99: np.array([255, 255, 50], dtype=np.uint8),
    252: np.array([245, 150, 100], dtype=np.uint8),
    253: np.array([200, 40, 255], dtype=np.uint8),
    254: np.array([30, 30, 255], dtype=np.uint8),
    255: np.array([90, 30, 150], dtype=np.uint8),
    256: np.array([255, 0, 0], dtype=np.uint8),
    257: np.array([255, 150, 255], dtype=np.uint8),
    258: np.array([180, 30, 80], dtype=np.uint8),
    259: np.array([255, 0, 0], dtype=np.uint8)
}

RPY_CMRNET2IMAGE = [90, 90, 0]
