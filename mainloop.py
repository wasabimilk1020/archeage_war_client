import win32gui
import img_search_utils
import check_hunting
from waking_from_sleep import *
from go_to_sleep import *
import copy

ERR_MSG = 0
STATUS_MSG = 1

def mainLoop(sio, btn_func, func_data, id_handle, btn_name):
  _idx=0
  dict_length=len(id_handle)-1
  for idx, (id, handle) in enumerate(id_handle):
    _idx=idx
    character_name=id
    if win32gui.IsWindow(handle):
      sio.emit("logEvent",[f"{btn_name} 시작", character_name, STATUS_MSG]) 

      return_val=img_search_utils.getWindow(handle) #윈도우 얻음
      if return_val[0]==0:
        sio.emit("logEvent",[return_val[1], character_name, ERR_MSG])
        continue 

      if btn_name !="status_check_button":
        #절전해제 및 사망체크
        if btn_name=="파티초대":
          chk_result=waking_from_sleep_and_deathChk(btn_name, 0)  #두 번째 인자 time.sleep
        else:
          chk_result=waking_from_sleep_and_deathChk(btn_name, 2)  #두 번째 인자 time.sleep
        
        if chk_result==1: #사망 체크를 수행 했는대 chk.png가 확인 안되서 실패
          sio.emit("logEvent",["페널티 체크 루틴 실패", character_name, ERR_MSG])
          continue
      
      if len(func_data) ==5:
        func_data_copy = copy.deepcopy(func_data)
        result=btn_func(sio, func_data_copy, btn_name, character_name, handle) #result[0]=성공여부, result[1]=메세지
        try:
          message=result[1]

          if result[0]==0:
            sio.emit("logEvent",[message, character_name, ERR_MSG])
          elif result[0]==1:  #일반루틴 완료메세지
            if btn_name not in ["파티"]:  
              go_to_sleep_and_huntingChk(btn_name, character_name, sio) #절전모드
          elif result[0]==2:  #statusChk 완료메세지
            sio.emit("logEvent",[f"{message} 완료", character_name, STATUS_MSG])
          elif result[0]==3:  #diamond 완료메세지
            diamond=message
            data=[]
            data.append(diamond)
            data.append(character_name)
            sio.emit("get_diamond",data)
            #절전모드
            go_to_sleep_and_huntingChk(btn_name, character_name, sio)
        except Exception as e:
          sio.emit("logEvent", [f"message result 에러: {e}", character_name, ERR_MSG])
          continue
      else:
        sio.emit("logEvent",["데이터 인덱스 에러", character_name, ERR_MSG])
        continue
    else:
      print("핸들 없음",handle)
      sio.emit("logEvent",["윈도우 없음", character_name, ERR_MSG])
      continue
  if _idx==dict_length:
    sio.emit("stop_animation",btn_name)

      
      
      


    