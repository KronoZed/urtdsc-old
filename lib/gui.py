# -*- coding: utf-8 -*-

import os, sys, func, platform, glob, time, config
try:
    import wx
    print "* wxWidgets module loaded"
except:
    print "! Cannot load wxWidgets module! (Re)Install wxpython, please!"
    exit(101)

from wx.lib.wordwrap import wordwrap

# Set some variables
try:
    if config.DEBUG:
        DEBUG = config.DEBUG
except:
    DEBUG = '0'

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

        if os.path.exists(os.path.expanduser('~/.q3a/q3ut4/demos')):
            pass
        else:
            nodemos = '1'
                        
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
            
        self.demotext = wx.StaticText(self.panel, -1, "Demo: ", pos=(205, 5))
        txtf = self.demotext.GetFont()
        txtf.SetWeight(wx.BOLD) 
        self.demotext.SetFont(txtf)
        self.demoname = wx.StaticText(self.panel, -1, '', pos=(205 + self.demotext.GetSize()[0], 5))
        self.nicktext = wx.StaticText(self.panel, -1, 'Nickname: ', pos=(205, 25))
        self.nicktext.SetFont(txtf)
        self.nickname = wx.StaticText(self.panel, -1, '', pos=(205 + self.nicktext.GetSize()[0], 25))
        self.mapstext = wx.StaticText(self.panel, -1, 'Maps: ', pos=(205, 45))
        self.mapstext.SetFont(txtf)
        self.maps = wx.StaticText(self.panel, -1, '', pos=(205 + self.mapstext.GetSize()[0], 45))
        self.sshottext = wx.StaticText(self.panel, -1, "Screenshot:", pos=(205, 65))
        self.sshottext.SetFont(txtf)
        self.sshotaddr = wx.StaticText(self.panel, -1, "", pos=(205, 85))
        
        self.screenshot = wx.StaticBitmap(self.panel, -1, pos=(205, 105), bitmap=wx.EmptyBitmap(550, 400))
        sshot = wx.EmptyImage(550, 400).ConvertToBitmap()
        self.screenshot.SetBitmap(sshot)
        
        wx.StaticBox(self.panel, -1, pos=(205, 500), size=(550, 60))
        createdemos = wx.Button(self.panel, -1, "Copy demo to desktop", pos=(213, 518))
        # Will not implement it in main window, maybe...
        #wx.Button(self.panel, -1, "Copy Screenshots to Desktop", pos=(405, 518))
        otherscreens = wx.Button(self.panel, -1, "All screenshots...", pos=(630, 518), style=wx.ID_ADD)
        self.Bind(wx.EVT_BUTTON, self.others, otherscreens)
        
        # TODO: implement it in 0.3 :-)
        #self.Bind(wx.EVT_BUTTON, self.createdemos, createdemos)
        self.Bind(wx.EVT_BUTTON, self.copydemos, createdemos)
        
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
        func.log('1', "Main Window - success")
        
    def exitapp(self, event):
        func.log('1', "*** Exiting UrTDSC... ***")
        self.Close(True)

    def OnSelect(self, event):
        index = event.GetSelection()
        global timed
        timed = self.demos.GetString(index)
        #systimed = func.demorealdate(func.demoname(timed))
        a = self.demoname
        b = self.nickname
        c = self.sshotaddr
        d = self.maps
        maplist = []
        func.log('2', "[to func] Sending demo time: %s" % timed)
        a.SetLabel(label=func.demoname(timed))
        b.SetLabel(label=func.demonick(func.demoname(timed)))
        try:
            screens = func.demoscreens(func.demoname(timed))
            c.SetLabel(label=str(screens[0]))
            if DEBUG in ('1', '2'):
                func.log('1', "Screenshot: %s" % str(screens[0]))
            if str(screens[0]) != None or str(screens[0]) != "None":
                try:
                    sshot = wx.Image(screens[0], wx.BITMAP_TYPE_JPEG).Scale(550, 400, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                except:
                    sshot = wx.Image(screens[0], wx.BITMAP_TYPE_TGA).Scale(550, 400, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                self.screenshot.SetBitmap(sshot)
            else:
                sshot = wx.EmptyImage(550, 400).ConvertToBitmap()
                self.screenshot.SetBitmap(sshot)
                func.log('1', "Failed to set a screenshot!")
        except:
            c.SetLabel(label='No screenshot')
            sshot = wx.EmptyImage(550, 400).ConvertToBitmap()
            self.screenshot.SetBitmap(sshot)
            func.log('1', "No reliable screenshot(s) found")
            
        for scr in screens:
            scrs = scr.split("_")
            if scrs[1] in ('TOHUNGA', 'ORBITAL'):
                maplist.append(scrs[1] + "_" + scrs[2])
            else:
                maplist.append(scrs[1])
        
        items = ", ".join(maplist).lower()
        d.SetLabel(items)
    
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
        
    def createdemos(self, event):
        demosarc = CreateDemosArchive(self)
        demosarc.Show()
        demosarc.MakeModal(True)
        
    def copydemos(self, event):
        func.copyfile(os.path.expanduser("~/" + config.URT_FOLDER + "/q3ut4/demos/") + func.demoname(timed))

    def AboutDlg(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "Urban Terror Demo-Screenshot C0nc4t3n4t0r"
        info.Version = "0.2"
        info.Copyright = "(C) 2011, Stanislav N. aka p0z1tr0n"
        info.Description = wordwrap(
            "This tool is intended for concatenate demos and screenshots of Urban Terror game. It shows demos list, date the demo was recorded, player nickname used and a screenshot.\n\nPython version: " + str(platform.python_version()) + "\nwxWidgets version: " + str(wx.version()),
            1000, wx.ClientDC(self.panel))
        info.WebSite = ("http://code.google.com/p/urtdsc/", "Project Page")
        info.Developers = ["* Stanislav N. aka pztrn (pztrn@pztrn.ru) - project starter and main developer", "* archlinux@java (drakmail@gmail.com) - help, help, help"]
        info.License = wordwrap("* Beerware - it means next: if you like this software then buy me a beer! \n* GNU GPL v3 or higher", 500, wx.ClientDC(self.panel))
        wx.AboutBox(info)

class OtherScreens(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="UrTDSC - All Screenshots", size=(700, 450))
        OtherScreens.SetSizeHints(self, 700, 450, 700, 450)
        self.panel = wx.Panel(self, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #print scraddr
        
        try:
            # Screenshots list
            self.screenlist = wx.ListCtrl(self.panel, size=(155,390), style=wx.LC_REPORT)
            self.screenlist.InsertColumn(0, 'Screenshot', width=155, format=wx.LIST_FORMAT_CENTER)
            self.screenlist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
            
            # Lonely button :-)
            cpscrs = wx.Button(self.panel, -1, "Copy Screenshots to\nDesktop", pos=(10, 396))
            self.Bind(wx.EVT_BUTTON, self.CopyToDesktop, cpscrs)
            
            #Screenshot
            self.screenshot = wx.StaticBitmap(self.panel, -1, pos=(156, 0), bitmap=wx.EmptyBitmap(544, 452))
            sshot = wx.EmptyImage(544, 452).ConvertToBitmap()
            self.screenshot.SetBitmap(sshot)
        
            self.sslist = wx.ImageList(150, 150)
            func.log('1', '* Demo date is: %s' % timed)
            
            self.scrlist = func.demoscreens(func.demoname(timed))
            index = 0
            self.idx = 0
            for i in self.scrlist:
                try:
                    scr1 = wx.Image(i, wx.BITMAP_TYPE_JPEG).Scale(150, 150, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                except:
                    scr1 = wx.Image(i, wx.BITMAP_TYPE_TGA).Scale(150, 150, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                self.sslist.Add(scr1)
                self.index = self.screenlist.InsertStringItem(self.idx, '', self.idx)
                self.screenlist.SetItemImage(1, self.index, self.index)
                self.screenlist.SetItemData(self.index, index)
                index = index + 1
                self.idx = self.idx + 1
            
            self.sslist1 = self.screenlist.SetImageList(self.sslist, wx.IMAGE_LIST_SMALL)

            self.CenterOnParent()
            self.Show(True)
            func.log('1', 'Other Screenshots Window - success')
        except:
            oops = wx.MessageDialog(None, 'Demo not specified or cannot find reliable screenshots.', 'UrTDSC - Error!', wx.OK | wx.ICON_EXCLAMATION)
            oops.ShowModal()
            # This piece of shit generates traceback required to prevent opening "Other Screenshots" window
            self.OnClose('DO NOT OPEN THIS F***ING WINDOW >.<')
            func.log('1', '[ERR] No demo specified or cannot find reliable screenshots. Supress "Other Screenshots" window')
            func.log('1', '[ERR] Other Screenshots - fail')
            
    def OnClose(self, event):
        self.MakeModal(False)
        event.Skip()
        func.log('1', "Other Screenshots Window - closed")
        
    def OnSelect(self, event):
        index = event.GetIndex()
        func.log('1','Demoname in "All Screenshots": %s' % func.demoname(timed))
        try:
            sshot = wx.Image(self.scrlist[index], wx.BITMAP_TYPE_JPEG).Scale(544, 452, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        except:
            sshot = wx.Image(self.scrlist[index], wx.BITMAP_TYPE_TGA).Scale(544, 452, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.screenshot.SetBitmap(sshot)
        
    def CopyToDesktop(self, event):
        for screen in self.scrlist:
            func.copyfile(screen)

class CreateDemosArchive(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="UrTDSC - Create demos archive", size=(700, 580))
        CreateDemosArchive.SetSizeHints(self, 700, 580, 700, 580)
        self.panel = wx.Panel(self, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        wx.StaticText(self.panel, -1, "Demos that will be archived are listed on left side. Demos that was completed in 40 minutes range of selected demo in main window are listed on right side.", pos=(5, 5), size=(600, 35))
        wtfb = wx.Button(self.panel, -1, "WTF?", pos=(610, 5))
        self.Bind(wx.EVT_BUTTON, self.wtf, wtfb)
        
        self.dmtoarc = wx.ListBox(self.panel, 26, pos=(15, 55), size=(270, 200), style=wx.LB_SINGLE)
        self.dmlist = wx.ListBox(self.panel, 26, pos=(415, 55), size=(270, 200), style=wx.LB_SINGLE)
        wx.Button(self.panel, -1, "<< Add", pos=(307, 54))
        wx.Button(self.panel, -1, "Remove >>", pos=(307, 227))
        
        wx.StaticLine(self.panel, -1, pos=(5, 260), size=(690, 5))
        wx.StaticLine(self.panel, -1, pos=(350, 265), size=(5, 200), style=wx.LI_VERTICAL)
        wx.StaticLine(self.panel, -1, pos=(5, 470), size=(690, 5))
        
        wx.StaticText(self.panel, -1, "Ready to create archive...", pos=(5, 480), size=(620, 35))
        wx.Gauge(self.panel, -1, 100, pos=(5, 505), size=(690,15))
        wx.Button(self.panel, -1, "Create archive!", pos=(300, 535))
        
        
        self.CenterOnParent()
        func.log('1', "Demos Window - success")
        
    def OnClose(self, event):
        self.MakeModal(False)
        event.Skip()
        func.log('1', "Demos Window - closed")
            
    def wtf(self, event):
        wtf = wx.MessageDialog(None, 'This means, that UrTDSC can fail with creating list of demos.\n\nOn the left - demos that will be added to archive.\n\nOn the right - demos, that in 40 minutes range and will not be added to archive.\n\nUnder these lists - short demo information. Select demo to get it.', 'UrTDSC - WTF IS THAT?', wx.OK | wx.ICON_INFORMATION)
        wtf.ShowModal()