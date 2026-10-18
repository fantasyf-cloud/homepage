@echo off
rem ============================================
rem  tasy.net ����.bat
rem  ����: �� ������ repo ���� �ȿ� �ְ� ����Ŭ��
rem  (�� ������ repo ������ ���� �� ����)
rem ============================================
cd /d "%~dp0"

echo [1/3] ���� ���� ���� ��...
"C:\Program Files\Git\bin\git.exe" add .

echo [2/3] Ŀ�� ��...
"C:\Program Files\Git\bin\git.exe" commit -m "[Deploy] %date% %time%"

echo [3/3] GitHub Ǫ�� ��... (Vercel�� �ڵ����� �����մϴ�)
"C:\Program Files\Git\bin\git.exe" push origin main

echo.
echo --------------------------------------------
echo  ���� ��û �Ϸ�! 1~2�� �� tasy.net���� Ȯ���ϼ���.
echo --------------------------------------------
pause
