#!/bin/bash

for seq in {0..10}
do
    python /workspace/make_localMaps.py \
        --sequence ${seq}
done