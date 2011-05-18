# -*- coding: utf-8 -*-

import os, sys, wx, func, platform
from wx.lib.wordwrap import wordwrap
from wx.lib.mixins.listctrl import ColumnSorterMixin

class MainWindow(wx.Frame, wx.lib.mixins.listctrl.ColumnSorterMixin):
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
        self.demos = wx.ListBox(self.panel, 26, wx.DefaultPosition, (200, 568),style=wx.LB_SINGLE)
                
        try:
            path = os.path.expanduser('~/.q3a/q3ut4/demos')
            self.dmlist = []
            for demo in os.listdir(path):
                self.dmlist.append(func.demodate(demo))
            self.dmlist.sort()
            #self.dmlist.reverse()
            for demo in self.dmlist:
                self.demos.Insert(demo, 0)
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
        if os.path.exists(os.path.expanduser('~/.q3a/q3ut4/screenshots')):
            pass
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
        print "* Main window - success"
        
    def exitapp(self, event):
        print ">> Exiting urtdsc..."
        self.Close(True)

    def aboutw(self, event):
        abw = AboutWindowFrame(None)
        
    def OnSelect(self, event):
        index = event.GetSelection()
        timed = self.demos.GetString(index)
        a = self.demoname
        b = self.nickname
        c = self.sshotaddr
        a.SetLabel(label='Demo name: ' + func.demoname(timed))
        b.SetLabel(label='Nickname: ' + func.demonick(func.demoname(timed)))
        c.SetLabel(label='Screenshot: \n' + str((func.demoscreen(func.demoname(timed)))))
        print "Screenshot: " + str(func.demoscreen(func.demoname(timed)))
        try:
            if str(func.demoscreen(func.demoname(timed))) != "None":
                sshot = wx.Image(func.demoscreen(func.demoname(timed)),wx.BITMAP_TYPE_JPEG).Scale(550, 400, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
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
        exit(255)

    def AboutDlg(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "Urban Terror Demo-Screenshot C0nc4t3n4t0r"
        info.Version = "0.2-dev"
        info.Copyright = "(C) 2011, Stanislav N. aka p0z1tr0n"
        info.Description = wordwrap(
            "This tool is intended for concatenate demos and screenshots of Urban Terror game. It shows demos list, date the demo was recorded, player nickname used and a screenshot.\n\nPython version: " + str(platform.python_version()) + "\nwxWidgets version: " + str(wx.version()),
            1000, wx.ClientDC(self.panel))
        info.WebSite = ("http://code.google.com/p/urtdsc/", "Google Code page")
        info.Developers = ["* Stanislav N. aka pztrn (pztrn@pztrn.ru) - project\nstarter and main developer"]
        info.License = wordwrap("* Beerware - it means next: if you like this software then buy me a beer! \n* GNU GPL v3", 500, wx.ClientDC(self.panel))
        wx.AboutBox(info)

#TODO: переписать ListBox как ListCtrl
