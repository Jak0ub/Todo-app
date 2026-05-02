#!/bin/sh
cd $HOME
mkdir Todo-app
cd Todo-app
printf -- '%s\n' '#!/bin/bash' > start.sh
echo "cd $HOME/Todo-app/" > start.sh
echo "python3 $HOME/Todo-app/main.py" >> start.sh
chmod +x start.sh
touch toDo.cfg
for i in $(seq 1 7);
do
    echo "$i;" >> toDo.cfg
done
value=$(date '+%Y-%m-%d')
echo $value > start.cfg
curl https://raw.githubusercontent.com/jak0ub/Todo-app/main/main.py -o main.py
curl https://raw.githubusercontent.com/jak0ub/Todo-app/main/dll.py -o dll.py
mkdir weeks
touch template.cfg
case "$(uname -sr)" in
    Darwin*) cp $HOME/Todo-app/start.sh $HOME/Desktop/Todo-app.command;;
    *) echo ln -s start.sh ../Desktop/Todo-app;;
esac
sleep 1
exit
