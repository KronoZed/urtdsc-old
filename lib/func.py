import os, time, gui, datetime

#Variables
path = os.path.expanduser('~/.q3a/q3ut4/demos/')
spath = os.path.expanduser('~/.q3a/q3ut4/screenshots/')

def demodate(demo):
    try:
        date = time.strftime('%d-%m-%Y @ %H:%M', time.localtime(os.path.getmtime(path + demo)))
        if gui.DEBUG == '2':
            print "[D2][func] Date:", date
        return str(date)
    except:
        return "None"

def demonick(d):
    try:
        demoname = d.split('_')
        n = demoname[6]
        n1 = demoname[7]
        n2 = demoname[8]
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
    if gui.DEBUG == 1:
        print "[func] Received demo time:", timed
    for demo in os.listdir(path):
        if gui.DEBUG == '2':
            print "[D2][func] Demo:", demo
        if timed == demodate(demo):
            return demo
        else:
            pass


def demoscreen(d):
    try:
        dday = time.strftime("%d", time.localtime(os.path.getmtime(path + d))).lstrip('0')
        dmonth = time.strftime("%m", time.localtime(os.path.getmtime(path + d))).lstrip('0')
        dhour = time.strftime("%H", time.localtime(os.path.getmtime(path + d))).lstrip('0')
        dmin = time.strftime("%M", time.localtime(os.path.getmtime(path + d))).lstrip('0')
        screenpath = os.listdir(spath)
        for screen in screenpath:
            sday = time.strftime("%d", time.localtime(os.path.getmtime(spath + screen))).lstrip('0')
            smonth = time.strftime("%m", time.localtime(os.path.getmtime(spath + screen))).lstrip('0')
            shour = time.strftime("%H", time.localtime(os.path.getmtime(spath + screen))).lstrip('0')
            smin = time.strftime("%M", time.localtime(os.path.getmtime(spath + screen))).lstrip('0')
            if dday == sday:
                if dmonth == smonth:
                    if dhour == shour:
                        if dmin == smin:
                            scr = spath + screen
                            if scr:
                                return str(scr)
                            else:
                                return None
    except:
        return "None"
