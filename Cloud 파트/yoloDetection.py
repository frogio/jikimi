import mysql.connector
import boto3
import json
import os
import time
from urllib import parse



# 인스턴스 정보
access_key = os.environ['access_key']
secret_key = os.environ['secret_key']
region = os.environ['region']
instance_id = os.environ['instance_id']

# s3 정보
BUCKET_NAME = os.environ['BUCKET_NAME']

# 데이터베이스 정보
DBNAME = os.environ['DBNAME']
ENDPOINT= os.environ['ENDPOINT']
PASSWD= os.environ['PASSWD']
PORT= os.environ['PORT']
USER= os.environ['USER']

   
def run_command(instance_id: str, client, commands: list):
   response = client.send_command(
       DocumentName="AWS-RunShellScript",
       Parameters={"commands": commands},
       InstanceIds=[instance_id],
       CloudWatchOutputConfig={
           'CloudWatchLogGroupName': 'yolo-CloudWatch-private',
           'CloudWatchOutputEnabled': True
       }
   )
   return response
   
def get_command_status(command_id: str, instance_id: str, client):
    
    response = client.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id
    )
    
    return response.get("Status")
   

def lambda_handler(event, context):
    # 삽입된 비데오 이름
    new_video_name = parse.unquote(event['Records'][0]['s3']['object']['key'])
    print(new_video_name)
    print(type(new_video_name))
    
    
    # ssm 클라이언트
    ssm_client = boto3.client(
        "ssm",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

    s3_url = 's3://'+BUCKET_NAME+"/"+new_video_name
    command_s3_download = f"aws s3 cp {s3_url} /root/data/{new_video_name}"
    print(command_s3_download)
    
    response = run_command(instance_id, ssm_client, [command_s3_download])
    command_id = response.get("Command").get("CommandId")
    command_status = "Pending"
    print("command_id : ", command_id)
    time.sleep(2)
    while command_status in ("Pending", "InProgress", "Delayed"):
        print("The command Status ------- ", command_status)
        command_status = get_command_status(command_id, instance_id, ssm_client)
        time.sleep(20)
    
    
    response = run_command(instance_id, ssm_client,[f'bash /root/yoloScript.sh {new_video_name}'])
    # 넘겨준 동영상의 url 을 데이터베이스에 저장한다.
    # - 데이터베이스 접속
    
    video_full_url = 'https://project2-school-violence-detection.s3.us-east-2.amazonaws.com/'
    video_full_url = video_full_url + event['Records'][0]['s3']['object']['key']
    
    # 비데오 정보 (날짜, 시작시간, 끝나는 시간, 학교, 비데오 경로)
    
    video_date = new_video_name.split('/')[1].replace('_','-')
    video_start_time = new_video_name.split('/')[2].replace('.mp4','').replace('_',':')
    video_school = new_video_name.split('/')[0]
    video_path = video_full_url
    
    find_school_sql = f"SELECT school_id FROM School WHERE school_name = '{video_school}'"

    try:
        conn =  mysql.connector.connect(host=ENDPOINT, user=USER, passwd=PASSWD, port=PORT, database=DBNAME)
        cur = conn.cursor(buffered=True)
        cur.execute(find_school_sql)
        rows = cur.fetchall()
        
        if len(rows) != 1:
            video_school = 1
        else:
            video_school = rows[0][0]
            
        insert_video_sql = f"INSERT INTO Video(video_date, video_start_time, video_school, video_path) VALUES ('{video_date}','{video_start_time}',{video_school},'{video_path}')"
        print(insert_video_sql)
        cur.execute(insert_video_sql)
        conn.commit()
            
    except Exception as e:
        print(e)
        return {
            "success" : False
        }
    
    
    return {
        'statusCode': 200,
        'new_video_name' : new_video_name,
        'video_date' : video_date,
        'video_full_url':video_full_url,
        'find_school_sql':find_school_sql,
        'video_school': video_school,
        'success' : True
    }
