#!/bin/sh
./download.sh
./make_worldMap.sh
./make_localMaps.sh
./poses_txt2csv.sh
./createdataset.sh
