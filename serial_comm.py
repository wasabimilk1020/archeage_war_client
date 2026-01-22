import serial
import time
import random
import json
import os
import utils

ser=None

cfg=utils.load_json("client_config.json","config_json")

def connect_serial():
  global ser
  try:
    if ser is None or not ser.is_open:
      ser = serial.Serial(cfg["serial_port"], cfg.get("serial_baudrate", 9600), timeout=0.1)
      time.sleep(0.5)  # 아두이노 리셋 대기
      print("Serial connected")
  except Exception as e:
    print("Serial connect failed:", e)
    ser=None

def close_serial():
  global ser
  try:
    if ser and ser.is_open:
      print("시리얼 닫힘")
      ser.close()
  except Exception as e:
    print("close_serial error:", e)
  finally:
    ser = None

def send_and_wait(cmd, timeout=3.0):
    global ser

    if ser is None or not ser.is_open:
      print("send and wait")
      connect_serial()

    # 버퍼 정리
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # 전송
    ser.write((cmd + "\n").encode())

    # ACK 대기
    start = time.time()
    while True:
      if ser.in_waiting:
        line = ser.readline().decode(errors="ignore").strip()
        if line == "ACK":
          return True  # 성공
      if time.time() - start > timeout:
        raise Exception("Arduino ACK timeout")

# 랜덤 클릭
def randClick(xVal, yVal, xRange, yRange, clkSleep):
  global ser

  try:
    if ser is None or not ser.is_open:
      print("randClick")
      connect_serial()
        
    randX = random.randint(xVal, xVal + xRange)
    randY = random.randint(yVal, yVal + yRange)

    val = f'1!{randX}!{randY}'
    send_and_wait(val)
    
    time.sleep(clkSleep)
  except Exception as e:
    print("Error:", e)
    # 통신 문제 발생 시 포트 리셋
    try:
      if ser:
        ser.close()
    except:
      pass
    ser = None


def randClickRight(xVal, yVal, xRange, yRange, clkSleep):
    try:
        if not ser.is_open:
            ser.open()

        xRange = xVal + xRange
        yRange = yVal + yRange
        if xVal < xRange:
            fromX = xVal
            toX = xRange
        else:
            fromX = xRange
            toX = xVal

        if yVal < yRange:
            fromY = yVal
            toY = yRange
        else:
            fromY = yRange
            toY = yVal

        randX = str(random.randint(fromX, toX))
        randY = str(random.randint(fromY, toY))

        val = f'11!{randX}!{randY}'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break

        time.sleep(clkSleep)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.is_open:
            ser.close()
    return

# 마우스 드래그
def mouseDrag(dragValues):
  global ser

  try:
    if ser is None or not ser.is_open:
      print("mouseDrag")
      connect_serial()
        
    randStartX = str(random.randint(dragValues['fromStartX'], dragValues['toStartX']))
    randStartY = str(random.randint(dragValues['fromStartY'], dragValues['toStartY']))
    randEndX = str(random.randint(dragValues['fromEndX'], dragValues['toEndX']))
    randEndY = str(random.randint(dragValues['fromEndY'], dragValues['toEndY']))
  
    val = f'2!{randStartX}!{randStartY}!{randEndX}!{randEndY}'
    send_and_wait(val)
    
  
  except Exception as e:
    print("Error:", e)
    # 통신 문제 발생 시 포트 리셋
    try:
      if ser:
        ser.close()
    except:
      pass
    ser = None

# 키보드 입력
def keyboard(input):
  global ser

  try:
    if ser is None or not ser.is_open:
      print("keyboard")
      connect_serial()

    val = f'3!{input}'
    send_and_wait(val)
    
  except Exception as e:
    print("Error:", e)
    # 통신 문제 발생 시 포트 리셋
    try:
      if ser:
        ser.close()
    except:
      pass
    ser = None

# 첫 마우스 사용 시
def startClick(xVal, yVal, xRange, yRange, clkSleep):
  global ser

  try:
    if ser is None or not ser.is_open:
      print("startClick")
      connect_serial()
        
    xRange = xVal + xRange
    yRange = yVal + yRange
    if xVal < xRange:
        fromX = xVal
        toX = xRange
    else:
        fromX = xRange
        toX = xVal
    if yVal < yRange:
        fromY = yVal
        toY = yRange
    else:
        fromY = yRange
        toY = yVal

    randX = str(random.randint(fromX, toX))
    randY = str(random.randint(fromY, toY))
    val = f'5!{randX}!{randY}'
    send_and_wait(val)
  except Exception as e:
    print("Error:", e)
    # 통신 문제 발생 시 포트 리셋
    try:
      if ser:
        ser.close()
    except:
      pass
    ser = None

# WIN+b
def winKey():
    try:
        if not ser.is_open:
            print("오픈!")
            ser.open()

        val = f'7'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.is_open:
            ser.close()
            print("포트 닫힘")
    return

def winKey_1():
    try:
        if not ser.is_open:
            print("오픈!")
            ser.open()

        val = f'10'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.is_open:
            ser.close()
            print("포트 닫힘")
    return

def escKey():
    try:
        if not ser.is_open:
            ser.open()

        val = f'9'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.is_open:
            ser.close()
    return

def enterKey():
    try:
        if not ser.is_open:
            ser.open()

        val = f'6'
        val = val.encode('utf-8')
        ser.flushOutput()
        ser.flushInput()
        ser.write(val)
        ser.flush()

        # 완료확인
        while True:
            if ser.in_waiting > 0:
                ret = ser.readline()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.is_open:
            ser.close()
    return

def win_left():
    try:
      if not ser.is_open:
          ser.open()
      val=f'8'
      val=val.encode('utf-8')
      ser.flushOutput()
      ser.flushInput()
      ser.write(val)
      ser.flush()
      # 완료확인
      while True:
          if ser.in_waiting > 0:
              ret = ser.readline()
              break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.is_open:
            ser.close()
    return
  