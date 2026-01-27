import pyautogui
import sys
import img_search_utils
import time
from button_func import *
import win32gui

for i in range(10):
  result=img_search_utils.img_matchTemplate("auto_hunting.png", 895,220, 130, 35)
  time.sleep(0.2)
  print("결과",result)
# img_search_utils.preprocess_image("debug_capture.png", "preprocessed_1.png")

# img_search_utils.img_matchTemplate("auto_hunting.png", 895,220, 130, 35, confidence=0.8)
# time.sleep(2)
# hwnd = win32gui.GetForegroundWindow()
# rect = win32gui.GetWindowRect(hwnd)
# print(rect)
