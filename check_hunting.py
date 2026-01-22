import img_search_utils
import time
import re

x, y, width, height = 890, 220, 130, 40 #자동 사냥 범위
config="--psm 7 -c preserve_interword_spaces=1"
binary_value=130

def checkHunting():
  for i in range(5):
    text=img_search_utils.capture_text_from_region(x, y, width, height, config, binary_value)
    if text[0]==0:  #capture_text_from_region 예외 발생
      return text[0], text[1]
    clean_text=re.sub(r"^\s+|\s+$", "", text[0])  # 정규식으로 앞뒤 공백 제거
    print(clean_text)
    if clean_text == "자동 사냥 중": #or clean_text == "퀘스트 진행 중":
      return clean_text, ""
    time.sleep(0.3)
  return 1, "사냥 멈춰있음" #실패를 나타냄