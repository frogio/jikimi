from CCTV import recordVideo, transferVideo
from CCTVUtil import printLog
from time import time, localtime, sleep

# 분 단위
# REST_TIME = 3
# LUNCH_TIME = 3

REST_TIME = 10
LUNCH_TIME = 60


IDX_LUNCH = 3

def sync_time_table(time_table):                          # 현재 시간과 시간표를 동기화한다.
    cur_time = localtime(time())
    cur_min = cur_time.tm_hour * 60 + cur_time.tm_min
    sync_time_no = 0

    for time_ in time_table:

        if(sync_time_no == IDX_LUNCH):
            time_ += LUNCH_TIME

        else :
            time_ += REST_TIME

        if(cur_min > time_):
            sync_time_no += 1

        else : break

    return sync_time_no


def main():
    global REST_TIME, LUNCH_TIME, IDX_LUNCH
    time_table = (570, 630, 690, 750, 860, 920, 980)        # 쉬는 시간 시작 시간 및 점심시간 시작 시간 (분 단위)
                                                            # 시간 영역 인덱스
    rest_time_no = sync_time_table(time_table)                # 현재 시간과 시간표를 동기화

    while(True):
        cur_time = localtime(time())
        cur_min = cur_time.tm_hour * 60 + cur_time.tm_min  # 현재 시간(분 단위로 처리)
        
        if(cur_min < 570 or cur_min > 990):
            printLog("System", "reached end of schedule, camera goes into sleep mode...")
            sleep(10)
            rest_time_no = 0
            continue
    
        startTime = time_table[rest_time_no]                        # 영상 녹화 시작시간 설정
        endTime = 0

        if(rest_time_no != IDX_LUNCH):                              # 점심시간이 아닐 경우
            endTime = time_table[rest_time_no] + REST_TIME          # 영상 녹화 종료시간 설정

        elif(rest_time_no == IDX_LUNCH ):                           # 점심시간일 경우
            endTime = time_table[rest_time_no] + LUNCH_TIME         # 영상 녹화 종료시간 설정

        if(startTime <= cur_min and cur_min <= endTime):            # 영상녹화를 시작할 시간일 경우
            
            if(rest_time_no != IDX_LUNCH):							# 로그 출력
                printLog("Time", "rest time")
            else:
                printLog("Time", "lunch time")

            transferVideo(recordVideo(endTime))                     # 영상 기록
            rest_time_no += 1                                       # 영상처리 기록이 끝났으므로 다른 시간 영역으로 인덱스를 옮긴다

        else:
            printLog("System","wait record...")
            # printLog("System", "current_time : " + str(rest_time_no + 1) + "번째 쉬는시간")
            sleep(10)


if __name__ == "__main__":
    main()  