from datetime import datetime
import sys
from dll import *

def main(count, day, days, weekday):
    end = ""
    while end.lower() != "q":
        end = menu()
        if end in ["1", "2", "3"]: #Options, where data load is needed
            msg, num, sum = load_weeks(count)

            if "1" == end:
                if count // 7 == 0:
                    print("No data...")
                else:
                    for ms in msg:
                        print(ms)
                input()
                clear()
            msg = []
            for content in sum:
                msg.append(f"{content} -> {num[sum.index(content)]}")
            num.sort(reverse=True)
            done = []

            if "2" == end:
                if count // 7 == 0:
                    print("No data...")
                else:
                    print("10 popular tasks:")
                for i in range(10):
                    for message in msg:
                        if message.split("-> ")[1] == str(num[i]) and message not in done:
                            print(f"{i + 1}: {message}")
                            done.append(message)
                input()
                clear()

            if "3" == end:
                if count // 7 == 0:
                    print("No data...")
                else:
                    find = input("Search for tasks:").lower()
                    text = list(find.lower())
                    found = 0
                    for message in msg:
                        cor = 0
                        saved = message
                        right = 0
                        bad = False
                        message = message.split(" ->")[0].lower()
                        temp = list(find)
                        for lttr in list(message):
                            if lttr.lower() in temp:
                                temp.pop(temp.index(lttr.lower()))
                                cor += 1
                            try:
                                if lttr.lower() == text[list(message).index(lttr)].lower() and bad == False:
                                    right += 1
                                else:
                                    bad = True
                            except IndexError:
                                bad = True
                        if right >= len(find) * 0.5 and cor >= len(find) * 0.5 or cor >= len(find) * 0.8 and right >= 2:
                            print(f"{message} -> {saved.split('-> ')[1]}")
                            found += 1
                    if found == 0:
                        print("Nothing corresponds to your search")
                input()
                clear()

        if "4" == end:
            now = datetime.now()
            hour = now.hour
            day = days[now.weekday()]
            while True:
                clear()
                listos = []
                printed = False
                q1 = "y"
                tasks, saved, linos, listos, printed, q1 = print_today_tasks(now, listos, day, hour, q1)
                if q1.lower() != "y" or printed == False: break #Doesnt want to apply template and tasks are empty for today
                if printed == True:
                    ok = input("$~ ")
                    if ok.lower() == "q":
                        break
                    mark_tasks(ok, tasks, listos, saved, linos)

        if end == "5":
            q1 = input("Enter number of week you want to edit:\n|1| -> |This week|\n|2| -> |Next week|\n$~ ")
            clear()
            if q1 == "1":
                edit_file = "toDo.cfg"
                left_of_week = 7 - days.index(weekday)
                print("Enter number of day you want to edit:")
                days_printed = []
                for i in range(left_of_week):
                    if i == 0: print_this_day = "Today"
                    elif i == 1: print_this_day = "Tomorrow"
                    else: print_this_day = days[i+days.index(weekday)]
                    print(f"|{i+1}| -> |{print_this_day}|")
                    days_printed.append(print_this_day)
                q2 = input("$~ ")
                clear()

                with open(edit_file, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                try: q2 = int(q2)
                except ValueError: input("invalid input");sys.exit()
                if q2 <= left_of_week and q2 >= 0:
                    today = days.index(weekday)+q2-1
                    writing_changes(q2, days_printed, lines, edit_file, today)
                             
            elif q1 == "2":                
                edit_file = "toDo.cfg.next"
                print("Enter number of day you want to edit:")
                for i in range(7): print(f"|{i + 1}| -> |{days[i]}|")
                q2 = input("$~ ")
                try: q2 = int(q2)
                except ValueError: input("invalid input");sys.exit()
                with open(edit_file, "r", encoding="utf-8") as file:
                    lines = file.readlines()    
                if q2 <= 7 and q2 > 0:
                    writing_changes(q2, days, lines, edit_file, q2-1)

            
        if end == "6":
            temp = ""
            while temp.lower() != "q":
                clear()
                print(f"Enter task name(If task is already in -> task is deleted, else the task is created)\n   {' '*((len('Enter task name(If task is already in -> task is deleted, else the task is created)') - len('|q to quit|'))//2)}|q to quit|")
                try:
                    with open("template.cfg", "r", encoding="utf-8") as file:
                        line = file.readlines()
                except FileNotFoundError:
                    with open("template.cfg", "w", encoding="utf-8") as file:
                        file.write("")
                        line = []
                if line != []:
                    for task in line[0].split(","):
                        if task != "":
                            print(f"{line[0].split(",").index(task) + 1}. {task}")
                temp = input("$~ ")
                if temp.lower() != "q":
                    temp_list = []
                    deleted = False
                    if line != []:
                        temp_list = line[0].split(",")
                        for task in temp_list:
                            if task.lower() == temp.lower():
                                temp_list.pop(temp_list.index(task))
                                deleted = True
                    main_list = []
                    for task in temp_list:
                        if task != "," and task != "" and task != " ":
                            main_list.append(f"{task},")
                    if deleted == False:
                        main_list.append(f"{temp},")
                    with open("template.cfg", "w", encoding="utf-8") as file:
                        file.write("".join(main_list))
if __name__ == "__main__":
    year, month, day, weekday, days = init()
    count, start_day = get_days_info(year, month, days, weekday, day)
    check_files(count)
    main(count, day, days, weekday)