import os
from datetime import datetime, date
import sys

def clear():
    os.system("cls")

def menu():
    clear()
    end = input("\t\tMENU\t\t\n\n|1| -> |Show all weeks|\n|2| -> |Show top 10 tasks|\n|3| -> |Search for specific task|\n|4| -> |Today's tasks|\n|5| -> |Edit planned tasks|\n|6| -> |Edit template|\n|q| -> |Quit|\n$~ ")
    clear()
    return end
def init():
    try:
        with open("toDo.cfg.next", "r", encoding="utf-8") as file:
            file.readlines()
    except FileNotFoundError:
        with open("toDo.cfg.next", "w", encoding="utf-8") as file:
            file.write("1;\n2;\n3;\n4;\n5;\n6;\n7;")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    now = datetime.now()
    year = int(str(now).split(" ")[0].split("-")[0])
    month = int(str(now).split(" ")[0].split("-")[1])
    day = str(now).split(" ")[0].split("-")[2]
    weekday = days[now.weekday()]
    return year, month, day, weekday, days
def get_days_info(year, month, days, weekday, day):
    with open("start.cfg", "r", encoding="utf-8") as file:
        line = str(file.readlines()[0])
    count = date(year, month, int(day)) - date(int(line.split("-")[0]),int(line.split("-")[1]),int(line.split("-")[2]))
    try:
        count = int(str(count).split(" ")[0])
    except ValueError:
        count = 0
    start_day = days[days.index(weekday) - (count % 7)]
    return count, start_day

def check_files(count):
    if count // 7 > 0:
        temp = count // 7
        error = 0
        for i in range(temp):
            try:
                with open(f".\\weeks\\{i + 1}.week.cfg", "r", encoding="utf-8") as file: file.readlines()
            except FileNotFoundError: error += 1
        if error == 1:    
            os.system(f"ren toDo.cfg {count // 7}.week.cfg & move {count // 7}.week.cfg weeks & ren toDo.cfg.next toDo.cfg")
        elif error >= 2:
            clear()
            input("Weeks missing...")
            sys.exit()

