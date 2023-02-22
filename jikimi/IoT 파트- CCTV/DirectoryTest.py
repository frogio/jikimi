import boto3
from time import time, localtime

def transferVideo():
    s3 = boto3.client('s3')
    bucket_name = 'project2-school-violence-detection'

    tm = localtime(time())

    dir_name = "XX고등학교/" + str(tm.tm_year) + "_" + str(tm.tm_mon) + "_" + str(tm.tm_mday) + "/"
    # file_name = str(tm.tm_hour) + "_" + str(tm.tm_min)
    file_name = "TestVideo"


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
    
    # else:
        # printLog("S3", "s3 bucket connected!") 

    s3.upload_file(file_name + ".mp4", bucket_name, dir_name + file_name + ".mp4")
    # printLog("S3", "transfer video success")

transferVideo()