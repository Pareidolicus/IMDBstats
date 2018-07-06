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

        # init windows, controls and sizers
        self.initControls()
        self.initSizers()

        # Menu and status bar
        self.initMenu()
        self.CreateStatusBar()
        self.GetStatusBar().SetFieldsCount(2, [self.filterPanel.Size[0], -1])

    def initControls(self):
        # panels and control items
        self.filterPanel = wx.Panel(self)
        self.filterSetSelection = fPnls.ListSelectionPanel(self.filterPanel,
                                                           ['Movies', 'Series', 'Videogames'],
                                                           'Set')
        self.filterSetSelection.Disable()
        self.clearApplyButtons = fPnls.ClearApplyButtonsPanel(self.filterPanel)
        self.clearApplyButtons.Disable()
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
        self.clearApplyButtons.Bind(wx.EVT_BUTTON, self.OnCAButton)
        self.filterSetSelection.Bind(wx.EVT_COMBOBOX, self.OnSetSelection)

    def initSizers(self):
        filterParamsSizer = wx.BoxSizer(wx.VERTICAL)
        filterParamsSizer.Add(self.filterSetSelection, 0, wx.ALIGN_TOP)
        #filterParamsSizer.Add(self.filterTitleYourRate, 0, wx.ALIGN_TOP)
        filterSizer = wx.BoxSizer(wx.VERTICAL)
        filterSizer.Add(filterParamsSizer, 1, wx.EXPAND)
        filterSizer.Add(self. clearApplyButtons, 0, wx.ALIGN_BOTTOM)
        self.filterPanel.SetSizer(filterSizer)

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
        if self.filterSetSelection.selectedItem == 0:
            self.OnSetMovies(None)
        elif self.filterSetSelection.selectedItem == 1:
            self.OnSetSeries(None)
        elif self.filterSetSelection.selectedItem == 2:
            self.OnSetVideogames(None)

    def OnCAButton(self, event):
        if self.clearApplyButtons.clearClicked:
            self.SetStatusText('Filter cleared')
            self.myTitles.clearFilter(self.currentSet)
        elif self.clearApplyButtons.appliedClicked:
            self.SetStatusText('Filter applied')
            self.myTitles.applyFilter(self.currentSet)
        self.activeTitles = self.myTitles.getActiveTitles(self.currentSet)
        self.objectList.SetObjects(self.activeTitles)

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
            self.activeTitles = self.myTitles.getActiveTitles(self.currentSet)
            self.objectList.SetObjects(self.activeTitles)
            self.objectList.SetEmptyListMsg("No titles to show")
            self.objectList.SortBy(1)
            # set status info
            self.SetStatusText('File ' + self.filename + ' opened')
            self.SetStatusText(str(len(self.activeTitles)) + ' ' + self.currentSet, 1)
            self.fileIsOpen = True
            # enable controls
            self.clearApplyButtons.Enable()
            self.filterSetSelection.Enable()
            self.GetMenuBar().Enable(wx.ID_CLOSE, self.fileIsOpen)
        dlg.Destroy()

    def OnClose(self, event):
        """ Close current file """
        # set status info
        self.SetStatusText('File closed')
        self.SetStatusText('', 1)
        self.fileIsOpen = False
        # disable controls
        self.clearApplyButtons.Disable()
        self.filterSetSelection.Disable()
        self.GetMenuBar().Enable(wx.ID_CLOSE, self.fileIsOpen)
        # clear data
        self.myTitles.clearFilter(self.currentSet)
        self.myTitles.clearProps()
        self.activeTitles = []
        self.objectList.SetObjects(self.activeTitles)
        self.objectList.SetEmptyListMsg("Open .csv file\n(Ctrl+O)")

    def OnExit(self, event):
        self.Close(True)

    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "About IMDBstats\n\nA program that computes statistics from your movies rated on IMDB.com\n\nCreated by Diego Ruiz", "About IMDB statistics", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def OnSetMovies(self, event):
        self.SetTitle("IMDB statistics - Movies")
        self.currentSet = 'movies'
        self.activeTitles = self.myTitles.getActiveTitles(self.currentSet)
        self.objectList.SetObjects(self.activeTitles)
        self.SetStatusText('Showing movies')
        self.SetStatusText(str(len(self.activeTitles)) + ' movies', 1)

    def OnSetSeries(self, event):
        self.SetTitle("IMDB statistics - Series")
        self.currentSet = 'series'
        self.activeTitles = self.myTitles.getActiveTitles(self.currentSet)
        self.objectList.SetObjects(self.activeTitles)
        self.SetStatusText('Showing series')
        self.SetStatusText(str(len(self.activeTitles)) + ' series/episodes', 1)

    def OnSetVideogames(self, event):
        self.SetTitle("IMDB statistics - Videogames")
        self.currentSet = 'videogames'
        self.activeTitles = self.myTitles.getActiveTitles(self.currentSet)
        self.objectList.SetObjects(self.activeTitles)
        self.SetStatusText('Showing videogames')
        self.SetStatusText(str(len(self.activeTitles)) + ' videogames', 1)


if __name__ == '__main__':

    app = wx.App(False)
    mainWind = MainWindow(None, "IMDB statistics - Movies")
    mainWind.Show(True)

    app.MainLoop()
