import mysql.connector
import json
from urllib import parse
import boto3
import os
import cv2
import math
import datetime
import time

access_key = os.environ['access_key']
secret_key = os.environ['secret_key']
BUCKET_NAME = os.environ['BUCKET_NAME']

DBNAME = os.environ['DBNAME']
ENDPOINT= os.environ['ENDPOINT']
PASSWD= os.environ['PASSWD']
PORT= os.environ['PORT']
USER= os.environ['USER']


def message(message:str, phone_number:str, client):
        
    response = client.publish(
        PhoneNumber=phone_number,
        Message=message
    )
    print(phone_number,':')
    
    print(response)

def getPhoneNumber(cur, school_name):
    sql = f'SELECT user_phone FROM video_view WHERE school_name="{school_name}"'
    cur.execute(sql)
    rows = cur.fetchall()
    rows = [r[0] for r in rows]
    return rows
    
def message_violence(violenceTime, phone_numbers, video_url):
    
    client = boto3.client('sns',
                      aws_access_key_id = access_key,
                      aws_secret_access_key = secret_key,
                      region_name='us-east-2')
    response = client.list_sms_sandbox_phone_numbers()
    verifiedPhoneNumber = [result['PhoneNumber'] for result in response['PhoneNumbers'] if result['Status'] == 'Verified']
    
    phone_numbers = [phone.replace('010','+8210', 1) for phone in phone_numbers]
    print(phone_numbers)
    null_phone = 0
    
    cctv_link = f'https://jikimi.link/cctv_page/?video_url={video_url}'
    msg = f'CCTV 분석 결과 {violenceTime} 에 폭력이 발생하였습니다. 확인해주십시오.'
    print(msg)
    for phone in phone_numbers:
        if phone not in verifiedPhoneNumber:
            if null_phone == 0:
                phone = '+821079390170'
                null_phone = 1
            else:
                continue
                
        message(msg, phone, client)
    
def videoViewIsValid(cur):
    sql = """SELECT COUNT(*) FROM information_schema.VIEWS
    WHERE table_schema = 'team2_db'
    AND table_name = 'video_view'"""
    cur.execute(sql)
    rows = cur.fetchall()
    count_videoView = rows[0][0]
    
    print('비디오 뷰 개수 : ', count_videoView)
    
    if count_videoView > 0:
        return True
    return False
    
def makeVideoView(conn, cur):
    sql = """
    CREATE VIEW video_view AS
    SELECT video_id, school_name, video_date, video_start_time, video_isViolence, user_phone
    FROM School, Video, User
    WHERE school_id = video_school = user_school
    """
    cur.execute(sql)
    conn.commit()
    
