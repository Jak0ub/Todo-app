#!/bin/sh
Green='\033[0;32m'
Color_Off='\033[0m'
cd $HOME
mkdir Todo-app
echo "${Green}Program directory created"
cd Todo-app
printf -- '%s\n' '#!/bin/bash' > start.sh
echo "cd $HOME/Todo-app/" > start.sh
echo "python3 $HOME/Todo-app/main.py" >> start.sh
chmod +x start.sh
echo "${Green}Script created"
touch toDo.cfg
for i in $(seq 1 7);
do
    echo "$i;" >> toDo.cfg
done
value=$(date '+%Y-%m-%d')
echo $value > start.cfg
echo "${Green}config files created"
curl https://raw.githubusercontent.com/jak0ub/Todo-app/main/main.py -o main.py
curl https://raw.githubusercontent.com/jak0ub/Todo-app/main/dll.py -o dll.py
echo "${Green}program files downloaded"
mkdir weeks
touch template.cfg
echo "${Green}Final touches"
case "$(uname -sr)" in
    Darwin*) cp $HOME/Todo-app/start.sh $HOME/Desktop/Todo-app.command;;
    *) echo ln -s start.sh ../Desktop/Todo-app;;
esac

echo "${Green}Desktop shortcut created"
sleep 1
echo "${Green}Program is ready!"
exit
