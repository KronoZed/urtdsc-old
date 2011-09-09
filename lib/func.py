import os, time, config, datetime

#Variables
path = os.path.expanduser('~/.q3a/q3ut4/demos/')
spath = os.path.expanduser('~/.q3a/q3ut4/screenshots/')
screenpath = os.listdir(spath)

def demodate(demo):
    try:
        date = time.strftime('%d-%m-%Y @ %H:%M', time.localtime(os.path.getmtime(path + demo)))
        if config.DEBUG == '2':
            print "[D2][func] Date:", date
        return str(date)
    except:
        return "None"
    
def demorealdate(demo):
    realdate = os.path.getmtime(path + demo)
    #print "Real Date:", realdate
    return realdate

def screenrealdate(screen):
    realdate = os.path.getmtime(spath + screen)
    #print "Real Date:", realdate
    return realdate

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
    if config.DEBUG == '2':
        print "[func] Received demo time:", timed
    for demo in os.listdir(path):
        if config.DEBUG == '2':
            print "[D2][func] Demo:", demo
        if timed == demodate(demo):
            return demo
        else:
            pass


def demoscreen(d):
    try:
        for screen in screenpath:
            if screenrealdate(screen) > demorealdate(d) - 60 * 40 and screenrealdate(screen) < demorealdate(demoname) + 60 * 20:
                scr = spath + screen
                return str(scr)
            else:
                return None
    except:
        return "None"

def demoscreens(demoname):
    scraddr = []
    for screen in screenpath:
        #scrtimerange = datetime.datetime.fromtimestamp(os.path.getmtime(path + demoname)) - datetime.timedelta(minutes=40)
        if screenrealdate(screen) > demorealdate(demoname) - 60 * 40 and screenrealdate(screen) < demorealdate(demoname) + 60 * 20:
            scr = spath + screen
            scraddr.append(scr)
    return scraddr