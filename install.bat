@echo off
mkdir %APPDATA%\Todo-app
cd %APPDATA%\Todo-app
cls
python --version >nul
IF %errorlevel% equ 0 (
	goto installed
)
cls
echo "Python is not installed, please refer to: https://www.python.org/downloads/"
set /p temp=
exit
:installed
curl https://raw.githubusercontent.com/jak0ub/Todo-app/main/installer.py -o installer.py
python -m ensurepip --upgrade
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
py get-pip.py
pip install pywin32
python installer.py
