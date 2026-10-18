@echo off
rem ============================================
rem  tasy.net 배포.bat
rem  사용법: 이 파일을 repo 폴더 안에 넣고 더블클릭
rem  (새 파일을 repo 폴더에 넣은 뒤 실행)
rem ============================================
cd /d "%~dp0"

echo [1/3] 변경 파일 수집 중...
"C:\Program Files\Git\bin\git.exe" add .

echo [2/3] 커밋 중...
"C:\Program Files\Git\bin\git.exe" commit -m "[Deploy] %date% %time%"

echo [3/3] GitHub 푸시 중... (Vercel이 자동으로 배포합니다)
"C:\Program Files\Git\bin\git.exe" push origin main

echo.
echo --------------------------------------------
echo  배포 요청 완료! 1~2분 뒤 tasy.net에서 확인하세요.
echo --------------------------------------------
pause
