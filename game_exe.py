import win32gui
import img_search_utils

def start_game():
  handle=win32gui.FindWindow(None,"PURPLE")
  img_search_utils.getWindow(handle) #윈도우 얻음
  result=img_search_utils.searchImg('lineage_symbol.png',beforeDelay=0, afterDelay=0, _region=(0,0,1920,1080), accuracy=0.7)
  result=img_search_utils.searchImg('lineage_symbol_2.png',beforeDelay=0, afterDelay=0, chkCnt=2, _region=(0,0,1920,1080), accuracy=0.7)
  result=img_search_utils.searchImg('game_start_1.png',beforeDelay=2, afterDelay=0, _region=(0,0,1920,1080))
  result=img_search_utils.searchImg('purple_list_btn.png',beforeDelay=0, afterDelay=0, _region=(0,0,1920,1080))
  for i in range(6):
    result=img_search_utils.searchImg('game_start_2.png',beforeDelay=5, afterDelay=0, _region=(0,0,1920,1080))
    if result==0:
        break