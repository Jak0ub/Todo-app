import os
from datetime import datetime, date
import sys
import platform, math

def check_os():
    platform_system = platform.system()
    return platform_system
def clear(platform_system):
    if platform_system == "Windows":
        os.system("cls")
    else:
        os.system("clear")
def menu(platform_system):
    clear(platform_system)
    end = input("\t\tMENU\t\t\n\n|1| -> |Show all weeks|\n|2| -> |Show top 10 tasks|\n|3| -> |Search for specific task|\n|4| -> |View specific date|\n|5| -> |Today's tasks|\n|6| -> |Edit planned tasks|\n|7| -> |Edit template|\n|q| -> |Quit|\n$~ ")
    clear(platform_system)
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

def check_files(count, platform_system):
    if count // 7 > 0:
        temp = count // 7
        error = 0
        os.chdir("weeks")
        for i in range(temp):
            try:
                with open(f"{i + 1}.week.cfg", "r", encoding="utf-8") as file: file.readlines()
            except FileNotFoundError: error += 1
        os.chdir("..")
        if error == 1:
            if platform_system == "Windows":    
                os.system(f"ren toDo.cfg {count // 7}.week.cfg & move {count // 7}.week.cfg weeks & ren toDo.cfg.next toDo.cfg")
            else:
                os.system(f"mv toDo.cfg {count // 7}.week.cfg & mv {count // 7}.week.cfg weeks/ & mv toDo.cfg.next toDo.cfg")
        elif error >= 2:
            clear(platform_system)
            input("Weeks missing...")
            sys.exit()

