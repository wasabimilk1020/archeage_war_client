import time
import win32gui
import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")
from serial_comm import *
import re

# 현재 실행중인 윈도우 핸들 목록 가져오기
def get_lin2m_hwnd_list():
  lin2m_handle_list=[]  #린2m 핸들 리스트

  def callback(_hwnd, _result: list):
    title = win32gui.GetWindowText(_hwnd)
    if win32gui.IsWindowEnabled(_hwnd) and win32gui.IsWindowVisible(_hwnd) and title is not None and len(title) > 0:
      _result.append(_hwnd)
    return True
  hwnd_list = []  #윈도우 핸들 리스트트
  win32gui.EnumWindows(callback, hwnd_list)
  
  for hwnd in hwnd_list:
    title = win32gui.GetWindowText(hwnd).strip()
    if title.startswith("ArcheAge") and "런처" not in title:
        lin2m_handle_list.append(hwnd)
  return lin2m_handle_list

# def get_account_list(sio):
#   account_dict={} #{"아이디":handle value}
#   lin2m_handle_list=get_lin2m_hwnd_list()

#   for lin2m_hwnd in lin2m_handle_list:
#     client_utils.getWindow(lin2m_hwnd)
#     name_server_list=[]
       
#     dragValues={'fromStartX':900, 'toStartX':1015,'fromStartY':590,'toStartY':620,'fromEndX':860, 'toEndX':1000,'fromEndY':325,'toEndY':345}
#     mouseDrag(dragValues)
#     time.sleep(2)   #실제로는 열렸는지 확인하는 코드 넣어야됨

#     keyboard('x')
  
#     result=client_utils.searchImg('information.png',beforeDelay=1, afterDelay=1, _region=(1330, 225, 200, 100))
#     if(result==0):
#       print("정보 클릭 실패")
#       continue
#       #서버에 실패를 보낼 방법이 없네 이름이 아직 없는 상태라서...
    
#     coords=[[1200, 345, 130, 50],[1220,470,100,35]]
#     for coord in coords:
#       x, y, width, height = coord
#       config="--psm 7 -c preserve_interword_spaces=1"
#       binary_value=130

#       # 문자 추출 실행
#       for i in range(3):
#         extracted_text = client_utils.capture_text_from_region(x, y, width, height, config,binary_value)
#         if extracted_text[0] != "":  #성공
#           if(extracted_text[0]!=0):
#             name_server_list.append(extracted_text[0].split(' ')[0].strip())
#           break
#         elif extracted_text[0]=="":
#           print("이름 추출 실패")
#         time.sleep(1)

#     if extracted_text[0]==0:
#       continue
    
#     name=name_server_list[0]
#     server=name_server_list[1]
#     server_and_name=f"({server}) {name}"
  
#     account_dict[server_and_name]=lin2m_hwnd
      
#     escKey() 
#     #절전모드
#     keyboard('g')
#     randClick(960,535,20,20,1)
#     sio.emit("logEvent",["어카운트 완료", name, 1])

#   return account_dict

def get_account_list(sio):
  account_dict = {}  # {"아이디1": hwnd}
  lin_handles = get_lin2m_hwnd_list()
  
  count = 1
  for hwnd in lin_handles:
      raw_title = win32gui.GetWindowText(hwnd)
      new_title = f"{raw_title}_{count}"   # 예: "카발RED_1"
      account_dict[new_title] = hwnd
      count += 1
  return account_dict
