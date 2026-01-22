import subprocess
import os
from utils import file_path
import sys

def run_git_update():
    bat_script = file_path("run_git_update.bat")

    if not os.path.exists(bat_script):
        print(f"업데이트 스크립트 없음: {bat_script}")
        return

    # 업데이트 배치 실행 (새 프로세스로)
    subprocess.Popen(["cmd.exe", "/c", bat_script])

    # 자기 자신 종료
    sys.exit()

