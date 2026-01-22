@echo off

REM 현재 위치 확인 (디버깅 끝나면 지워도 됨)
REM cd

REM 혹시 실행 중인 python 종료 (선택)
taskkill /IM python.exe /F >nul 2>&1

REM 업데이트
git fetch
git reset --hard origin/main

REM 재실행
python client.py

exit