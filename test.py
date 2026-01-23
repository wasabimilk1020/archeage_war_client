import pyautogui
import sys
import img_search_utils
import time
from button_func import *

result=img_search_utils.searchImg('kal_dun.png',beforeDelay=1, afterDelay=1)
if(result==0):
  print("칼바람 클릭 실패")
