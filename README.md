# 슬기로운 지키미 - 멀티캠퍼스 융복합 프로젝트

진행기간 : 2023.01.03 ~ 2023.02.16

주제 : 학교폭력예방 및 대응
  - 학교폭력위험지표개발(학교폭력위험점수, 학교폭력위험단계)
  - 학교에 설치된 CCTV에서 폭력 감지 시 학교선생님께 SMS 전송 

팀원 
  - 빅데이터 : 박수은, 서혁준, 유영일
  - 클라우드 : 박예서(팀장), 유승지, 이기복
  - Iot : 김준무

## Cloud(AWS)

### Service Architecture
![image](https://user-images.githubusercontent.com/12217092/221348484-94daeedc-4942-4293-b5fc-ed1355ebdd94.png)

### SMS 서비스
학교폭력 발생 시 서버에서 SMS를 보내 담당교사에게 알림

![image](https://user-images.githubusercontent.com/12217092/220605051-a7ddd25d-8e55-4af8-94bb-6cb1ff0fb2b9.png)
  

## Big Data

## **학교폭력위험 지표**
학교폭력발생에는 다양한 원인이 존재한다. 
한 개인이 어떤 사람으로 자라며 어떻게 행동하는가는 그 사람의 의식 구조에 따라 결정되는 수가 많으며 
그 의식 구조의 형성에는 개인이 자라온 가정, 환경, 학교, 사회의 환경에 의해서 결정된다. 
CPTED(셉테드) 범죄예방 디자인 연구센터에 따르면 학교 폭력은 학교 내 외부의 환경과 연관이 있다고 말하고 있다. 
따라서 학교폭력의 사회 환경적 요인에 환경지표, 학교폭력의 학교 개별환경적 요인으로 위해지표, 경감지표로 분류하여
서울특별시 고등학교 학교폭력위험지표를 개발하였다. 

## 분석 도구 및 절차

### 상관분석

유의미한 요인을 파악하기 위해 상관분석을 진행하여 높은 수준의 상관관계가 있는 요인 선택

### Standard Scaler

Scale이 큰 feature의 영향이 비대해지는 것을 방지 

### Kmeans(TSNE) 사용

![image](https://user-images.githubusercontent.com/12217092/221348641-e9477dfd-3b12-41e2-9621-cadfdd9f7cb3.png)

### Elbow method / Silhouette Score

군집화에 있어 가장 최적인 k를 찾는 방법



## 환경지표

학교폭력위험도 가중에 영향을 미치는 서울특별시 자치구 환경을 반영하여 점수를 산정한 상대적 지표 
분석 과정


### 1. 판다스 내부 Corr 함수를 이용해 상관분석

사회환경요인과 실제학교폭력신고수·피해응답학생 수 상관분석 진행 

### 2. 상관분석 결과를 바탕으로 사회환경요인 중 유의미한 변수 결정

![image](https://user-images.githubusercontent.com/12217092/221348955-e6a7f532-6b97-4b04-9c69-b352e96ee210.png)

### 3. Standard Scaler 진행

데이터 scale 조정

### 4. Kmeans 군집화(TSNE 사용) 

![image](https://user-images.githubusercontent.com/12217092/221348991-a521f057-538d-4d90-85d3-9365563fd64c.png)

## 위해지표

학교폭력위험도 가중에 영향을 미치는 학교 개별환경요인을 반영하여 점수를 산정한 상대적 지표

### 1. 학교 개별환경요인

학교500m내 유흥업소 개수, 학교폭력피해장소, 학교폭력피해유형, 학교폭력피해시간

### 2. Standard Scaler 진행

데이터 scale 조정

### 3. Kmeans 군집화(TSNE 사용) 

![image](https://user-images.githubusercontent.com/12217092/221349150-b64bbda0-ba6c-4459-984f-e97a4f7bbe0c.png)

### 4. 위해지표 점수

위해지표 학교폭력위험점수 계산 : 0~100점으로 5분위수 계산

![image](https://user-images.githubusercontent.com/12217092/221349582-d2a8c137-ac84-41ff-af3e-e0c19b280084.png)



## 경감지표

학교폭력위험도 경감에 영향을 미치는 학교 개별환경요인을 반영하여 점수를 산정한 상대적 지표

### 1. 학교 개별환경요인

학교 500m내 cctv대수, 학교500m내 경찰관서수, 학교폭력예방교육시간

### 2. Standard Scaler 진행

데이터 scale 조정

### 3. Kmeans 군집화(TSNE 사용) 

![image](https://user-images.githubusercontent.com/12217092/221349265-bfa761e8-fcf9-437c-85bb-ec63b20f2c15.png)

### 4. 경감지표 점수

경감지표 학교폭력위험점수 계산 : 0~100점으로 4분위수 계산

![image](https://user-images.githubusercontent.com/12217092/221349612-5a6e6785-067b-411e-b38a-95060cca3724.png)

## 학교 폭력 위험 지표

학교폭력에 영향을 미치는 사회환경요인과 학교개별환경요인을 모두 반영한 종합지표

### 학교폭력 위험점수

학교폭력위험점수란, 환경지표 · 위해지표 · 경감지표에서 학교폭력위험에 영향을 미치는 상관계수 크기를 가중치로 부여해서 계산한 학교폭력종합점수이다.
점수는 0 ~ 100의 범위를 가지며, 점수와 위험도는 비례한다.

![image](https://user-images.githubusercontent.com/12217092/221349842-43da39bf-76f6-4eac-b9fa-0a36d461b7ca.png)

## **데이터 명세**
#### A. 서울열린데이터광장
1. 서울시 저소득 한부모 가족(29 rows × 15 columns)
2. 서울시 소득인식 수준(240 rows × 5 columns)
3. 서울시 자치구 단위 생활인구(219000 rows × 32 columns)
4. 서울시 다문화가정(28 rows × 11 columns)
5. 서울시 보통가구(3600 rows × 7 columns)
6. 서울시 CCTV설치현황(83734 rows × 7 columns)

#### B. 스마트치안빅데이터플랫폼
1. 학교폭력(1966 rows × 43 columns)
2. 청소년비행/학교폭력영향데이터(247 rows × 14 columns) 
3. 112신고영향요소융(273 rows × 28 columns) 

#### C. 공공데이터포털
1. 경찰관서 위치 주소(2037 rows × 8 columns) 
2. 소상공인진흥공단 상권정보(377724 rows × 39 columns)

#### D. 나이스
1. 학교기본정보(1421 rows × 25 columns)

#### E. 학교알리미(크롤링)
1. 학교폭력 조사참여 현황
2. 학교폭력 피해시간
3. 학교폭력 피해신고현황
4. 학교폭력 피해유형
5. 학교폭력 피해장소
6. 학교폭력 예방교육시간


## **YOLO**
학습데이터 : roboflow Violence Detection dataset 1500개 이미지 사용

링크 : https://universe.roboflow.com/nuscrimesocietydatasets/violence-9gmjx




## IoT & Web Interface

### CCTV 구조

![image](https://user-images.githubusercontent.com/12217092/220604062-1c2a3ee0-9af0-487e-91cf-52da002148a4.png)


### CCTV 작동 모습

![image](https://user-images.githubusercontent.com/12217092/220603217-2877a945-6d48-4b55-98b2-58d005f217bf.png)


### Web interfaces

Django 4.1.1 기반으로 작성됨 

PC

![image](https://user-images.githubusercontent.com/12217092/220603318-f9574569-7878-4e0c-9785-1b80d711bdcd.png)

![image](https://user-images.githubusercontent.com/12217092/220604524-09f21847-f75f-46da-a2d8-3608c1aff94f.png)

Mobile

![image](https://user-images.githubusercontent.com/12217092/220603352-a5e1b1ea-3f48-47d9-b09b-80c4f29c93b2.png)
