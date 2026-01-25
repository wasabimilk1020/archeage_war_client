import time
import img_search_utils
from serial_comm import *
import re
import check_hunting
from waking_from_sleep import *
from go_to_sleep import *

#data=[1142, 375, 10, 10, 0.0]=[x,y,xRange,yRange,delay]
def statusChk(sio, data, btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
  
  value=check_hunting.checkHunting() #value=성공 시=문자열, 실패 시=0
  if value[0]==1: #1을 return (사냥을 하지 않고 있다는 뜻)
    result=waking_from_sleep_and_deathChk(btn_name, sleep_time=2)
    if result==1: #사망 체크를 수행 했는대 chk.png가 확인 안되서 실패
      return 0, "페널티 체크 루틴 실패"
    result=normalHunting(sio, data, btn_name, character_name)
    return result
  elif value[0]==0: #capture_text_from_region 예외 발생
    return 1, value[1]
  else:  #성공
    text=value[0]
    return 2, text

def normalHunting(sio, data,btn_name, character_name):
  coord=data
  flag=data[4]
  name=character_name

  keyboard('1') #귀환
 
  delay_time=5
  for i in range(2):
    result_1=img_search_utils.searchImg('portion.png',beforeDelay=delay_time, afterDelay=5, chkCnt=10, _region=(530, 105, 900, 150),accuracy=0.7)
    if(result_1==0):
      return 0, "잡화상점 실패"
    result=img_search_utils.searchImg('auto_buy.png',beforeDelay=0, afterDelay=0.5, chkCnt=25, _region=(1430, 790, 300, 200))
    if(result==0):  #실패
      if (i==0):
        delay_time-=3
        continue
      else:
        return 0, "자동담기 실패"
    else:  #성공
      randClick(1560,920,10,10,0.5) #구매결정
      randClick(1075,660,10,10,0) #확인
      break #첫 번째 루프에서 성공하면 break

  escKey() #상점 나가기

  keyboard('v') #위치저장 클릭
  time.sleep(0.5)
  randClick(535,355,5,5,3)  #이동

  result=img_search_utils.searchImg('chk.png',beforeDelay=0, afterDelay=1, chkCnt=10, justChk=True, _region=(880, 40, 200, 150), accuracy=0.7)
  if(result==0):
    return 0, "체크 실패"
  
  keyboard('f') #사냥

  # keyboard('m') #지도
  # randClick(195,470,5,5,0)  #즐겨찾기
  # randClick(310,310,10,10,0)  #마을 클릭
  # result_2=img_search_utils.searchImg('teleport.png',beforeDelay=0, afterDelay=0, _region=(1415, 855, 300, 150))
  # if(result_2==0):
  #   return 0, "순간이동 실패"
  # randClick(1075,670,10,10,2) #확인

  # result=img_search_utils.searchImg('chk.png',beforeDelay=0, afterDelay=0, chkCnt=10, justChk=True, _region=(880, 40, 200, 150), accuracy=0.7)
  # if(result==0):
  #   return 0, "체크 실패"
  
  # keyboard('2') #순간이동
  # time.sleep(2)

  # result=img_search_utils.searchImg('chk.png',beforeDelay=0, afterDelay=0, chkCnt=10, justChk=True, _region=(880, 40, 200, 150), accuracy=0.7)
  # if(result==0):
  #   return 0, "체크 실패"
  
  # keyboard('f') #사냥

  return 1, "message:None"

def postBox(sio, data,btn_name, character_name):
  keyboard(",") #메뉴

  randClick(1570,920,10,10,2) #모두받기
  randClick(1570,920,10,10,0) #확인

  escKey()  #우편 나가기

  return 1, "message:None"

#---------던전---------#
def dungeon(sio, data, btn_name, character_name):
  coord=data
  charging=data[4]
  name=character_name
  
  if btn_name=="칼바람":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    keyboard("`") #던전
    #던전 메뉴 진입 후에 칼바람을 클릭을 못하는대 왜그러지?? 이미지 서치 실패인가 그냥 딜레이 문제는 아니고
    result=img_search_utils.searchImg('kal_dun.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "칼바람 클릭 실패"

    randClick(coord[0],coord[1],coord[2],coord[3],2)  #층 클릭

    randClick(1500,920,10,10,0) #순간이동
    
    result=img_search_utils.searchImg('confirm.png',beforeDelay=0, afterDelay=4, _region=(950, 625, 300, 130))
    if(result==0):
      return 0, "확인 실패"

    #이동 완료 체크
    result=img_search_utils.searchImg('chk.png',beforeDelay=0, afterDelay=0, chkCnt=10, justChk=True, _region=(880, 40, 200, 150), accuracy=0.7)
    if(result==0):
      return 0, "체크 실패"
    
    keyboard('2') #순간이동
    time.sleep(3)
    keyboard('f') #사냥

  elif btn_name=="곤신전":
    for i in range(charging):
      keyboard("1")
      time.sleep(2)

    keyboard("`") #던전

    result=img_search_utils.searchImg('gon_dun.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "곤신전 클릭 실패"

    randClick(coord[0],coord[1],coord[2],coord[3],2)  #층 클릭

    randClick(1500,920,10,10,0) #순간이동
    
    result=img_search_utils.searchImg('confirm.png',beforeDelay=0, afterDelay=4, _region=(950, 625, 300, 130))
    if(result==0):
      return 0, "확인 실패"

    #이동 완료 체크
    result=img_search_utils.searchImg('chk.png',beforeDelay=0, afterDelay=0, chkCnt=10, justChk=True, _region=(880, 40, 200, 150), accuracy=0.7)
    if(result==0):
      return 0, "체크 실패"
    
    keyboard('2') #순간이동
    time.sleep(3)
    keyboard('f') #사냥

  elif btn_name=="어둠실험":
    for i in range(charging):
      keyboard("1")
      time.sleep(2)

    keyboard("`") #던전

    result=img_search_utils.searchImg('dark_dun.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "어둠실험 클릭 실패"

    randClick(coord[0],coord[1],coord[2],coord[3],2)  #층 클릭

    randClick(1500,920,10,10,0) #순간이동
    
    result=img_search_utils.searchImg('confirm.png',beforeDelay=0, afterDelay=4, _region=(950, 625, 300, 130))
    if(result==0):
      return 0, "확인 실패"

    #이동 완료 체크
    result=img_search_utils.searchImg('chk.png',beforeDelay=0, afterDelay=0, chkCnt=10, justChk=True, _region=(880, 40, 200, 150), accuracy=0.7)
    if(result==0):
      return 0, "체크 실패"
    
    # keyboard('2') #순간이동
    # time.sleep(3)
    # keyboard('f') #사냥

  elif btn_name=="도서관":
    for i in range(charging):
      keyboard("1")
      time.sleep(2)

    keyboard("`") #던전

    result=img_search_utils.searchImg('library.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "도서관 클릭 실패"

    randClick(coord[0],coord[1],coord[2],coord[3],2)  #층 클릭

    randClick(1500,920,10,10,0) #순간이동
    
    result=img_search_utils.searchImg('confirm.png',beforeDelay=0, afterDelay=4, _region=(950, 625, 300, 130))
    if(result==0):
      return 0, "확인 실패"

    #이동 완료 체크
    result=img_search_utils.searchImg('chk.png',beforeDelay=0, afterDelay=0, chkCnt=10, justChk=True, _region=(880, 40, 200, 150), accuracy=0.7)
    if(result==0):
      return 0, "체크 실패"
    
    # keyboard('2') #순간이동
    # time.sleep(3)
    keyboard('f') #사냥

  elif btn_name=="렐름던전":
    for i in range(charging):
      keyboard("1")
      time.sleep(2)

    keyboard("`") #던전
    randClick(600,145,5,5,0)  #렐름던전 클릭

    result=img_search_utils.searchImg('fire.png',beforeDelay=2, afterDelay=1)
    if(result==0):
      return 0, "렐름던전 클릭 실패"

    randClick(coord[0],coord[1],coord[2],coord[3],2)  #층 클릭

    randClick(1500,920,10,10,0) #순간이동
    
    result=img_search_utils.searchImg('confirm.png',beforeDelay=0, afterDelay=4, _region=(950, 625, 300, 130))
    if(result==0):
      return 0, "확인 실패"

    #이동 완료 체크
    result=img_search_utils.searchImg('chk.png',beforeDelay=0, afterDelay=0, chkCnt=10, justChk=True, _region=(880, 40, 200, 150), accuracy=0.7)
    if(result==0):
      return 0, "체크 실패"
    
    # keyboard('2') #순간이동
    time.sleep(3)
    keyboard('f') #사냥

  elif btn_name=="이벤트던전":
    print(f"{btn_name} 실행") #임시

    keyboard("`") #던전
    # result=img_search_utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭

    result=img_search_utils.searchImg('eventDun.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "이벤트던전 클릭 실패"

    result=img_search_utils.searchImg('dungeon_enter.png', beforeDelay=0, afterDelay=0, _region=(1200, 750, 400, 150))  #입장하기
    if(result==0):
      return 0, "이벤트 입장 클릭 실패"
    randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭 (설정 해줘야함 json에서)
    randClick(1050,650,5,5,0)

    keyboard('6') #순간이동

  img_search_utils.caputure_image(name, 227, 285, sio) #name, x, y, sio

  return 1, "message:None"

#---------아이템 변경---------#
def switch_get_item(sio, data, btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("x") #환경설정
  result=img_search_utils.searchImg('setting_get_btn.png', beforeDelay=1, afterDelay=1, _region=(355,370,200,200))
  if(result==0):
    return 0, "세팅 획득 버튼클릭 실패"
  
  if btn_name=="모두":
    result=img_search_utils.searchImg('allItem.png', beforeDelay=1, afterDelay=1, _region=(1210,360,200,150))
    if(result==0):
      return 0, "모두 클릭 실패"
    
    img_search_utils.caputure_image(name, 1295, 400, sio) #name, x, y, sio

  elif btn_name=="고급":
    result=img_search_utils.searchImg('greenItem.png', beforeDelay=1, afterDelay=1, _region=(1015,400,200,150))
    if(result==0):
      return 0, "고급 클릭 실패"
    
    img_search_utils.caputure_image(name, 1120, 450, sio) #name, x, y, sio

  elif btn_name=="희귀":
    result=img_search_utils.searchImg('blueItem.png', beforeDelay=1, afterDelay=1, _region=(1190,400,200,150))
    if(result==0):
      return 0, "희귀 클릭 실패"
    
    img_search_utils.caputure_image(name, 1280, 450, sio) #name, x, y, sio

  escKey()  #나가기
  return 1, "message:None"

def decomposeItemOn(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("i") 
  time.sleep(1)

  randClick(1500,800,5,5,0.5) #분해 
  randClick(1560,750,10,10,0.5) #분해 세팅
  randClick(1290,555,5,5,0) #분해ON
  

  result=img_search_utils.searchImg('confirm.png', beforeDelay=0, afterDelay=1, chkCnt=2, _region=(950,580,300,200))
  if(result==0):
    return 0, "분해세팅 실패"

  return 1, "message:None"

def decomposeItemOff(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("i") 
  time.sleep(1)

  randClick(1500,800,5,5,0.5) #분해 
  randClick(1560,750,10,10,0.5) #분해 세팅
  randClick(1190,555,5,5,0) #분해OFF
  

  result=img_search_utils.searchImg('confirm.png', beforeDelay=0, afterDelay=1, chkCnt=2, _region=(950,580,300,200))
  if(result==0):
    return 0, "분해세팅 실패"

  return 1, "message:None"
  
def deathChk(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
  img_search_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=1, chkCnt=2, _region=(920,580,300,200))

  img_search_utils.caputure_image(name, 1145, 195, sio) #name, x, y, sio

  return 1, "message:None"

def showDiamond(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard('x')
  # Box(left=880, top=196, width=25, height=27)
  result_1=img_search_utils.searchImg('diamondChk_1.png', beforeDelay=1, afterDelay=0, justChk=True, _region=(840,180,100,60), accuracy=0.7)
  result_2=img_search_utils.searchImg('diamondChk_2.png', beforeDelay=0, afterDelay=0, justChk=True, _region=(920,180,80,60), accuracy=0.7)
  
  if result_1!=0 and result_2!=0:
    x=result_1.left+result_1.width
    capture_width=result_2.left-x #끝나는 x좌표는 고정정
    y, height = 190, 35 
    config="--psm 7 -c tessedit_char_whitelist=0123456789,"
    binary_val=150

    text=img_search_utils.capture_text_from_region(x, y, capture_width, height, config,binary_val)
    if text[0]==0:  #capture_text_from_region 예외 발생
      return 1, text[1] 
    numbers = ''.join(re.findall(r'\d+', re.sub(r"[.,]", "", text[0])))  #문자와 , . 제거 후 숫자만 남김김
    diamond=numbers
  else:
    return 0, "다이아 이미지서치 실패"
  
  escKey()  #나가기

  return 3, diamond

def useItem(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
  
  keyboard('i') #인벤토리
  randClick(1520,735,5,5,0) 
  randClick(1450,520,10,5,0)  #일괄사용 클릭

  randClick(1305,680,5,5,0)
 
  randClick(1405,740,5,5,10) 

  return 1, "message:None"

def agasion(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("i")
  randClick(1220,460,5,5,0) #왼쪽 메뉴 클릭

  while True:
    randClick(1290,505,5,5,0) #첫 번째 카드 클릭
    randClick(1290,505,5,5,1)
    result=img_search_utils.searchImg('agasionFirstChk.png', beforeDelay=1, afterDelay=1, justChk=True, _region=(800,750,300,200))
    if(result==0):
      break
    for j in range(30):
      keyboard("y")
      time.sleep(1)
      keyboard("y")
      result=img_search_utils.searchImg('agasionExit.png', beforeDelay=1, afterDelay=1, chkCnt=3,_region=(830,775,300,140))
      if(result==1):
        break

  return 1, "message:None"

def itemDelete(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard('v')
  img_search_utils.searchImg('stop_schedule.png',beforeDelay=1, afterDelay=0, chkCnt=2, _region=(1260,790,300,100))
  
  escKey()  #나가기

  keyboard("i")
  randClick(1225,405,5,5,0)

  randClick(1365,355,5,5,0) #순간이동
  randClick(1305,740,5,5,0)
  randClick(1030,705,5,5,0)
  randClick(1055,655,5,5,0)

  randClick(1295,355,5,5,0) #물약
  randClick(1305,740,5,5,0)
  randClick(1030,705,5,5,0)
  randClick(1055,655,5,5,2)

  randClick(1295,425,5,5,0) #초록물약
  randClick(1305,740,5,5,0)
  randClick(1030,705,5,5,0)
  randClick(1055,655,5,5,2)

  result=img_search_utils.searchImg('chk.png', beforeDelay=1, afterDelay=1, justChk=True, chkCnt=10,_region=(910,180,230,70))
  if(result==0):
    return 0, "아이템 삭제 실패"
  
  return 1, "message:None"

def paper(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
  
  keyboard("i")
  randClick(1225,405,10,10,0)
  randClick(1439,355,10,10,0)
  randClick(1373,737,5,5,0)
  result=img_search_utils.searchImg('paper_make.png', beforeDelay=1, afterDelay=1, _region=(1255,488,200,100))
  if(result==0):
    return 0, "신탁서 제작 클릭 실패"

  randClick(1230,475,5,5,2)

  for i in range(6):
    randClick(630,345,10,10,0)
    randClick(1050,825,5,5,0) #max클릭
    randClick(1450,825,10,10,1) #제작클릭

    result=img_search_utils.searchImg('createCancel.png', beforeDelay=1, afterDelay=1, justChk=True, _region=(1340,765,300,200))
    if(result==0):
      break
    time.sleep(3)
    randClick(945,820,10,10,1)
    randClick(945,820,10,10,0)

  escKey()  #나가기
  
  return 1, "message:None"

def event_store(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard('7')
  
  result=img_search_utils.searchImg('event_store1.png', beforeDelay=1, afterDelay=3, chkCnt=10)  
  if(result==0):
    return 0, "이벤트상점 클릭 실패"
    
  result=img_search_utils.searchImg('dailyProduct.png', beforeDelay=1, afterDelay=1, chkCnt=30)  
  if(result==0):
    return 0, "일일상품담기 실패"
  
  # for i in range(8):
  #   randClick(490,465,10,10,0)

  randClick(1475,830,5,5,0) #구매 결정
  randClick(1050,650,5,5,0) 
  escKey()

  # result=img_search_utils.searchImg('event_store2.png', beforeDelay=1, afterDelay=3, chkCnt=10)  
  # if(result==0):
  #   return 0, "이벤트상점 클릭 실패"
    
  # result=img_search_utils.searchImg('dailyProduct.png', beforeDelay=1, afterDelay=1, chkCnt=30)  
  # if(result==0):
  #   return 0, "일일상품담기 실패"
  
  # # for i in range(8):
  # #   randClick(490,465,10,10,0)

  # randClick(1475,830,5,5,0) #구매 결정
  # randClick(1050,650,5,5,0) 
  # escKey()

  result=normalHunting(sio, data,btn_name, character_name)
  return result

#거리 40M
def fourty(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("x") #환경설정

  result=img_search_utils.searchImg('fourty_meter.png', beforeDelay=1, afterDelay=1, _region=(1065,710,550,200)) 
  if(result==0):
    return 0, "40M 클릭 실패"

  img_search_utils.caputure_image(name, 1300, 720, sio) #name, x, y, sio

  escKey()  #나가기

  return 1, "message:None"

#거리 제한없음
def unlimit(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("x") #환경설정
  

  result=img_search_utils.searchImg('unlimit_meter.png', beforeDelay=1, afterDelay=1, _region=(1065,710,550,200)) 
  if(result==0):
    return 0, "제한없음 클릭 실패"

  img_search_utils.caputure_image(name, 1450,720, sio) #name, x, y, sio

  escKey()  #나가기

  return 1, "message:None"

#데일리 출석 루틴
def daily(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name

  keyboard("/") #출석

  x=280
  for i in range(2):
    randClick(x,150,10,10,0)
    result=img_search_utils.searchImg('daily_chk.png', beforeDelay=1, afterDelay=1.5, _region=(1145,760,400,200)) 
    if(result==0):
      return 0, "출석 체크 실패"
    randClick(1315,835,10,10,0) #보상 클릭
    x+=200
 
  #데일리 나가기
  escKey()

  return 1, "message:None"

#혈맹 출석 루틴
def guild(sio, _donation_cnt,btn_name, character_name):
  donation_cnt=_donation_cnt
  name=character_name
  keyboard('.')

  randClick(280,920,10,10,1.5)  #출석보상 클릭
  randClick(280,920,10,10,0.5)  #출석보상 

  randClick(300,860,10,10,0)  #기부 클릭

  for i in range(donation_cnt):
    result=img_search_utils.searchImg('donation.png', beforeDelay=0.5, afterDelay=1,_region=(480,675,400,150)) 
    if(result==0):
      return 0, "일괄구매 실패"
    randClick(590,730,10,10,0)

  escKey()
  escKey()

  return 1, "message:None"

def store(sio, data,btn_name, character_name):
  coord=data
  delay=data[4]
  name=character_name
  #상점 클릭
  keyboard('u')
  
  result=img_search_utils.searchImg('exchange.png', beforeDelay=1, afterDelay=1, _region=(220,110,1000,150)) 
  if(result==0):
    return 0, "교환소 클릭 실패"

  result=img_search_utils.searchImg('exchange_all_buy.png', beforeDelay=0, afterDelay=1, _region=(160,885,300,150)) 
  if(result==0):
    return 0, "일괄구매 클릭 실패"
  
  randClick(1077,752,10,10,0) #확인

  #상점 나가기
  escKey()

  return 1, "message:None"

#------------모닝 루틴------------#
def morning(sio, data,btn_name, character_name):
  coord=data
  donation_cnt=data[4]
  name=character_name

  # 데일리 
  daily(sio, data,btn_name, character_name)

  # 혈맹 
  result_1=guild(sio, donation_cnt, btn_name, character_name)
  if(result_1[0]==0):
    return result_1[0], result_1[1]
  
  #상점
  result_2=store(sio, data,btn_name, character_name)
  if(result_2[0]==0):
    return result_2[0], result_2[1]

  img_search_utils.caputure_image(name, 387,258, sio) #name, x, y, sio

  return 1, "message:None"

def seasonpass(sio, data,btn_name, character_name):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("z") #시즌패스
  time.sleep(2)

  x_coord=700
  for i in range(cnt):
    while(True):
      result=img_search_utils.searchImg('getSeason.png', beforeDelay=0, afterDelay=1,_region=(1110,330,350,150))
      if(result==0):
        randClick(1325,825,10,10,0)
        result=img_search_utils.searchImg('confirm.png', beforeDelay=1, afterDelay=0, _region=(920,580,300,200))
        randClick(x_coord,280,30,10,1)
        break
    x_coord=x_coord+240
    
   
  img_search_utils.caputure_image(name, 1175,365, sio) #name, x, y, sio
  
  escKey()  #나가기

  return 1, "message:None"

def make_item(sio, data, btn_name, character_name):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("-") #제작
  time.sleep(2)

  result=img_search_utils.searchImg('armor.png', beforeDelay=0, afterDelay=1,_region=(475,215,500,150))
  if(result==0):
    return 0, "방어구 클릭 실패"
  
  result=img_search_utils.searchImg('half_plate.png', beforeDelay=0, afterDelay=1,_region=(480,270,400,300))
  if(result==0):
    return 0, "플레이트 클릭 실패"

  for i in range(cnt):
    randClick(1260,825,5,5,0)
  
  result=img_search_utils.searchImg('make.png', beforeDelay=0, afterDelay=6,_region=(1315,745,250,200))
  if(result==0):
    return 0, "제작 클릭 실패"
  
  result=img_search_utils.searchImg('white_confirm.png', beforeDelay=0, afterDelay=1, chkCnt=10, _region=(830,735,250,200))
  if(result==0):
    return 0, "제작 클릭 실패"
  
  escKey()  #나가기

  return 1, "message:None"

def party(sio, data,btn_name, character_name):
  coord=data
  cnt=data[4]
  name=character_name

  result=img_search_utils.searchImg('enter_party.png', beforeDelay=0, afterDelay=1, _region=(380,290,200,100))  #파티생성 여부 체크 및 참여
  if(result==0):
    keyboard('e') #파티
    randClick(350,360,2,2,0.5)  #6인
    randClick(728,408,2,2,0.5)  #랜덤
    randClick(482,452,2,2,0.5)  #균등
    result=img_search_utils.searchImg('party.png',beforeDelay=0, afterDelay=0.5, _region=(400, 640, 250, 100)) #파티 생성
    if(result==0):
      return 0, "파티 생성 실패"
    randClick(328,574,5,5,0.5)  #파티초대
    randClick(360,170,5,5,1)  #친구
    _y = 235
    for _ in range(5):
        randClick(445, _y, 10, 10, 1)
        _y += 65

  return 1, "message:None"

def unparty(sio, data,btn_name, character_name):
  coord=data
  cnt=data[4]
  name=character_name

  randClick(865,480,30,30,0)  #전리품 확인 클릭

  y=560
  keyboard("t") #파티
  for i in range(4):
    randClick(970,y,5,5,0)
    result=img_search_utils.searchImg('unparty.png',beforeDelay=0, afterDelay=0, _region=(980, 480, 300, 400))
    if(result==1):
      break
    y=y+60

  result=normalHunting(sio, data, btn_name, character_name)
  return result

def party_dungeon(sio, data, btn_name, character_name):
  coord=data
  charging=data[4]
  name=character_name

  keyboard("`") #던전
  # result=utils.searchImg('favorite.png', beforeDelay=1, afterDelay=1,  _region=(700, 230, 800, 120))  #즐겨찾기 클릭
  result=img_search_utils.searchImg('party.png',beforeDelay=0, afterDelay=0, _region=(630, 230, 400, 100))
  if(result==0):
    return 0, "파티클릭 실패"
  
  if btn_name=="봉인사원":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    result=img_search_utils.searchImg('sealing_temple.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "봉인의 사원 클릭 실패"

  elif btn_name=="카이트해적":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    result=img_search_utils.searchImg('kite_pirates.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "카이트해적 클릭 실패"
    
  elif btn_name=="네뷸라이트":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    result=img_search_utils.searchImg('nebul.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "네뷸라이트 클릭 실패"
    
  elif btn_name=="회색제단":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    dragValues={'fromStartX':680, 'toStartX':980,'fromStartY':650,'toStartY':750,'fromEndX':680, 'toEndX':980,'fromEndY':120,'toEndY':160}
    serial_comm.mouseDrag(dragValues)
    time.sleep(2)   

    result=img_search_utils.searchImg('gray_ash.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "회색제단 클릭 실패"
    
  elif btn_name=="최후정원":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    result=img_search_utils.searchImg('last_garden.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "최후정원 클릭 실패"
    
  elif btn_name=="케트라":
    for i in range(charging):
      keyboard("2")
      time.sleep(2)

    dragValues={'fromStartX':680, 'toStartX':980,'fromStartY':650,'toStartY':750,'fromEndX':680, 'toEndX':980,'fromEndY':120,'toEndY':160}
    serial_comm.mouseDrag(dragValues)
    time.sleep(2)

    result=img_search_utils.searchImg('ketra.png',beforeDelay=1, afterDelay=1)
    if(result==0):
      return 0, "케트라 클릭 실패"

  result=img_search_utils.searchImg('request_enter.png', beforeDelay=0, afterDelay=1, _region=(1200, 750, 400, 150))  #입장신청
  if(result==0):
    return 0, f"{btn_name} 입장 클릭 실패"
  
  randClick(coord[0],coord[1],coord[2],coord[3],1)  #층 클릭
  result=img_search_utils.searchImg('confirm_enter.png', beforeDelay=0, afterDelay=1, _region=(880, 570, 320, 200))  #입장신청
  if(result==0):
    return 0, f"{btn_name} 입장신청 확인 실패"

  return 1, "message:None"

def go_home(sio, data, btn_name, character_name):
  coord=data
  charging=data[4]
  name=character_name
  
  img_search_utils.caputure_image(name, 355, 410, sio) #name, x, y, sio

  keyboard('7') #귀환
  result=img_search_utils.searchImg('chk.png', beforeDelay=5, afterDelay=0, justChk=True, chkCnt=10,_region=(910,180,230,70))
  if(result==0):
    return 0, f"{btn_name} 이동 실패"
  
  keyboard('f') #자동사냥

  return 1, "message:None"

def class_add(sio, data, btn_name, character_name):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("l") #클래스 합성
  time.sleep(2)

  result=img_search_utils.searchImg('class_add.png', beforeDelay=0, afterDelay=3,_region=(360,240,700,100))
  if(result==0):
    return 0, "합성 클릭 실패"

  for i in range(cnt):
    keyboard("y")
    time.sleep(1)
  
  escKey()
  time.sleep(1)
  escKey()  #나가기

  return 1, "message:None"

def aga_add(sio, data, btn_name, character_name):
  coord=data
  cnt=data[4]
  name=character_name

  keyboard("q") #아가시온 합성
  time.sleep(2)

  result=img_search_utils.searchImg('class_add.png', beforeDelay=0, afterDelay=3,_region=(360,240,700,100))
  if(result==0):
    return 0, "합성 클릭 실패"

  for i in range(cnt):
    keyboard("y")
    time.sleep(1)
  
  escKey()
  time.sleep(1)
  escKey()  #나가기

  return 1, "message:None"





  
