#!/usr/bin/env python
import wx
import MovieManager as movMng
import FilterPanels as fPnls
import os
from ObjectListView import ObjectListView, ColumnDefn

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 750))

        # Atributes
        self.dirname = ''
        self.filename = ''
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

    def initControls(self):
        # panels and control items
        self.filterPanel = fPnls.MainFilterPanel(self)
        self.infoNb = wx.Notebook(self)
        self.objectList = ObjectListView(self.infoNb,
                                         style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES,
                                         cellEditMode="CELLEDIT_NONE",
                                         useAlternateBackColors=False)
        self.objectList.SetEmptyListMsg("Open .csv file\n(Ctrl+O)")
        self.myColumns = [
            ColumnDefn(title="Year", align="center", valueGetter="Year", isEditable=False, fixedWidth=75),
            ColumnDefn(title="Title", width=250, valueGetter="Title", isEditable=False, minimumWidth=200, isSearchable=True),
            ColumnDefn(title="IMDb Rating", align="center", valueGetter="IMDb Rating", isEditable=False, fixedWidth=125),
            ColumnDefn(title="Your Rating", align="center", valueGetter="Your Rating", isEditable=False, fixedWidth=125),
            ColumnDefn(title="Date Rated", align="center", valueGetter="Date Rated", isEditable=False, fixedWidth=125),
            ColumnDefn(title="Genres", width=250, valueGetter="Genres", minimumWidth=100, isEditable=False),
            ColumnDefn(title="Directors", width=250, valueGetter="Directors", minimumWidth=100, isEditable=False),
            ColumnDefn(title="Num Votes", valueGetter="Num Votes", isEditable=False, fixedWidth=125),
            ColumnDefn(title="Runtime (min.)", valueGetter="Runtime (mins)", isEditable=False, fixedWidth=150)
        ]
        self.objectList.SetColumns(self.myColumns)
        self.infoNb.AddPage(self.objectList, "List")
        self.infoNb.AddPage(wx.Panel(self.infoNb), "Graphs")
        #infoNb.AddPage(wx.Panel(infoNb), "Records")

        # set Control events
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColumn, self.objectList)
        self.Bind(wx.EVT_BUTTON, self.OnCAButton)
        self.Bind(wx.EVT_COMBOBOX, self.OnSetSelection)

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
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnSetSelection(self, event):
        titles = ['Movies', 'Series', 'Videogames']
        sets = ['movies', 'series', 'videogames']
        sel = self.filterPanel.selectedSet

        self.SetTitle("IMDB statistics - " + titles[sel])
        self.currentSet = sets[sel]
        self.SetStatusText('Showing ' + sets[sel])
        self.updateListView()

    def OnCAButton(self, event):
        if self.filterPanel.clearClicked:
            self.SetStatusText('Filter cleared')
            self.myTitles.clearFilter(self.currentSet)
        elif self.filterPanel.appliedClicked:
            self.SetStatusText('Filter applied')
            self.myTitles.setFilterParams(self.currentSet, self.filterPanel.filterParams[self.currentSet])
            self.myTitles.applyFilter(self.currentSet)
        self.filterPanel.setFilterParams(self.myTitles.filterParams)
        self.updateListView()

    def OnColumn(self, event):
        self.SetStatusText('Sorted by ' + self.myColumns[event.GetColumn()].title)
        return

    def OnOpen(self, event):
        """ Open a file """
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.csv", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            # open file
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.myTitles.readFile(os.path.join(self.dirname, self.filename))
            # update list
            self.updateListView()
            self.objectList.SetEmptyListMsg("No titles to show")
            self.objectList.SortBy(1)
            # set status info
            self.SetStatusText('File ' + self.filename + ' opened')
            self.fileIsOpen = True
            self.filterPanel.EnableFilter(True)
            self.filterPanel.setFilterRanges(self.myTitles.filterRanges)
            self.filterPanel.setFilterParams(self.myTitles.filterParams)
            self.GetMenuBar().Enable(wx.ID_CLOSE, self.fileIsOpen)
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
        self.objectList.SetEmptyListMsg("Open .csv file\n(Ctrl+O)")
        # update list view
        self.updateListView(True)

    def OnExit(self, event):
        self.Close(True)

    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "About IMDBstats\n\nA program that computes statistics from your movies rated on IMDB.com\n\nCreated by Diego Ruiz\n", "About IMDB statistics", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def updateListView(self, clear=False):
        if clear:
            self.activeTitles = []
            self.SetStatusText('', 1)
        else:
            tempText = ' '
            self.activeTitles = self.myTitles.getActiveTitles(self.currentSet)
            if self.currentSet == 'series':
                tempText = '/episodes'
            self.SetStatusText(str(len(self.activeTitles)) + ' ' + self.currentSet + tempText, 1)
        self.objectList.SetObjects(self.activeTitles)

if __name__ == '__main__':

    app = wx.App(False)
    mainWind = MainWindow(None, "IMDB statistics - Movies")
    mainWind.Show(True)

    app.MainLoop()
