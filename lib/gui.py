# -*- coding: utf-8 -*-

import os, sys, wx, func
import wx.lib.mixins.listctrl as listmix

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
        self.Bind(wx.EVT_MENU, self.aboutw, aboutw)
        
        self.demos = wx.ListBox(self.panel, 26, wx.DefaultPosition, (200, 568),style=wx.LB_SINGLE | wx.LB_SORT)
        try:
            path = os.path.expanduser('~/.q3a/q3ut4/demos')
            for demo in os.listdir(path):
                self.demos.Insert(demo, 0)
            self.demos.Bind(wx.EVT_LISTBOX, self.OnSelect, id=26)
        except:
            self.nodemosfound()
            
        self.dateplayed = wx.StaticText(self.panel, -1, 'Date played: ', pos=(205, 5))
        self.nickname = wx.StaticText(self.panel, -1, 'Nickname: ', pos=(205, 25))
        self.sshotaddr = wx.StaticText(self.panel, -1, "Screenshot:", pos=(205, 65))
        
        self.screenshot = wx.StaticBitmap(self.panel, -1, pos=(205, 105), bitmap=wx.EmptyBitmap(550, 400))
        sshot = wx.EmptyImage(550, 400).ConvertToBitmap()
        self.screenshot.SetBitmap(sshot)
        if os.path.exists(os.path.expanduser('~/.q3a/q3ut4/screenshots')):
            pass
        else:
            self.nosshotsfound()
        
        menubar = wx.MenuBar()
        menubar.Append(fm, "&File")
        menubar.Append(hm, "&Help")
        self.SetMenuBar(menubar)
        self.CenterOnParent()
        self.Show(True)
        print "* Main window - success"
        
    def exitapp(self, event):
        print ">> Exiting urtds..."
        self.Close(True)

    def aboutw(self, event):
        abw = AboutWindowFrame(None)
        
    def OnSelect(self, event):
        index = event.GetSelection()
        d = self.demos.GetString(index)
        a = self.dateplayed
        b = self.nickname
        c = self.sshotaddr
        a.SetLabel(label='Date played: ' + func.demodate(d))
        b.SetLabel(label='Nickname: ' + func.demonick(d))
        c.SetLabel(label='Screenshot: \n' + str((func.demoscreen(d))))
        print "Screenshot: " + str(func.demoscreen(d))
        try:
            if str(func.demoscreen(d)) != "None":
                sshot = wx.Image(func.demoscreen(d),wx.BITMAP_TYPE_JPEG).Scale(550, 400, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                self.screenshot.SetBitmap(sshot)
            else:
                sshot = wx.EmptyImage(550, 400).ConvertToBitmap()
                self.screenshot.SetBitmap(sshot)
        except:
            pass
        #TODO: Скриншоты
    
    def nodemosfound(self):
        achtung = wx.MessageDialog(None, 'Demos not found', 'UrTDSC - Error!', wx.OK | wx.ICON_EXCLAMATION)
        achtung.ShowModal()
        
    def nosshotsfound(self):
        achtung = wx.MessageDialog(None, 'Screenshots not found', 'UrTDSC - Error!', wx.OK | wx.ICON_EXCLAMATION)
        achtung.ShowModal()

class AboutWindowFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="About UrTDSC", size=(400, 250))
        AboutWindowFrame.SetSizeHints(self, 400, 250, 400, 250)
        panel = wx.Panel(self, -1)
        
        abouttext1 = 'Urban Terror Demo-Screenshot C0nc4t3n4t0r'
        abouttext1font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, False)
        text1 = wx.StaticText(panel, -1, abouttext1, (15, 5), (300, -1), wx.ALIGN_CENTER)   
        text1.SetFont(abouttext1font)
        abouttext2 = 'Version 0.1-alpha'
        wx.StaticText(panel, -1, abouttext2, (140, 25), (300, -1), wx.ALIGN_CENTER)
        
        wx.Button(panel, 1, 'Close', (160, 200))
        self.Bind(wx.EVT_BUTTON, self.CloseAbw, id=1)
        
        self.CenterOnParent()
        self.Show(True)
        print "* About Window - success"
        
    def CloseAbw(self, event):
        self.Close(True)
        print "* About Window - closed"

#TODO: переписать ListBox как ListCtrl
