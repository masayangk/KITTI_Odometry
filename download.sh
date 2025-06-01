#!/bin/sh

# Odometry データセットのベースURL
BASE_URL="https://s3.eu-central-1.amazonaws.com/avg-kitti"
SEMANTIC_KITTI_URL="https://semantic-kitti.org/assets"

# ダウンロードと展開の関数
download_and_extract() {
    local url=$1
    local output=$2
    wget -c $url -O $output
    unzip $output
    rm $output
}

# シーケンスディレクトリの作成
for seq in 00 01 02 03 04 05 06 07 08 09 10; do
    mkdir -p odometry/$seq
done

# 各データセットのダウンロードと整理

# Odometry カラー画像
download_and_extract "$BASE_URL/data_odometry_color.zip" "data_odometry_color.zip"
for seq_id in 00 01 02 03 04 05 06 07 08 09 10; do
    mv dataset/sequences/$seq_id/* odometry/$seq_id  # カラー画像
done
rm -r dataset

# Odometry グレースケール画像
download_and_extract "$BASE_URL/data_odometry_gray.zip" "data_odometry_gray.zip"
for seq_id in 00 01 02 03 04 05 06 07 08 09 10; do
    mv dataset/sequences/$seq_id/* odometry/$seq_id  # グレースケール画像
done
rm -r dataset

# Odometry 点群データ
download_and_extract "$BASE_URL/data_odometry_velodyne.zip" "data_odometry_velodyne.zip"
for seq_id in 00 01 02 03 04 05 06 07 08 09 10; do
    mv dataset/sequences/$seq_id/* odometry/$seq_id  # 点群データ
done
rm -r dataset

# Odometry 地上真値ポーズ
download_and_extract "$BASE_URL/data_odometry_poses.zip" "data_odometry_poses.zip"
for seq_id in 00 01 02 03 04 05 06 07 08 09 10; do
    mv dataset/poses/$seq_id.txt odometry/$seq_id  # ポーズ
done
rm -r dataset

# Odometry キャリブレーションデータ
download_and_extract "$BASE_URL/data_odometry_calib.zip" "data_odometry_calib.zip"
for seq_id in 00 01 02 03 04 05 06 07 08 09 10; do
    mv dataset/sequences/$seq_id/* odometry/$seq_id  # キャリブレーションデータ
done
rm -r dataset

# Semantic KITTI ラベルデータ
download_and_extract "$SEMANTIC_KITTI_URL/data_odometry_labels.zip" "data_odometry_labels.zip"
for seq_id in 00 01 02 03 04 05 06 07 08 09 10; do
    mv dataset/sequences/$seq_id/* odometry/$seq_id  # ラベルデータ
done
rm -r dataset 
rm README

# Semantic KITTI トレーニングボクセルデータ
download_and_extract "$SEMANTIC_KITTI_URL/data_odometry_voxels_all.zip" "data_odometry_voxels_all.zip"
for seq_id in 00 01 02 03 04 05 06 07 08 09 10; do
    mv dataset/sequences/$seq_id/* odometry/$seq_id  # ボクセルデータ
done
rm -r dataset

echo "すべてのシーケンスを整理しました！"