def writing_changes(q2, days_printed, lines, edit_file, today, platform_system):
    while True:
        clear(platform_system)
        print(f"Enter task name(If task is already in -> task is deleted, else the task is created)\n\t|q to quit|\n{' '*((len('        |q to quit|')-len(f'|Editing {days_printed[q2-1]}|') + 8)// 2)}|Editing {days_printed[q2-1]}|\n{'=' * len(f'''{' '*((len('        |q to quit|')-len(f'|Editing {days_printed[q2-1]}|') + 8)// 2)}|Editing {days_printed[q2-1]}|''')}")
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
    tasks_sum = []
    if count // 7 >= 1:
        os.chdir("weeks")
        for i in range(count // 7):
            count_tasks = 0
            try:
                with open(f"{i + 1}.week.cfg", "r", encoding="utf-8") as file:
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
                tasks_sum.append(count_tasks)
            except FileNotFoundError:
                msg = ["Some weeks are missing..."]
                break
        os.chdir("..")
    return msg, num, sum, tasks_sum

def mark_tasks(ok, tasks, listos, saved, linos):
    try:
        if int(ok.lower().split(".")[0]) <= len(tasks) and int(ok.lower().split(".")[0]) > 0:
            try:
                try:
                    if listos[int(ok) - 1].split(":")[1] == "done,":
                        listos[int(ok) - 1] = f"{listos[int(ok) - 1].split(',')[0].split(':')[0]},"
                    else:
                        listos[int(ok) - 1] = f"{listos[int(ok) - 1].split(',')[0]}:done,"
                except IndexError:
                    listos[int(ok) - 1] = f"{listos[int(ok) - 1].split(',')[0]}:done,"
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
                tasks[tasks.index(task)] = f"{task.split(':done')[0]},"
            else:
                tasks[tasks.index(task)] = f"{task}:done,"
            lino = ",".join(tasks)
            lino = f"{saved};{lino}\n"
            linos[saved - 1] = lino
            with open("toDo.cfg", "w", encoding="utf-8") as file:
                file.writelines(linos)

def print_today_tasks(now, listos, day, hour, q1, platform_system):
    try:
        with open("toDo.cfg", "r", encoding="utf-8") as file:
            linos = file.readlines()
            print(f"{' '* ((len('|Enter number of done task to mark/unmark it as completed|') - len(f'day: {day}')) // 2)}day: {day}\n{' '* ((len('|Enter number of done task to mark/unmark it as completed|') - len(f'hour: {hour}')) // 2)}hour: {hour}\n{'=' * (len('|Enter number of done task to mark/unmark it as completed|'))}\n|Enter number of done task to mark/unmark it as completed|\n{' '*((len('|Enter number of done task to mark/unmark it as completed|') - len('|Enter q to quit|'))//2)}|Enter q to quit|\n{'=' * len('|Enter number of done task to mark/unmark it as completed|')}")
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
                                    if platform.release()  != "11" and platform_system == "Windows":
                                        two = "Done"
                                    else:
                                        two = "✓"
                                else:
                                    if platform.release()  != "11" and platform_system == "Windows":
                                        two = "Undone"
                                    else:
                                        two = "✘"
                                print(f"{tasks.index(task) + 1}.{one} {two}") 
                                printed = True
                            
                        except IndexError:
                            print(f"{tasks.index(task) + 1}.{task} ✘")  
                            printed = True
                    if printed == False:
                        clear(platform_system)
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


def check_year_count(year, month, day, count):
    years = []
    days_of_years = []
    with open("start.cfg", "r") as f: r = f.readlines()
    while year != int(r[0].split("-")[0]):
        years.append(year)
        if len(years) == 1:
            value = date(year, month, int(day)) - date(year, 1, 1)
        else:
            value = date(year, 12, 31) - date(year, 1, 1)
        try:
            value = int(str(value).split(" ")[0])
        except ValueError:
            value = 0
        days_of_years.append(value)
        year -= 1
    value = date(int(r[0].split("-")[0]), 12, 31) - date(int(r[0].split("-")[0]), int(r[0].split("-")[1]), int(r[0].split("-")[2]))
    try:
        value = int(str(value).split(" ")[0])
    except ValueError:
        value = 0
    days_of_years.append(value)
    years.append(int(r[0].split("-")[0]))
    weeks = count//7
    weeks_num = []
    for year in years:
        if days_of_years[years.index(year)]/7 != int and year is not years[-1]: #Not whole number and is not last in list, round down
            weeks_num.append(weeks - math.floor(days_of_years[years.index(year)]/7) )
            weeks -= math.floor(days_of_years[years.index(year)]/7)
        else:
            weeks_num.append(weeks - days_of_years[years.index(year)]//7)
            weeks -= days_of_years[years.index(year)]/7
    return weeks_num, years

def get_day_msg(q, platform_system):
    try:
        clear(platform_system)
        printed = 0
        day = int(q.split(".")[0])
        month = int(q.split(".")[1])
        year = int(q.split(".")[2])
        with open("start.cfg", "r") as f: r = f.readlines()[0]
        now = datetime.now()
        max_value = date(int(str(now).split(" ")[0].split("-")[0]), int(str(now).split(" ")[0].split("-")[1]), int(str(now).split(" ")[0].split("-")[2])) - date(int(r.split("-")[0]),int(r.split("-")[1]),int(r.split("-")[2]))
        value = date(year, month, day) - date(int(r.split("-")[0]),int(r.split("-")[1]),int(r.split("-")[2]))
        try:
            value = int(str(value).split(" ")[0])
        except:
            value = 1
        max_value = int(str(max_value).split(" ")[0])
        if value < 1 or value > max_value: print("Date not available...")
        else:
            week = math.floor(value/7)
            if week*7 == max_value-max_value%7 and value != week*7:
                with open(f"toDo.cfg", "r", encoding="utf-8") as f: r = f.readlines()
            else:
                if week*7 == max_value-max_value%7 and value == week*7: week -= 1#Last day of last possible week? Avoid errors
                os.chdir("weeks")
                with open(f"{week+1}.week.cfg", "r", encoding="utf-8") as f: r = f.readlines()
                os.chdir("..")
            tasks = r[value%7-1].strip().split(";")
            if len(tasks) > 1:
                tasks = tasks[1].split(",")
                for task in tasks:
                    try:
                        one = task.split(":")[0]
                        two = task.split(":")[1]
                    except IndexError:
                        if len(task) >= 1 and tasks[-1] is not task: #If the task is short and the task is last in list, ignore this task
                            if platform.release() != "11" and platform_system == "Windows":
                                two = "Undone"
                            else:
                                two = "✘"
                        else:
                            continue
                    if two.lower() == "done":
                        if platform.release() != "11" and platform_system == "Windows":
                            two = "Done"
                        else:
                            two = "✓"
                    else:
                        if platform.release() != "11" and platform_system == "Windows":
                            two = "Undone"
                        else:
                            two = "✘"
                    print(f"|{tasks.index(task)+1}|. {one} {two}")
                    printed += 1
        if printed == 0: print("No tasks")
    except Exception as e:
        print(f"Error occurred: {e}")
        
