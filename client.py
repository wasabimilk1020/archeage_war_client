from cProfile import run
from serial import win32
import os
import socketio
import datetime
import threading
import time
from mainloop import mainLoop
import button_func
import queue
import hashlib
import base64
import get_account
import serial_comm
import json
import logging
import sys
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "computer_restart"))
# import computer_restart
import game_exe
import utils
import connect_request
import re
import code_update

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s") # 로깅 설정
last_pong_time = None # 마지막으로 pong을 받은 시간
PONG_TIMEOUT = 8  # 초 (pong 응답 대기 시간)

character_list={}

def load_json(json_file, json_folder): #file, folder
  full_path=utils.file_path(json_file, json_folder)  #file, folder, sub_folder

  try:
    with open(full_path, "r", encoding="utf-8") as f:
      return json.load(f)
  except (FileNotFoundError, json.JSONDecodeError):
    return {}  # 파일이 없거나 잘못된 JSON이면 빈 데이터 반환
  
# 작업 큐 생성
task_queue = queue.Queue()

# 작업 처리 스레드 함수
def process_tasks():
  while True:
    try:
      # 큐에서 작업 가져오기
      task = task_queue.get(timeout=10)
      if task is None:
        break  # None이 들어오면 스레드 종료
      print("클라이언트 메인루프 시작")
      # 작업 실행
      func, args = task
      func(*args)
    except queue.Empty:
      continue  # 작업이 없으면 다시 대기
    except Exception as e:
      print(f"Error processing task: {e}")
    
# 작업 처리 스레드 시작
worker_thread = threading.Thread(target=process_tasks, daemon=True)
worker_thread.start()

#웹소켓 통신
sio = socketio.Client()

@sio.event
def connect():
  global last_pong_time
  global character_list
  print('connection established')   
  character_list=utils.load_json("character_list.json","config_json")
  print("여기서 들어오나?",character_list)
  last_pong_time = time.time()  #서버가 다시 연결되었을 때 타이머 초기화 (이전 타이머 값이 남아있을 경우 방지)

  if serial_comm.ser is None or not serial_comm.ser.is_open:
    serial_comm.connect_serial()

  sio.start_background_task(monitor_connection)
  sio.start_background_task(send_ping)

@sio.event
def disconnect():
  global last_pong_time
  print("disconnet 호출! 서버와 연결 끊김")
  last_pong_time = None #퐁 타임 초기화
  if serial_comm.ser is not None and serial_comm.ser.is_open:
    # serial_comm.ser.flushInput()
    # serial_comm.ser.flushOutput()
    serial_comm.close_serial()

# @sio.event
# def reqAccount(data):
#   global character_list

#   full_path=utils.file_path("character_list.json","character_list_json")  #file, folder, sub_folder
#   def sort_key(text):
#     # 첫 번째 공백을 기준으로 앞(서버)과 뒤(아이디)를 나눔
#     server_part, id_part = text.split(" ", 1)  
#     # 정규식을 사용해 서버 번호(숫자)를 추출: "(에덴10)" → "10"
#     match = re.search(r'\d+', server_part)
#     server_number = int(match.group()) if match else 0
#     return (server_number, id_part)
  
#   accont_dict=get_account.get_account_list(sio)

#   sorted_keys = sorted(accont_dict.keys(), key=sort_key)
#   character_list = {key: accont_dict[key] for key in sorted_keys}

#   with open(full_path, "w", encoding="utf-8") as f:
#     json.dump(character_list, f, indent=4, ensure_ascii=False)
#   sio.emit("revAccount", character_list)

@sio.event
def reqAccount(data):
  global character_list

  full_path=utils.file_path("character_list.json","config_json")  #file, folder, sub_folder 
  
  accont_dict=get_account.get_account_list(sio)

  with open(full_path, "w", encoding="utf-8") as f:
    json.dump(accont_dict, f, indent=4, ensure_ascii=False)
  sio.emit("revAccount", accont_dict)

