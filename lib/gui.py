# -*- coding: utf-8 -*-

import os, sys, wx, func, platform, glob, time, config
from wx.lib.wordwrap import wordwrap

# Temporary variables
DEBUG = config.DEBUG

class MainWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Urban Terror Demo-Screenshot C0nc4t3n4t0r", size=(800, 600))
        MainWindow.SetSizeHints(self, 800, 600, 800, 600)
        self.panel = wx.Panel(self, -1)
        
        fm = wx.Menu()
        closeapp = fm.Append(wx.ID_EXIT, "E&xit")
        self.Bind(wx.EVT_MENU, self.exitapp, closeapp)
        
        hm = wx.Menu()
        aboutw = hm.Append(wx.ID_ABOUT, "A&bout")
        self.Bind(wx.EVT_MENU, self.AboutDlg, aboutw)
        
        #Listbox with available self.demos
        self.demos = wx.ListBox(self.panel, 26, wx.DefaultPosition, (200, 571), style=wx.LB_SINGLE)
                
        try:
            path = os.path.expanduser('~/.q3a/q3ut4/demos')
            self.date_file_list = []
            for file in glob.glob(path + "/*.dm_68"):
                stats = os.stat(file)
                lastmod_date = time.localtime(stats[8])
                date_file_tuple = lastmod_date, file
                self.date_file_list.append(date_file_tuple)
                self.date_file_list.sort()
            for file in self.date_file_list:
                file_date = time.strftime('%d-%m-%Y @ %H:%M', file[0])
                self.demos.Insert(file_date, 0)
                self.demos.Bind(wx.EVT_LISTBOX, self.OnSelect, id=26)
                nodemos = '0'
        except:
            self.nodemosfound()
            nodemos = '1'
            
        self.demoname = wx.StaticText(self.panel, -1, 'Demo name: ', pos=(205, 5))
        self.nickname = wx.StaticText(self.panel, -1, 'Nickname: ', pos=(205, 25))
        self.sshotaddr = wx.StaticText(self.panel, -1, "Screenshot:", pos=(205, 65))
        
        self.screenshot = wx.StaticBitmap(self.panel, -1, pos=(205, 105), bitmap=wx.EmptyBitmap(550, 400))
        sshot = wx.EmptyImage(550, 400).ConvertToBitmap()
        self.screenshot.SetBitmap(sshot)
        
        wx.StaticBox(self.panel, -1, pos=(205, 500), size=(550, 60))
        wx.Button(self.panel, -1, "Create demos archive...", pos=(213, 518))
        wx.Button(self.panel, -1, "Copy Screenshots to Desktop", pos=(405, 518))
        otherscreens = wx.Button(self.panel, -1, "All screenshots...", pos=(630, 518), style=wx.ID_ADD)
        self.Bind(wx.EVT_BUTTON, self.others, otherscreens)
        
        if os.path.exists(os.path.expanduser('~/.q3a/q3ut4/screenshots')):
            nosshots = '0'
        else:
            self.nosshotsfound()
            nosshots = '1'
            
        if nodemos == '0' and nosshots == '0':
            pass
        else:
            self.nothingfound()
                    
        menubar = wx.MenuBar()
        menubar.Append(fm, "&File")
        menubar.Append(hm, "&Help")
        self.SetMenuBar(menubar)
        self.CenterOnParent()
        self.Show(True)
        print '* Debug is:', DEBUG
        if config.DEBUG in ('1', '2'):
            print "* Main window - success"
        
    def exitapp(self, event):
        if config.DEBUG in ('1', '2'):
            print ">> Exiting urtdsc..."
        self.Close(True)

    def OnSelect(self, event):
        index = event.GetSelection()
        global timed
        timed = self.demos.GetString(index)
        a = self.demoname
        b = self.nickname
        c = self.sshotaddr
        if config.DEBUG in ('1', '2'):
            print "[to func] Sending demo time:", timed
        a.SetLabel(label='Demo name: ' + func.demoname(timed))
        b.SetLabel(label='Nickname: ' + func.demonick(func.demoname(timed)))
        c.SetLabel(label='Screenshot: \n' + str((func.demoscreen(func.demoname(timed)))))
        if config.DEBUG in ('1', '2'):
            print "* Screenshot: " + str(func.demoscreen(func.demoname(timed)))
        try:
            if str(func.demoscreen(func.demoname(timed))) != "None":
                sshot = wx.Image(func.demoscreen(func.demoname(timed)), wx.BITMAP_TYPE_JPEG).Scale(550, 400, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                self.screenshot.SetBitmap(sshot)
            else:
                sshot = wx.EmptyImage(550, 400).ConvertToBitmap()
                self.screenshot.SetBitmap(sshot)
        except:
            pass
    
    def nodemosfound(self):
        achtung = wx.MessageDialog(None, 'Demos not found', 'UrTDSC - Error!', wx.OK | wx.ICON_EXCLAMATION)
        achtung.ShowModal()
        
    def nosshotsfound(self):
        achtung = wx.MessageDialog(None, 'Screenshots not found', 'UrTDSC - Error!', wx.OK | wx.ICON_EXCLAMATION)
        achtung.ShowModal()
    
    def nothingfound(self):
        nf = wx.MessageDialog(None, 'No screenshots or demos found.\nWill now exit.', 'UrTDSC - Error!', wx.OK | wx.ICON_EXCLAMATION)
        nf.ShowModal()
        sys.exit(255)
        
    def others(self, event):
        otherscreenshots = OtherScreens(self)
        otherscreenshots.Show()
        otherscreenshots.MakeModal(True)

    def AboutDlg(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "Urban Terror Demo-Screenshot C0nc4t3n4t0r"
        info.Version = "0.2-rc1"
        info.Copyright = "(C) 2011, Stanislav N. aka p0z1tr0n"
        info.Description = wordwrap(
            "This tool is intended for concatenate demos and screenshots of Urban Terror game. It shows demos list, date the demo was recorded, player nickname used and a screenshot.\n\nPython version: " + str(platform.python_version()) + "\nwxWidgets version: " + str(wx.version()),
            1000, wx.ClientDC(self.panel))
        info.WebSite = ("http://redmine.pztrn.ru/projects/urtdsc", "Project Page")
        info.Developers = ["* Stanislav N. aka pztrn (pztrn@pztrn.ru) - project starter and main developer", "* archlinux@java (drakmail@gmail.com) - help, help, help"]
        info.License = wordwrap("* Beerware - it means next: if you like this software then buy me a beer! \n* GNU GPL v3 or higher", 500, wx.ClientDC(self.panel))
        wx.AboutBox(info)

class OtherScreens(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="UrTDSC - All Screenshots", size=(700, 450))
        OtherScreens.SetSizeHints(self, 700, 450, 700, 450)
        self.panel = wx.Panel(self, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        try:
            # Screenshots list
            self.screenlist = wx.ListCtrl(self.panel, size=(155,452), style=wx.LC_REPORT)
            self.screenlist.InsertColumn(0, 'Screenshot', width=155)
            self.screenlist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
            
            #Screenshot
            self.screenshot = wx.StaticBitmap(self.panel, -1, pos=(156, 0), bitmap=wx.EmptyBitmap(544, 452))
            sshot = wx.EmptyImage(544, 452).ConvertToBitmap()
            self.screenshot.SetBitmap(sshot)
        
            self.sslist = wx.ImageList(150, 150)
            if config.DEBUG in ('1', '2'):
                print '* Demo date is:', timed
            #i = wx.Image(func.demoscreen(demoname), wx.BITMAP_TYPE_JPEG).Scale(150, 150, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
            i = func.demoscreen(func.demoname(timed))
            self.sslist.Add(wx.Bitmap(i))
            self.sslist1 = self.screenlist.SetImageList(self.sslist, wx.IMAGE_LIST_SMALL)
            self.idx = 1
            self.index = self.screenlist.InsertStringItem(self.idx, '', self.idx)
            self.screenlist.SetItemImage(1, self.index, self.index)
            

            self.CenterOnParent()
            self.Show(True)
            if config.DEBUG in ('1', '2'):
                print "* Other Screenshots Window - success"
        except:
            oops = wx.MessageDialog(None, 'Demo not specified or cannot find reliable screenshots.', 'UrTDSC - Error!', wx.OK | wx.ICON_EXCLAMATION)
            oops.ShowModal()
            # This piece of shit generates traceback required to prevent opening "Other Screenshots" window
            self.OnClose('DO NOT OPEN THIS FUCKING WINDOW >.<')
            if config.DEBUG in ('1', '2'):
                print '[ERR] No demo specified or cannot find reliable screenshots. Supress "Other Screenshots" window'
                print '[ERR] Other Screenshots - fail'
            
    def OnClose(self, event):
        self.MakeModal(False)
        event.Skip()
        print "* Other Screenshots Window - closed"
        
    def OnSelect(self, event):
        index = event.GetItem()
        #demoname = self.screenlist.GetItem(index)
        print 'index:', func.demoname(timed)
        sshot = wx.Image(func.demoscreen(func.demoname(timed)), wx.BITMAP_TYPE_JPEG).Scale(544, 452, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.screenshot.SetBitmap(sshot)