import pyautogui
import os
import time
import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")
import win32gui
import pyautogui
import datetime
import base64
import serial_comm
import utils
import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import ImageGrab,ImageEnhance,Image,ImageOps,ImageFilter

#이미지 서치
def searchImg(imgTitle, beforeDelay, afterDelay, justChk=False, coord=[], chkCnt=5, _region=(160, 35, 1600, 950), accuracy=0.85):
  full_path=utils.file_path(f"{imgTitle}","image_files")  #file, folder, sub_folder
  chkInterval=0.5
  loopCnt = 0

  while loopCnt < chkCnt:
    loopCnt += 1
    try:
      time.sleep(beforeDelay)
      result = pyautogui.locateOnScreen(full_path, region=_region, confidence=accuracy)

      if result is None:  # 이미지 찾기 실패
        time.sleep(chkInterval)
        continue

      # 이미지 찾기 성공
      if coord:  # 이미지가 아닌 다른 곳 클릭 시
        serial_comm.randClick(coord[0], coord[1], coord[2], coord[3], 0)
      elif justChk:  # 클릭 없이 이미지 체크만 할 경우
        return result
      else:  # 이미지 클릭
        serial_comm.randClick(result[0], result[1], result[2], result[3], 0)

      time.sleep(afterDelay)
      return 1
    except pyautogui.ImageNotFoundException:  #이미지 찾기 실패
      print(f"Image '{imgTitle}' not found on screen.")
      time.sleep(chkInterval)
      continue
    except Exception as e:
      print(f"An error occurred: {e}")
      return 0 
  return 0  

def caputure_image(name,x,y,sio):
  full_path=utils.file_path(f"{name}.png","image_files","capture_img")  #file, folder, sub_folder

  time.sleep(0.2)
  pyautogui.screenshot(full_path, region=(x,y,50,30))
  with open(full_path, "rb") as f:
    b64_string = base64.b64encode(f.read())
    captureImg=b64_string
  now = datetime.datetime.now()
  nowDatetime=now.strftime('%H:%M')
  data=[name, nowDatetime, captureImg] 
  sio.emit("captured_image",data)

# def getWindow(handle):
#   startClick(0,0,0,0,0)
#   time.sleep(0.1)
#   shell.SendKeys('%')
#   try:
#     win32gui.SetForegroundWindow(handle)  # 창을 앞으로 가져오기 시도
#   except Exception as e:
#     return 0, "Error bringing window to foreground"
  
#   for _ in range(10): # 최대 3초 동안 (0.3초 간격으로 10번) 창 활성화 확인
#       if win32gui.GetForegroundWindow() == handle:
#           return 1, "성공" 
#       time.sleep(0.3)  
#   return 0, "Error: Window did not come to foreground within timeout."

def getWindow(handle):
    try:
      time.sleep(0.1)
      shell.SendKeys('%')
      win32gui.SetForegroundWindow(handle)
      serial_comm.startClick(850,440,100,100,0)
    except:
      pass  # 실패해도 무시

    return 1, "성공"

def capture_text_from_region(x, y, width, height, _config, binary_val):
  binary_value=binary_val
  # 화면의 특정 영역 캡처
  bbox = (x, y, x + width, y + height)
  try:
    screenshot = ImageGrab.grab(bbox)
    # screenshot.save("origin.png")
  except Exception as e:
    return 0, f"ImageGrab 실행 중 오류 발생: {e}"
  # 크기 키우기
  scaled = screenshot.resize((screenshot.width * 2, screenshot.height * 2), Image.Resampling.LANCZOS)

  # 전처리: 흑백 변환 및 대비 증가
  grayscale = scaled.convert("L")  # 흑백 이미지로 변환
  # grayscale.save("greyscale_img.png")
  enhanced = ImageEnhance.Contrast(grayscale).enhance(2.0)  # 대비 조정
  # enhanced.save("enhanced_img.png")
  binary = enhanced.point(lambda x: 0 if x < binary_value else 255, '1')  # 이진화 처리
  # binary.save("binary_img.png")

  # 이미지 반전
  inverted_image = ImageOps.invert(binary)
  # inverted_image.save("inverted_img.png")

  # OCR로 문자 추출
  try:
    text = pytesseract.image_to_string(inverted_image, lang='kor',config=_config)  
  except Exception as e:
    return 0, f"OCR 실행 중 오류 발생: {e}"

  return text, "capture_text 성공"

def preprocess_image(temp_imgTitle, output_path):  #이미지 전처리
    input_path=utils.file_path(f"{temp_imgTitle}","image_files")  #file, folder, sub_folder

    # 이미지 로드
    template_image = cv2.imread(input_path)
    
    # 1. 그레이스케일
    gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    # 2. 대비 향상 (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)

    # 3. 샤프닝
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(contrast, -1, kernel)

    # # 4. 이진화 (Otsu Threshold)
    # _, binary = cv2.threshold(
    #     sharpened, 0, 255,
    #     cv2.THRESH_BINARY + cv2.THRESH_OTSU
    # )

    # 저장
    cv2.imwrite(output_path, sharpened)

def img_matchTemplate(temp_imgTitle, x, y, width, height, confidence=0.6):

    # 템플릿 경로
    template_path = utils.file_path(f"{temp_imgTitle}", "image_files")

    # 전처리된 템플릿 이미지 로드 (그레이로)
    template_img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template_img is None:
        raise ValueError(f"템플릿 로드 실패: {template_path}")

    # ---------- 타겟 캡처 ----------
    bbox = (x, y, x + width, y + height)
    target_pil = ImageGrab.grab(bbox)
    # target_pil.show()
    target_pil.save("debug_capture.png")

    # PIL → OpenCV
    img = cv2.cvtColor(np.array(target_pil), cv2.COLOR_RGB2BGR)

    # ---------- 타겟 전처리 ----------
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)

    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(contrast, -1, kernel)

    # _, binary = cv2.threshold(
    #     sharpened, 0, 255,
    #     cv2.THRESH_BINARY + cv2.THRESH_OTSU
    # )
    # cv2.imshow("binary", binary)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # ---------- 매칭 ----------
    try:
      result = cv2.matchTemplate(sharpened, template_img, cv2.TM_CCOEFF_NORMED) 
    except Exception as e:
      return 2, f"템플릿매칭 오류 발생: {e}"
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= confidence: #매칭 성공
      return "자동 사냥 중", "capture_text 성공"
    else: #매칭 실패
      print(max_val)
      return 0, max_val