button_mapping={
  "status_check_button":button_func.statusChk,  
  "사냥":button_func.normalHunting,
  "칼바람":button_func.dungeon,
  "곤신전":button_func.dungeon,
  "어둠실험":button_func.dungeon,
  "도서관":button_func.dungeon,
  "렐름던전":button_func.dungeon,
  # "이벤트던전":button_func.dungeon,
  "모닝":button_func.morning,
  "우편":button_func.postBox,
  # "시즌패스":button_func.seasonpass,
  "분해ON":button_func.decomposeItemOn,
  "분해OFF":button_func.decomposeItemOff,
  # "스킬북분해":button_func.decomposeBook,
  # "아이템삭제":button_func.itemDelete,
  # "일괄사용":button_func.useItem,
  # "사망체크":button_func.deathChk,
  # "신탁서":button_func.paper,
  # "이벤트상점":button_func.event_store,
  # "아가시온":button_func.agasion,
  # "모두":button_func.switch_get_item,
  # "고급":button_func.switch_get_item,
  # "희귀":button_func.switch_get_item,
  # "40M":button_func.fourty,
  # "제한없음":button_func.unlimit,
  # # "바람":button_func.decomposeItem,
  # # "불":button_func.decomposeItem,
  # # "물":button_func.decomposeItem,
  # "다이아":button_func.showDiamond,
  # "제작":button_func.make_item,
  "파티":button_func.party,
  # "파티해제":button_func.unparty,
  # "귀환":button_func.go_home,
  # "봉인사원":button_func.party_dungeon,
  # "카이트해적":button_func.party_dungeon,
  # "네뷸라이트":button_func.party_dungeon,
  # "회색제단":button_func.party_dungeon,
  # "최후정원":button_func.party_dungeon,
  # "케트라":button_func.party_dungeon,
  # "클래스합성":button_func.class_add,
  # "아가합성":button_func.aga_add,

}

@sio.event
def button_schedule(data):
  global character_list
#emit_data={"버튼이름":[데이터],"character_list":{"아이디1":핸들 값1,"아이디2":핸들 값2}}
  for idx, (key, value) in enumerate(data.items()):
    if idx==0:
      button_name=key
      func_data=value
    elif idx==1:
      if  value=={}:  #statusChk
        id_handle=list(character_list.items())
      else:
        id_handle=list(value.items())
  
  # 버튼에 해당하는 함수 가져오기
  print("버튼이름: ",button_name)
  btn_func = button_mapping[button_name]

  # mainLoop 호출을 큐에 추가
  task_queue.put((mainLoop, (sio, btn_func, func_data, id_handle, button_name)))

@sio.event
def recvImage(data):
  img=data[0]
  hash_value=data[1]
  file_name=data[2]
  calculated_hash = hashlib.sha256(img.encode("utf-8")).hexdigest()

  full_path=utils.file_path(f"{file_name}","image_files")  #file, folder, sub_folder

  # 해시 확인
  if hash_value==calculated_hash: 
    image_data = base64.b64decode(img)
    # 파일로 저장
    with open(full_path, "wb") as f:
      f.write(image_data)
    for name in character_list.keys():
      sio.emit("logEvent",["이미지 저장", name, 1]) 
  else:
    print("데이터가 손상되었거나 무결성 검증 실패!")

# @sio.event
# def reboot_computer(data):
#   computer_restart.run_bat_as_admin()

@sio.event
def game_start(data):
  game_exe.start_game()

# @sio.event
# def connect_request_from_server(data):
#   connect_request.conn_req()

@sio.event
def update_code(data):
  code_update.run_git_update()

@sio.event
def pong(data):
    global last_pong_time
    # logging.info(f"Received pong from server: {data['time']}")
    last_pong_time = time.time()  # pong 수신 시 갱신

def monitor_connection():
  global last_pong_time

  while not sio.connected:  #첫 호출 시 연결상태 확인. 반드시 연결 후 아래 루프 시작하기 위해서
    time.sleep(0.01)
    continue

  while True:
    if last_pong_time and time.time() - last_pong_time > PONG_TIMEOUT:
      logging.error("서버 응답 없음, 연결 종료.")
      sio.disconnect()  # 명시적으로 연결 종료
      break
    time.sleep(1)  # 1초마다 상태 확인

def send_ping():
  while not sio.connected:  #첫 호출 시 연결상태 확인. 반드시 연결 후 아래 루프 시작하기 위해서
    time.sleep(0.01)
    continue
  
  while True:
    if not sio.connected:
      break

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sio.emit("ping", {"time": current_time})
    time.sleep(5)

#client_config.json에서 클라이언트 설정
cfg=utils.load_json("client_config.json","config_json")

server_url = cfg["server_url"]
computer_id = cfg["computer_id"]

sio.connect(f"{server_url}?computer_id={computer_id}")

sio.wait()

#절전모드 시 멈춰있으면 사냥을 하게 만들어줘야함. 지금은 그냥 "멈춰있음" 로그 발생 시키고 맘맘
