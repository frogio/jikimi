#!/bin/bash

video_name=$1
video_name="/root/data/${video_name}"

echo "video_name=${video_name}"

school=$(echo $1 | cut -d '/' -f 1)
date=$(echo $1 | cut -d '/' -f 2)
time=$(echo $1 | cut -d '/' -f 3)
time=${time:0:(-4)}

echo $school
echo $date
echo $time

python --version
python3 --version

mkdir /root/data/result/$school
mkdir /root/data/result/$school/$date
touch "/root/data/result/$school/$date/${time}.log"

python3 /root/yolov5/detect.py --source $video_name --weights /root/yolov5/best.pt --conf 0.65

aws s3 mv "/root/data/result/$school/$date/$time.log" "s3://project2-school-violence-detection-result/$school/$date/${time}.log"
aws s3 mv "/root/data/result/$school/$date/$time.mp4" "s3://project2-school-violence-detection-result/$school/$date/${time}.mp4"

count_school_data=$(ls -l /root/data/${school} | grep ^- | wc -l)
count_date_data=$(ls -l /root/data/${school}/${date} | grep ^- | wc -l)

echo "count_school_data = ${count_school_data}"
echo "count_date_data = ${count_date_data}"

if [ $count_date_data -eq 0 ];then
	rm -d -r -f /root/data/result/$schhool/$date
fi

if [ $count_school_data -eq 0 ];then
	rm -d -r -f /root/data/$school
fi

exit 0