def lambda_handler(event, context):
    # TODO implement
    print('total context : ',event['Records'][0]['s3']['object']['key'] )
    new_file_name = parse.unquote(event['Records'][0]['s3']['object']['key'])
    data_school = str(new_file_name).split('/')[0]
    data_date = str(new_file_name).split('/')[1].replace('_','-')
    data_time = str(new_file_name).split('/')[2].replace('.log','').replace('.mp4','').replace('_',':')
    
    
    # 들어온 파일의 양식이 mp4 일 경우
    if 'mp4' in new_file_name:
        print('mp4 file')
        
    # 들어온 파일의 양식이 log 일 경우
    if 'log' in new_file_name:
        # 임시 저장소에 로그 파일 다운로드
        tmp_file_place = '/tmp/result.log'
        
        print('log file 위치 : ', tmp_file_place)
        print('s3 파일 위치 : ', new_file_name)
        
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(BUCKET_NAME)
        bucket.download_file(new_file_name, tmp_file_place)
        
        # mp4 파일 있는지 확인
        s3_client = boto3.client('s3')
        mp4_filename = str(new_file_name)
        mp4_filename = mp4_filename.replace('log','mp4')
        dir_info = s3_client.list_objects(Bucket=BUCKET_NAME, Prefix = mp4_filename)['Contents']
        print('mp4 파일 확인 :', dir_info)
        
        # mp4 가 들어올 떄까지 기다린다.
        while len(dir_info) == 0:
            time.sleep(3)
            s3_client = boto3.client('s3')
            dir_info = s3_client.list_objects(Bucket=BUCKET_NAME, Prefix = mp4_filename)['Contents']
        
        file = open(tmp_file_place, 'r')
        result_log = file.readlines()
        result_log = [result.replace('(no detections)','None').replace(',','').replace('\n','') for result in result_log if 'video' in result]
        result_log = [result.split() for result in result_log]
        num_frame = int(result_log[0][2].replace('(','').replace(')','').split('/')[1])
        
        for result in result_log:
            result[2]=int(result[2].replace('(','').replace(')','').split('/')[0])
            
    
        
        violence_scene = [result for result in result_log if 'Violence' in result]
        
        violence_scene_sure = list()
        
        # 1초에 해당하는 프레임의 대략적인 개수
        check_frame_num = 20
        
        # confidence threshold (ex. 10 개의 프레임 중 6개  violence 라 판단하면 violence 라 판단.)
        check_prob = 0.5
        
        for idx, result in enumerate(violence_scene):
            if idx > len(violence_scene) -1 - check_frame_num:
                break
            
            count = 0
            for check in range(check_frame_num):
                
                if violence_scene[idx + check][2] <= result[2] + check_frame_num:
                    count +=1
                    
            if count >=(check_frame_num*check_prob):
                violence_scene_sure.append(result)
                
        print('Violence Scene : ', violence_scene[0])
        print('number of violence scene : ', len(violence_scene))
        
        print('number of Certain Violence Scene : ', len(violence_scene_sure))
        print('Certain Violence Scene :', violence_scene_sure)
        
        conn =  mysql.connector.connect(host=ENDPOINT, user=USER, passwd=PASSWD, port=PORT, database=DBNAME)
        cur = conn.cursor(buffered=True)
        
        if videoViewIsValid(cur) == False:
            makeVideoView(conn, cur)
        
        if len(violence_scene_sure) > 0:
            # 비디오 폭력 여부 업데이트 sql --> VIEW 사용
            sql = f'UPDATE video_view SET video_isViolence = TRUE WHERE school_name = "{data_school}" AND video_date = "{data_date}" AND video_start_time = "{data_time}"'
            violence_frame = violence_scene_sure[0][2]
            
            new_file_name = str(new_file_name)
            new_file_name = new_file_name.replace('log','mp4')
            new_file_name = parse.quote(new_file_name)
            print('new_file_name :', new_file_name)
            video_url = f'https://project2-school-violence-detection-result.s3.us-east-2.amazonaws.com/{new_file_name}'
            print('로그에 해당하는 비디오 url : ', video_url)
            video = cv2.VideoCapture(video_url)
            print('is opened : ', video.isOpened())
            fps = video.get(cv2.CAP_PROP_FPS)
            print('fps : ', fps)
            print('number of frame : ', num_frame)
            
            video_time = num_frame / fps
            print('video_time : ', video_time)
            
            violence_start_sec = math.floor(violence_frame / fps) *3
            print('폭력 시작 시간(초):', violence_start_sec)
            
            video_start_time = datetime.datetime.strptime(data_time, "%H:%M")
            violence_start_sec = datetime.timedelta(seconds=violence_start_sec)
            
            violence_start_time = video_start_time + violence_start_sec
            violence_start_time = violence_start_time.strftime("%H시 %M분 %S초")
            
            phone_numbers = getPhoneNumber(cur, data_school)
            print('학교 내 전화번호들 : ', phone_numbers)
            message_violence(str(violence_start_time), phone_numbers, video_url)
            
            
            
        else:
            sql = f'UPDATE video_view SET video_isViolence = FALSE WHERE school_name = "{data_school}" AND video_date = "{data_date}" AND video_start_time = "{data_time}"'
        
        
        cur.execute(sql)
        conn.commit()
        print('Update sql : ',sql)
        
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'new_file_name' : new_file_name,
        'data_school': data_school,
        'data_date':data_date,
        'data_time':data_time,
        'success': True,
    }
