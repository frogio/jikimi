import cv2
import boto3
from CCTVUtil import printLog
from time import time, localtime

# VIDEO_LENGHT = 60       # 1분 녹화 (Sample)
# latest_time = time()

SCHOOL_NAME = "명지고등학교"

def recordVideo(endTime):

    tm = localtime(time())
    hour = str(tm.tm_hour).zfill(2)
    min = str(tm.tm_min).zfill(2)

    now = hour + "_" + min

    cap = cv2.VideoCapture(0)
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*"H264")    
    out = cv2.VideoWriter(now + ".mp4", fourcc, fps, (640, 480))

    printLog("CCTV", "start record...")

    while(cap.isOpened()):
        ret, frame = cap.read()
        out.write(frame)

        tm = localtime(time())
        cur_min = tm.tm_hour * 60 + tm.tm_min
        
        if(cur_min > endTime):
            break            

    cap.release()
    out.release()

    printLog("CCTV", "recording success")
    return now

def transferVideo(now):
    global SCHOOL_NAME

    tm = localtime(time())

    month = str(tm.tm_mon).zfill(2)
    day = str(tm.tm_mday).zfill(2)

    s3 = boto3.client('s3')
    bucket_name = 'project2-school-violence-detection'

    today = str(tm.tm_year) + "_" + month + "_" + day
    file_name = SCHOOL_NAME + "/" + today + "/" + now

    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name="us-east-2",
            aws_access_key_id="AKIA5VZTIAOJXZNJHMMD",
            aws_secret_access_key="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",
        )

    except Exception as e:
        print(e)
    
    else:
        printLog("S3", "s3 bucket connected!") 

    s3.upload_file(now + ".mp4", bucket_name, file_name + ".mp4")
    printLog("S3", "transfer video success")