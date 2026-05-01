@echo off
mkdir %APPDATA%\Todo-app
cd %APPDATA%\Todo-app
cls
python --version >nul
IF %errorlevel% equ 0 (
	goto installed_python
)
cls
echo "Python is not installed, please refer to: https://www.python.org/downloads/"
set /p temp=
exit
:installed_python
curl https://raw.githubusercontent.com/jak0ub/Todo-app/main/installer.py -o installer.py
python -m ensurepip --upgrade
pip --version
IF %errorlevel% equ 0 (
	goto installed_pip
)
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
py get-pip.py
:installed_pip
pip install pywin32
python installer.py
