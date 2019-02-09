#!/usr/bin/env python
import wx
import MovieManager as movMng
import FilterPanels as fPnls
import InfoPanels as infoPnls
import os
import configparser


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
        self.titlesToShow = []
        self.customList = []
        self.currentSet = 'movies'
        self.settingsOptions = {'noConfBrowser':
                                "Don't ask for confirmation when open the browser after double-click on title."}
        self.settingsSelection = {key: False for key in self.settingsOptions}

        # init controls and sizers
        self.initControls()
        self.initSizers()

        # Menu and status bar
        self.initMenu()
        self.CreateStatusBar(2)
        self.SetStatusWidths([310, -1]) #self.filterPanel.GetSize().width

        # configuration file
        self.config = configparser.RawConfigParser()
        self.initConfigFile(self.configFileName)
        self.openLastFile()
        self.loadSettings()

        # set app icon
        ico = wx.Icon('icons/icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        # set window events
        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def initConfigFile(self, name):
        if self.config.read(name):
            return
        self.config.add_section('dirs')
        self.config.set('dirs', 'filename', '')
        self.config.set('dirs', 'dirname', '')
        self.config.add_section('settings')
        for key in self.settingsOptions:
            self.config.set('settings', key, 'false')
        try:
            with open(name, 'w') as configfile:
                self.config.write(configfile)
                configfile.close()
            print('Configuration file created: ' + name)
        except IOError:
            print('WARNING: Config file could not be created')

    def openLastFile(self):
        if not self.config.get('dirs', 'filename'):
            print('No last file path in configuration file')
            return
        self.filename = self.config.get('dirs', 'filename')
        self.dirname = self.config.get('dirs', 'dirname')
        if self.dirname:
            if self.openNewFile(self.dirname, self.filename):
                print('file ' + self.dirname + ' ' + self.filename + ' opened from config file')

    def loadSettings(self):
        if not self.config.has_section('settings'):
            return
        for key in self.settingsOptions:
            self.settingsSelection[key] = self.config.getboolean('settings', key)

    def saveSettings(self):
        if not self.config.has_section('settings'):
            self.config.add_section('settings')
        for key in self.settingsOptions:
            self.config.set('settings', key, self.settingsSelection[key])

    def initControls(self):
        # panels and control items
        self.filterPanel = fPnls.MainFilterPanel(self)
        self.infoNb = wx.Notebook(self)
        self.mainListPanel = infoPnls.ListPanel(self.infoNb)
        self.infoNb.AddPage(self.mainListPanel, "List")
        #self.infoNb.AddPage(wx.Panel(self.infoNb), "Graphs")

        # set Control events
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColumn)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivatedItem)

    def initSizers(self):
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.filterPanel, 0, wx.EXPAND)
        mainSizer.Add(self.infoNb, 1, wx.EXPAND)
        self.SetSizer(mainSizer)

    def initMenu(self):

        # Setting up the menu.
        filemenu = wx.Menu()
        setmenu = wx.Menu()
        helpmenu = wx.Menu()

        # Menu items
        openItem = filemenu.Append(wx.ID_OPEN, wx.EmptyString, " Open .csv file")
        closeItem = filemenu.Append(wx.ID_CLOSE, wx.EmptyString, " Close current file")
        closeItem.Enable(self.fileIsOpen)
        filemenu.AppendSeparator()
        settingsItem = filemenu.Append(wx.ID_ANY, "Settings...", " Edit settings")
        filemenu.AppendSeparator()
        exitItem = filemenu.Append(wx.ID_EXIT, wx.EmptyString, " Terminate the program")

        setMovieItem = setmenu.AppendRadioItem(-1, "Movies", "Movie set")
        setSeriesItem = setmenu.AppendRadioItem(-1, "Series", "Series set")
        setVideogamesItem = setmenu.AppendRadioItem(-1, "Videogames", "Videogames set")

        aboutItem = helpmenu.Append(wx.ID_ABOUT, wx.EmptyString, " About IMDBstats")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(setmenu, "&Set")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        menuBar.EnableTop(menuBar.FindMenu("Set"), self.fileIsOpen)

        # set Menu events
        self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
        self.Bind(wx.EVT_MENU, self.OnClose, closeItem)
        self.Bind(wx.EVT_MENU, self.OnSettings, settingsItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnSetSelectionMovies, setMovieItem)
        self.Bind(wx.EVT_MENU, self.OnSetSelectionSeries, setSeriesItem)
        self.Bind(wx.EVT_MENU, self.OnSetSelectionVideogames, setVideogamesItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnSetSelectionMovies(self, event):
        self.filterPanel.updateSetSelection(0)
        self.setSelectionUpdate(0)

    def OnSetSelectionSeries(self, event):
        self.filterPanel.updateSetSelection(1)
        self.setSelectionUpdate(1)

    def OnSetSelectionVideogames(self, event):
        self.filterPanel.updateSetSelection(2)
        self.setSelectionUpdate(2)

    def OnTextEnter(self, event):
        self.searchTitles()

    def OnButton(self, event):
        label = event.GetEventObject().GetLabel()
        if label in {'Clear', 'Apply'}:
            self.CAButtonClicked(label)
        elif label == 'customList':
            self.createCustomList()
        elif label == 'customDeleteList':
            self.customList = []
            self.setActiveTitles()
            self.setTitlesToShow()
            self.updateListView()
            self.SetStatusText('Custom List Removed')
        elif label == 'customAddList':
            self.addSelectedItemsToCustomList()
            self.SetStatusText('Title added to custom list (' + str(len(self.customList)) + ')')
        elif label in {'movies', 'series', 'videogames'}:
            setName = ['Movies', 'Series', 'Videogames'][self.filterPanel.selectedSet]
            itemId = self.GetMenuBar().FindMenuItem("Set", setName)
            self.GetMenuBar().Check(itemId, True)
            self.setSelectionUpdate(self.filterPanel.selectedSet)

    def showActiveList(self):
        self.setTitlesToShow()
        self.updateListView()
        self.SetStatusText('Showing active titles')

    def searchTitles(self):
        textToSearch = self.mainListPanel.topList.searchTerm
        if not textToSearch:
            self.showActiveList()
            return
        self.setTitlesToShow(True)
        self.updateListView()
        self.SetStatusText('Showing search result')

    def OnColumn(self, event):
        self.SetStatusText('Sorted by ' + self.mainListPanel.getColumnSelected())

    def OnActivatedItem(self, event):
        self.mainListPanel.openTitleLink(self.settingsSelection['noConfBrowser'])

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
        self.mainListPanel.topList.Disable()
        self.GetMenuBar().Enable(wx.ID_CLOSE, self.fileIsOpen)
        setMenuIdx = self.GetMenuBar().FindMenu("Set")
        self.GetMenuBar().EnableTop(setMenuIdx, self.fileIsOpen)
        # clear data
        self.filterPanel.clearProps()
        self.myTitles.clearFilter(self.currentSet)
        self.myTitles.clearProps()
        self.mainListPanel.setEmptyMessage("Open .csv file\n(Ctrl+O)")
        # update list view
        self.activeTitles = []
        self.titlesToShow = []
        self.customList = []
        self.updateListView(True)

    def OnSettings(self, event):
        keys = [x for x in self.settingsOptions]
        dlg = wx.MultiChoiceDialog(self, "Choose settings", "Settings",
                                   [self.settingsOptions[x] for x in keys],
                                   wx.DEFAULT_DIALOG_STYLE | wx.OK | wx.CANCEL)
        currentSelection = []
        for ind in range(len(keys)):
            if self.settingsSelection[keys[ind]]:
                currentSelection += [ind]
        dlg.SetSelections(currentSelection)

        if dlg.ShowModal() == wx.ID_OK:
            tempList = dlg.GetSelections()
            self.settingsSelection = {key: False for key in self.settingsOptions}
            for ind in tempList:
                self.settingsSelection[keys[ind]] = True

    def OnQuit(self, event):
        self.Close(True)

    def OnExit(self, event):
        self.updateConfigFile()
        event.Skip()

    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "About IMDBstats\n\nCompute statistics from your movies rated on IMDB.com\n\nCreated by Diego Ruiz\n\ngithub.com/Pareidolicus/IMDBstats", "About IMDB statistics", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def openNewFile(self, dirName, fileName):
        # open file
        if not self.myTitles.readFile(os.path.join(dirName, fileName)):
            return False
        # update list
        self.setActiveTitles()
        self.setTitlesToShow()
        self.updateListView()
        self.mainListPanel.setEmptyMessage("No titles to show")
        self.mainListPanel.sortColumn(1)
        # set status info
        self.SetStatusText('File ' + self.filename + ' opened')
        self.fileIsOpen = True
        self.filterPanel.EnableFilter(True)
        self.mainListPanel.topList.Enable()
        self.filterPanel.setFilterRanges(self.myTitles.filterRanges)
        self.filterPanel.setFilterParams(self.myTitles.filterParams)
        self.GetMenuBar().Enable(wx.ID_CLOSE, self.fileIsOpen)
        setMenuIdx = self.GetMenuBar().FindMenu("Set")
        self.GetMenuBar().EnableTop(setMenuIdx, self.fileIsOpen)
        return True

    def setSelectionUpdate(self, sel):
        titles = ['Movies', 'Series', 'Videogames']
        sets = ['movies', 'series', 'videogames']

        self.SetTitle("statsIMDB - " + titles[sel])
        self.currentSet = sets[sel]
        self.SetStatusText('Showing ' + sets[sel])
        self.setActiveTitles()
        self.setTitlesToShow()
        self.updateListView()

    def addSelectedItemsToCustomList(self):
        selectedTitles = self.mainListPanel.getSelectedTitlesID()
        tmpSet = set(self.customList)
        tmpSet.update(selectedTitles)
        self.customList = list(tmpSet)

    def createCustomList(self):
        self.setActiveTitles(True)
        self.setTitlesToShow()
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
        self.setTitlesToShow()
        self.updateListView()

    def setActiveTitles(self, custom=False):
        if custom:
            self.addSelectedItemsToCustomList()
            self.activeTitles = self.customList
        else:
            self.activeTitles = self.myTitles.getActiveTitlesID(self.currentSet)

    def setTitlesToShow(self, searchTitles=False):
        # if searchTitles, titlesToShow are result of search, not activeTitles
        if searchTitles:
            self.setTitlesToShowBySearching()
        else:
            self.titlesToShow = self.activeTitles

    def setTitlesToShowBySearching(self):
        textToSearch = self.mainListPanel.topList.searchTerm
        self.titlesToShow = self.myTitles.searchTitlesByName(self.currentSet, self.activeTitles, textToSearch)

    def updateListView(self, close=False):
        if close:
            self.SetStatusText('', 1)
        else:
            self.updateStatusListText()
        self.mainListPanel.objectList.SetElementsInList(self.myTitles.getTitlesByID(self.currentSet, self.titlesToShow))

    def updateStatusListText(self):
        tempText = ' '
        if self.currentSet == 'series':
            tempText = '/episodes'
        self.SetStatusText(str(len(self.titlesToShow)) + ' ' + self.currentSet + tempText, 1)

    def updateConfigFile(self):
        self.config.set('dirs', 'filename', self.filename)
        self.config.set('dirs', 'dirname', self.dirname)
        self.saveSettings()
        try:
            with open(self.configFileName, 'w') as configfile:
                self.config.write(configfile)
                configfile.close()
            print('Configuration file: ' + self.configFileName +
                  ' updated with filename ' + self.dirname + ' ' + self.filename)
        except IOError:
            print('WARNING: config file could not be opened')


if __name__ == '__main__':

    app = wx.App(False)
    mainWind = MainWindow(None, "IMDB statistics (Beta) - Movies")
    mainWind.Show(True)
    mainWind.Maximize()

    app.MainLoop()
