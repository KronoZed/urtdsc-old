import os, time, config, datetime, shutil

#Variables
path = os.path.expanduser('~/' + config.URT_FOLDER + '/q3ut4/demos/')
spath = os.path.expanduser('~/' + config.URT_FOLDER + '/q3ut4/screenshots/')
try:
    screenpath = os.listdir(spath)
except:
    pass

def log(level, text, *args, **kwargs):
    if level in ('1', '2') and config.DEBUG in '2':
        print "[D2]:", text
    elif level in '1' and config.DEBUG in '1':
        print "[D1]:", text
    else:
        pass

def demodate(demo):
    try:
        date = time.strftime('%d-%m-%Y @ %H:%M', time.localtime(os.path.getmtime(path + demo)))
        log('2', 'Date: %s' % date)
        return str(date)
    except:
        return "None"
    
def demorealdate(demo):
    realdate = os.path.getmtime(path + demo)
    return realdate

def screenrealdate(screen):
    realdate = os.path.getmtime(spath + screen)
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
    log('2', "[func] Received demo time: %s" % timed)
    for demo in os.listdir(path):
        if timed == demodate(demo):
            log('2', "[func] Demo: %s" % demo)
            return demo
        else:
            pass


def demoscreen(d):
    try:
        for screen in screenpath:
            if screenrealdate(screen) > demorealdate(d) - 60 * 30 and screenrealdate(screen) < demorealdate(demoname) + 60 * 20:
                scr = spath + screen
                return str(scr)
            else:
                return None
    except:
        return "None"

def demoscreens(demoname):
    scraddr = []
    for screen in screenpath:
        if screenrealdate(screen) > demorealdate(demoname) - 60 * 30 and screenrealdate(screen) < demorealdate(demoname) + 60 * 20:
            scr = spath + screen
            scraddr.append(scr)
    return scraddr

def copyfile(filename):
    try:
        log('1', 'Copying file: %s' % filename)
        shutil.copy(filename, os.path.expanduser("~/Desktop"))
    except:
        log('1', 'Failed to copy %s' % filename)