#!/bin/sh
for seq in 00 01 02 03 04 05 06 07 08 09 10
do
    rm -r ${seq}/local_maps
done

# rm -r kitti_maps