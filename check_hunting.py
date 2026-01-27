import img_search_utils
import time
import re

x, y, width, height = 895,220, 130, 35 #매칭 위치

def checkHunting():
  for i in range(5):
    match_result=img_search_utils.img_matchTemplate("auto_hunting.png", x, y, width, height)
    if match_result[0]==0:  #템플릿 매칭 예외 발생
      return match_result[0], match_result[1]
    elif match_result[0] == "자동 사냥 중": #매칭 성공
      return match_result[0], ""
    time.sleep(0.3)
  return 1, "사냥 멈춰있음" #실패를 나타냄