def writing_changes(days, weekday, q2, days_printed, lines, edit_file, today):
    while True:
        clear()
        print(f"Enter task name(If task is already in -> task is deleted, else the task is created)\n\t|q to quit|\n{" "*((len("        |q to quit|")-len(f"|Editing {days_printed[q2-1]}|") + 8)// 2)}|Editing {days_printed[q2-1]}|\n{"=" * len(f"{" "*((len("        |q to quit|")-len(f"|Editing {days_printed[q2-1]}|") + 8)// 2)}|Editing {days_printed[q2-1]}|")}")
        for task in lines[today].split(";")[1].split(","):
            if task.split(":")[0] != "" and task != "\n":
                print(task.split(":")[0])
        q3 = input("$~ ").strip()
        if q3.lower() == "q":
            break
        edited = False
        temp_line = lines[today].split(";")[1].split(",")
        for task in lines[today].split(";")[1].split(","):
            if task.split(":")[0].lower().strip() == q3.lower():
                edited = True
                temp_line.pop(temp_line.index(task)) 
        if edited == False:
            temp_line.append(q3)
        line = [f"{today + 1};"]
        for task in temp_line:
            if task != "\n" and task != "":
                line.append(f"{task},") 
        line[-1] = line[-1].strip() 
        if today != 6: line.append("\n")
        lines[today] = "".join(line)
        with open(edit_file, "w", encoding="utf-8") as file:
            file.write("".join(lines))


def load_weeks(count):
    num = []
    sum = []
    msg = []
    if count // 7 >= 1:
        for i in range(count // 7):
            count_tasks = 0
            try:
                with open(f".\\weeks\\{i + 1}.week.cfg", "r", encoding="utf-8") as file:
                    linos = file.readlines()
                    for lino in linos:
                        try:
                            main = lino.split(";")[1].split(",")
                            for contents in main:
                                try:
                                    if contents.split(":")[1].strip().lower() == "done":
                                        count_tasks += 1
                                        if contents.split(":")[0].strip().lower() not in sum:
                                            sum.append(contents.split(":")[0].strip().lower())
                                            num.append(1)
                                        else:
                                            num[sum.index(contents.split(":")[0].strip().lower())] += 1
                                except IndexError:
                                    pass
                        except IndexError:
                            pass
                msg.append(f"{i + 1}. Week consists of {count_tasks} done tasks")
            except FileNotFoundError:
                msg = ["Some weeks are missing..."]
                break
    return msg, num, sum

def mark_tasks(ok, tasks, listos, saved, linos):
    try:
        if int(ok.lower().split(".")[0]) <= len(tasks) and int(ok.lower().split(".")[0]) > 0:
            try:
                try:
                    if listos[int(ok) - 1].split(":")[1] == "done,":
                        listos[int(ok) - 1] = f"{listos[int(ok) - 1].split(",")[0].split(":")[0]},"
                    else:
                        listos[int(ok) - 1] = f"{listos[int(ok) - 1].split(",")[0]}:done,"
                except IndexError:
                    listos[int(ok) - 1] = f"{listos[int(ok) - 1].split(",")[0]}:done,"
                lino = "".join(listos)
                lino = f"{saved};{lino}\n"
                linos[saved - 1] = lino
                with open("toDo.cfg", "w", encoding="utf-8") as file:
                    file.writelines(linos)
            except IndexError:
                input("Index Error")
    except ValueError: pass
    #Easter egg
    for task in tasks:
        if task.split(":done")[0].lower() == ok.lower():
            try: temp = task.split(":")[1].lower()
            except IndexError: temp = ""
            if temp == "done":
                tasks[tasks.index(task)] = f"{task.split(":done")[0]},"
            else:
                tasks[tasks.index(task)] = f"{task}:done,"
            lino = ",".join(tasks)
            lino = f"{saved};{lino}\n"
            linos[saved - 1] = lino
            with open("toDo.cfg", "w", encoding="utf-8") as file:
                file.writelines(linos)

def print_today_tasks(now, listos, day, hour, q1):
    try:
        with open("toDo.cfg", "r", encoding="utf-8") as file:
            linos = file.readlines()
            print(f"{" "* ((len("|Enter number of done task to mark/unmark it as completed|") - len(f"day: {day}")) // 2)}day: {day}\n{" "* ((len("|Enter number of done task to mark/unmark it as completed|") - len(f"hour: {hour}")) // 2)}hour: {hour}\n{"=" * (len("|Enter number of done task to mark/unmark it as completed|"))}\n|Enter number of done task to mark/unmark it as completed|\n{" "*((len("|Enter number of done task to mark/unmark it as completed|") - len("|Enter q to quit|"))//2)}|Enter q to quit|\n{"=" * (len("|Enter number of done task to mark/unmark it as completed|"))}")
            for line in linos:
                line = line.strip()
                day_ = line.split(";")[0]
                if int(day_) == now.weekday() + 1:
                    saved = int(day_)
                    tasks = line.split(";")[1].split(",")
                    printed = False
                    for task in tasks:
                        if task == "":
                            tasks.pop(tasks.index(task))
                    for task in tasks:
                        if task == "" and len(tasks) <= 2:
                            break
                        listos.append(f"{task},")
                        try:
                            if task != "":      
                                one = task.split(":")[0]
                                two = task.split(":")[1]
                                if two.lower() == "done":
                                    two = "✓"
                                else:
                                    two = "✘"
                                print(f"{tasks.index(task) + 1}.{one} {two}") 
                                printed = True
                            
                        except IndexError:
                            print(f"{tasks.index(task) + 1}.{task} ✘")  
                            printed = True
                    if printed == False:
                        clear()
                        with open("template.cfg", "r", encoding="utf-8") as file:
                            lines = file.readlines()
                            try:
                                line = lines[0]
                            except IndexError:
                                line = ""
                        q1 = ""
                        if line != "":
                            q1 = input("No plan for today, do you want to apply your template?(y/n)\n$~ ")
                            if q1.lower() == "y":
                                with open("toDo.cfg", "r", encoding="utf-8") as file:
                                    lines = file.readlines()
                                    lines[now.weekday()] = f"{now.weekday()+ 1};{line.strip()}\n"
                                with open("toDo.cfg", "w", encoding="utf-8") as file:
                                    file.writelines(lines)
                                continue
                            else:
                                break
                        else:
                            input("No plan for today nor template created...")
                            break
    except FileNotFoundError: sys.exit()
    return tasks, saved, linos, listos, printed, q1


# def check_year_count(year, count): #To be done O.O
