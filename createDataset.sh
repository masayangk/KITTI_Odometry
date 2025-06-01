#!/bin/sh
PROJECT_ROOT=/workspace/odometry
DATASET_ROOT=/workspace/kitti

# データセットの分割とコピー
for seq in 00 01 02 03 05 06 07 08 09 10
do
    # ディレクトリ構造の作成
    mkdir -p ${DATASET_ROOT}/train/${seq}/image_2
    mkdir -p ${DATASET_ROOT}/train/${seq}/local_maps
    mkdir -p ${DATASET_ROOT}/val/${seq}/image_2
    mkdir -p ${DATASET_ROOT}/val/${seq}/local_maps
    mkdir -p ${DATASET_ROOT}/test/${seq}/image_2
    mkdir -p ${DATASET_ROOT}/test/${seq}/local_maps
    
    echo "Processing sequence ${seq}..."
    
    # トレーニングデータのコピー（000000〜000499）- findコマンドを使用
    echo "Copying training data (000000-000499)..."
    find ${PROJECT_ROOT}/${seq}/image_2/ -name "[0-9][0-9][0-9][0-9][0-9][0-9].png" | grep -E "0{6}|0{5}[1-9]|0{4}[0-9]{2}|0{3}[0-4][0-9]{2}" | xargs -I{} rsync -avhP {} ${DATASET_ROOT}/train/${seq}/image_2/
    
    find ${PROJECT_ROOT}/${seq}/local_maps/ -name "[0-9][0-9][0-9][0-9][0-9][0-9].ply" | grep -E "0{6}|0{5}[1-9]|0{4}[0-9]{2}|0{3}[0-4][0-9]{2}" | xargs -I{} rsync -avhP {} ${DATASET_ROOT}/train/${seq}/local_maps/
    
    # 検証データのコピー（000500〜000599）
    echo "Copying validation data (000500-000599)..."
    find ${PROJECT_ROOT}/${seq}/image_2/ -name "[0-9][0-9][0-9][0-9][0-9][0-9].png" | grep -E "0{3}5[0-9]{2}" | xargs -I{} rsync -avhP {} ${DATASET_ROOT}/val/${seq}/image_2/
    
    find ${PROJECT_ROOT}/${seq}/local_maps/ -name "[0-9][0-9][0-9][0-9][0-9][0-9].ply" | grep -E "0{3}5[0-9]{2}" | xargs -I{} rsync -avhP {} ${DATASET_ROOT}/val/${seq}/local_maps/
    
    # ポーズファイルのコピー
    if [ -f ${PROJECT_ROOT}/${seq}/poses_train.csv ]; then
        rsync -avhP ${PROJECT_ROOT}/${seq}/poses_train.csv ${DATASET_ROOT}/train/${seq}/poses.csv
    fi
    
    if [ -f ${PROJECT_ROOT}/${seq}/poses_val.csv ]; then
        rsync -avhP ${PROJECT_ROOT}/${seq}/poses_val.csv ${DATASET_ROOT}/val/${seq}/poses.csv
    fi
    
    if [ -f ${PROJECT_ROOT}/${seq}/poses_test.csv ]; then
        rsync -avhP ${PROJECT_ROOT}/${seq}/poses_test.csv ${DATASET_ROOT}/test/${seq}/poses.csv
    fi
    
    # テストデータのコピー（000600〜）
    echo "Copying test data (000600+)..."
    rsync -avhP  ${PROJECT_ROOT}/${seq}/image_2/* ${DATASET_ROOT}/test/${seq}/image_2/
    rsync -avhP  ${PROJECT_ROOT}/${seq}/local_maps/* ${DATASET_ROOT}/test/${seq}/local_maps/

    # 000000から000599までのファイルをテストディレクトリから削除
    for scene in $(seq -f "%06g" 0 1 599)
    do
        rm -f ${DATASET_ROOT}/test/${seq}/image_2/${scene}.png
        rm -f ${DATASET_ROOT}/test/${seq}/local_maps/${scene}.ply
    done
done

# シーケンスファイルのコピー
if [ -f ${PROJECT_ROOT}/sequence.txt ]; then
    rsync -avhP ${PROJECT_ROOT}/sequence.txt ${DATASET_ROOT}/train/
    rsync -avhP ${PROJECT_ROOT}/sequence.txt ${DATASET_ROOT}/val/
    rsync -avhP ${PROJECT_ROOT}/sequence.txt ${DATASET_ROOT}/test/
fi