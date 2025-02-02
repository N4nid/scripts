import os
import sys

# NO heading can have the name none or clockout

# date +"[%F %a %R]"
# org mode time log thing
# termux-dialog sheet -v "1,2,3" | jq ".text"
# datediff -i "[%F %a %H:%M]" now ""

logfilepath = "/data/data/com.termux/files/home/storage/shared/org/org/clocklist.org"
lastclockpath = "/data/data/com.termux/files/home/lastClock" # saves the heading with last clock in
lastClock = "none"

def getUserInput(vals):
    result = os.popen("termux-dialog sheet -v '"+vals+ "'| jq '.text'").read()
    print(result)

    if("clockout" in result):
        clockout(lastClock[0])
    elif("cancel" in result):
        print("canceled yo")
    else:
        clockin(result)

def notify(msg):
    os.popen('termux-toast -g top -b black "'+msg+'"')

def clockout(input):
    print("clockin out")
    if("clockout" in input or "none" in input):
        notify("already clocked out")
        return

    #datediff = os.popen('datediff -i "[%F %a %H:%M]" now '+lastClock[1]).read()
    notify("clockout: "+str(input))
    #notify("CO: "+datediff+" "+input)
    print(input)
    linenum = input.split(":")[0][1:]
    print("yo "+linenum)
    f = open(logfilepath,"r")
    lines = f.readlines()
    f.close()

    date = "--"+os.popen('date +"[%F %a %R]"').read()

    for i in range(int(linenum), len(lines)):
        if("LOGBOOK" in lines[i]):
            print("has logbook")
            i += 1
            print(lines[i])
            lines[i] = lines[i][:-1]+ date
            print(lines[i])
            with open(logfilepath, "w") as file:
                file.writelines(lines)
            break

    with open(lastclockpath, "w") as l:
        l.write("none")

def clockin(input):
    print("clocking in")
    if("none" not in lastClock[0]):
        #notify("clockout: "+lastClock[0])
        clockout(lastClock)
    notify("clockin: "+input)

    print(input)
    linenum = input.split(":")[0][1:]
    f = open(logfilepath,"r")
    lines = f.readlines()
    f.close()
    hasLogbook = True

    date = "CLOCK: "+os.popen('date +"[%F %a %R]"').read()

    for i in range(int(linenum), len(lines)):
        if("LOGBOOK" in lines[i]):
            print("has logbook")
            print(lines[i])
            linenum = i
            break
        elif("* " in lines[i]):
            print("no logbook below")
            hasLogbook = False
            break

    linenum = int(linenum)
    if(not hasLogbook):
        lines[linenum:linenum] = [":LOGBOOK:\n",date,":END:\n"]
    else:
        linenum += 1
        lines[linenum:linenum] = date

    with open(logfilepath, "w") as file:
        file.writelines(lines)

    with open(lastclockpath, "w") as l:
        l.writelines([input,os.popen('date +"[%F %a %R]"').read()])



pipe = os.popen("grep -n '*\* ' "+logfilepath)
vals = "clockout"
for line in pipe:
    vals += ","+line

vals += ",cancel"
print(vals)

with open(lastclockpath, "r") as l:
    lastClock = l.readlines()

if(len(sys.argv) > 1):
    clockout(lastClock[0])
    print(sys.argv[1])
else:
    getUserInput(vals)
