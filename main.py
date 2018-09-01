#!/usr/bin/env python
import wx
import MovieManager as movMng
import FilterPanels as fPnls
import InfoPanels as infoPnls
import os
import ConfigParser


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        # Atributes
        self.dirname = ''
        self.filename = ''
        self.configFileName = 'config.ini'
        self.fileIsOpen = False
        self.myTitles = movMng.MovieManagerClass()
        self.activeTitles = []
        self.currentSet = 'movies'

        # init controls and sizers
        self.initControls()
        self.initSizers()

        # Menu and status bar
        self.initMenu()
        self.CreateStatusBar(2)
        self.SetStatusWidths([self.filterPanel.Size[0], -1])

        # configuration file
        self.config = ConfigParser.RawConfigParser()
        self.initConfigFile(self.configFileName)
        self.openLastFile()

        # set window events
        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def initConfigFile(self, name):
        if self.config.read(name):
            return
        self.config.add_section('dirs')
        self.config.set('dirs', 'filename', '')
        self.config.set('dirs', 'dirname', '')
        with open(name, 'wb') as configfile:
            self.config.write(configfile)
            configfile.close()
        print('Configuration file created: ' + name)

    def openLastFile(self):
        if not self.config.get('dirs', 'filename'):
            print('No last file path in configuration file')
            return
        self.filename = self.config.get('dirs', 'filename')
        self.dirname = self.config.get('dirs', 'dirname')
        if self.dirname:
            if self.openNewFile(self.dirname, self.filename):
                print('file ' + self.dirname + ' ' + self.filename + ' opened from config file')

    def initControls(self):
        # panels and control items
        self.filterPanel = fPnls.MainFilterPanel(self)
        self.infoNb = infoPnls.MainInfoPanel(self)

        # set Control events
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_COMBOBOX, self.OnSetSelection)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColumn)

    def initSizers(self):
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.filterPanel, 0, wx.EXPAND)
        mainSizer.Add(self.infoNb, 1, wx.EXPAND)
        self.SetSizer(mainSizer)

    def initMenu(self):

        # Setting up the menu.
        filemenu = wx.Menu()
        helpmenu = wx.Menu()

        # Menu items
        openItem = filemenu.Append(wx.ID_OPEN, wx.EmptyString, " Open .csv file")
        closeItem = filemenu.Append(wx.ID_CLOSE, wx.EmptyString, " Close current file")
        closeItem.Enable(self.fileIsOpen)
        filemenu.AppendSeparator()
        exitItem = filemenu.Append(wx.ID_EXIT, wx.EmptyString, " Terminate the program")
        aboutItem = helpmenu.Append(wx.ID_ABOUT, wx.EmptyString, " About IMDBstats")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)

        # set Menu events
        self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
        self.Bind(wx.EVT_MENU, self.OnClose, closeItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnSetSelection(self, event):
        titles = ['Movies', 'Series', 'Videogames']
        sets = ['movies', 'series', 'videogames']
        sel = self.filterPanel.selectedSet

        self.SetTitle("IMDB statistics - " + titles[sel])
        self.currentSet = sets[sel]
        self.SetStatusText('Showing ' + sets[sel])
        self.setActiveTitles()
        self.updateListView()

    def OnButton(self, event):
        label = event.GetEventObject().GetLabel()
        if label in {'Clear', 'Apply'}:
            self.CAButtonClicked(label)
        if label == 'Custom List':
            self.createCustomList()

    def OnColumn(self, event):
        self.SetStatusText('Sorted by ' + self.infoNb.objectList.TitleColumnSelected)

    def OnOpen(self, event):
        """ Open a file """
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename, "*.csv", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            # open file
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.openNewFile(self.dirname, self.filename)
        dlg.Destroy()

    def OnClose(self, event):
        """ Close current file """
        # set status info
        self.SetStatusText('File closed')
        self.fileIsOpen = False
        # disable controls
        self.filterPanel.EnableFilter(False)
        self.GetMenuBar().Enable(wx.ID_CLOSE, self.fileIsOpen)
        # clear data
        self.filterPanel.clearProps()
        self.myTitles.clearFilter(self.currentSet)
        self.myTitles.clearProps()
        self.infoNb.objectList.SetEmptyListMsg("Open .csv file\n(Ctrl+O)")
        # update list view
        self.activeTitles = []
        self.updateListView(True)

    def OnQuit(self, event):
        self.Close(True)

    def OnExit(self, event):
        self.updateConfigFile()
        event.Skip()

    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "About IMDBstats\n\nA program that computes statistics from your movies rated on IMDB.com\n\nCreated by Diego Ruiz\n", "About IMDB statistics", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def openNewFile(self, dirName, fileName):
        # open file
        if not self.myTitles.readFile(os.path.join(dirName, fileName)):
            return False
        # update list
        self.setActiveTitles()
        self.updateListView()
        self.infoNb.objectList.SetEmptyListMsg("No titles to show")
        self.infoNb.objectList.SortBy(1)
        # set status info
        self.SetStatusText('File ' + self.filename + ' opened')
        self.fileIsOpen = True
        self.filterPanel.EnableFilter(True)
        self.filterPanel.setFilterRanges(self.myTitles.filterRanges)
        self.filterPanel.setFilterParams(self.myTitles.filterParams)
        self.GetMenuBar().Enable(wx.ID_CLOSE, self.fileIsOpen)
        return True

    def createCustomList(self):
        numSelected = self.infoNb.objectList.GetSelectedItemCount()
        if numSelected == 0:
            self.SetStatusText('No titles selected')
            return
        self.setActiveTitles(True)
        self.updateListView()
        self.SetStatusText('Custom List Created')

    def CAButtonClicked(self, label):
        if label == 'Clear':
            self.SetStatusText('Filter cleared')
            self.myTitles.clearFilter(self.currentSet)
        elif label == 'Apply':
            self.SetStatusText('Filter applied')
            self.myTitles.setFilterParams(self.currentSet, self.filterPanel.filterParams[self.currentSet])
            self.myTitles.applyFilter(self.currentSet)
        self.filterPanel.setFilterParams(self.myTitles.filterParams)
        self.setActiveTitles()
        self.updateListView()

    def setActiveTitles(self, custom=False):
        if custom:
            self.activeTitles = self.infoNb.objectList.GetSelectedObjects()
        else:
            self.activeTitles = self.myTitles.getActiveTitles(self.currentSet)

    def updateListView(self, close=False):
        if close:
            self.SetStatusText('', 1)
        else:
            self.updateStatusListText()
        self.infoNb.objectList.SetObjects(self.activeTitles)

    def updateStatusListText(self):
        tempText = ' '
        if self.currentSet == 'series':
            tempText = '/episodes'
        self.SetStatusText(str(len(self.activeTitles)) + ' ' + self.currentSet + tempText, 1)

    def updateConfigFile(self):
        self.config.set('dirs', 'filename', self.filename)
        self.config.set('dirs', 'dirname', self.dirname)
        with open(self.configFileName, 'wb') as configfile:
            self.config.write(configfile)
            configfile.close()
        print('Configuration file: ' + self.configFileName +
              ' updated with filename ' + self.dirname + ' ' + self.filename)


if __name__ == '__main__':

    app = wx.App(False)
    mainWind = MainWindow(None, "IMDB statistics - Movies")
    mainWind.Show(True)
    mainWind.Maximize()

    app.MainLoop()
