#!/bin/sh
for seq in 00 01 02 05 06 07 08 09 10
do
    python poses_txt2csv.py \
        --sequence ${seq} \
        --mode train \
        --start 0 \
        --num_scene 500
    
    python poses_txt2csv.py \
        --sequence ${seq} \
        --mode val \
        --start 500 \
        --num_scene 100

    python poses_txt2csv.py \
        --sequence ${seq} \
        --mode test \
        --start 600
done