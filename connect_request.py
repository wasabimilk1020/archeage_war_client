import subprocess
import os

def conn_req():
  # 시작 프로그램 폴더 경로
  startup_folder = r"C:\Users\eunsu\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
  
  # 실행할 스크립트의 파일명 (예: your_script.py 또는 .bat 파일 등)
  script_name = "start_client.py"  # 또는 .bat 파일일 경우 "your_script.bat"
  
  # 전체 경로 생성
  script_path = os.path.join(startup_folder, script_name)
  
  # 스크립트 실행
  if os.path.exists(script_path):
      subprocess.run(['python', script_path])  # 파이썬 스크립트 실행
  else:
      print("스크립트가 존재하지 않습니다.")
