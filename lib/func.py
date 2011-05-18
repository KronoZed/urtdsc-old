import os, sys, gui, time, commands, re

#Variables
path = os.path.expanduser('~/.q3a/q3ut4/demos/')
spath = os.path.expanduser('~/.q3a/q3ut4/screenshots/')

def demodate(d):
    try:
        date = time.strftime("%m-%d-%Y @ %H:%M",time.localtime(os.path.getmtime(path+d)))
        print "[func] Date for", d + ": ", date
        return str(date)
    except:
        return "None"

def demonick(d):
    try:
        os.system('echo '+d+' > 1')
        n = commands.getoutput("cat 1 | awk -F '_' {' print $7 '}")
        n1 = commands.getoutput("cat 1 | awk -F '_' {' print $8 '}")
        n2 = commands.getoutput("cat 1 | awk -F '_' {' print $9 '}")
        os.system('rm 1')
        if n2 in "ut4":
            NICK = n + " " + n1
            return NICK
        elif n1 in "ut4":
            NICK = n
            return NICK
        else:
            NICK = n + " " + n1 + " " + n2
            return NICK
    except:
        return "None"

def demoname(timed):
    for demo in os.listdir(path):
        if timed == demodate(demo):
            return demo

def demoscreen(d):
    try:
        dday = time.strftime("%d",time.localtime(os.path.getmtime(path+d))).lstrip('0')
        dmonth = time.strftime("%m",time.localtime(os.path.getmtime(path+d))).lstrip('0')
        dhour = time.strftime("%H",time.localtime(os.path.getmtime(path+d))).lstrip('0')
        dmin = time.strftime("%M",time.localtime(os.path.getmtime(path+d))).lstrip('0')
        screenpath = os.listdir(spath)
        for screen in screenpath:
            sday = time.strftime("%d",time.localtime(os.path.getmtime(spath+screen))).lstrip('0')
            smonth = time.strftime("%m",time.localtime(os.path.getmtime(spath+screen))).lstrip('0')
            shour = time.strftime("%H",time.localtime(os.path.getmtime(spath+screen))).lstrip('0')
            smin = time.strftime("%M",time.localtime(os.path.getmtime(spath+screen))).lstrip('0')
            if dday == sday:
                if dmonth == smonth:
                    if dhour == shour:
                        if dmin == smin:
                            scr = spath+screen
                            if scr:
                                return str(scr)
                            else:
                                return None
    except:
        return "None"
