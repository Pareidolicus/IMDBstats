import wx
import wx.adv
from ObjectListView import ObjectListView, ColumnDefn


class ListPanel(wx.Panel):
    def __init__(self, parent):
        super(ListPanel, self).__init__(parent)

        # attributes

        # controls
        self.topList = topListPanel(self)
        self.objectList = ObjectListClass(self)

        # sizers
        listSizer = wx.BoxSizer(wx.VERTICAL)
        listSizer.Add((0, 5))
        listSizer.Add(self.topList, 0, wx.EXPAND)
        listSizer.Add((0, 5))
        listSizer.Add(self.objectList, 1, wx.EXPAND)
        self.SetSizer(listSizer)

        # events
        self.topList.customListButton.Bind(wx.EVT_BUTTON, self.OnCustomListButton)

    def OnCustomListButton(self, event):
        numSelected = self.objectList.GetSelectedItemCount()
        if numSelected == 0:
            dlg = wx.MessageDialog(self,
                                   "Select at least one title",
                                   "Custom List",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            return
        event.Skip()

    def openTitleLink(self, noConfBrowser):
        if noConfBrowser:
            wx.LaunchDefaultBrowser(self.objectList.activatedItem['URL'])
            return
        dlg = wx.MessageDialog(self,
                               "Show '" + self.objectList.activatedItem['Title'] + "' on imdb.com",
                               "Open browser",
                               wx.OK_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_OK:
            wx.LaunchDefaultBrowser(self.objectList.activatedItem['URL'])

    def sortColumn(self, colIdx):
        self.objectList.SortBy(colIdx)

    def setEmptyMessage(self, message):
        self.objectList.SetEmptyListMsg(message)

    def getColumnSelected(self):
        return self.objectList.TitleColumnSelected

    def getSelectedTitlesID(self):
        return [title['Const'] for title in self.objectList.GetSelectedObjects()]


class topListPanel(wx.Panel):
    """
        Panel for controls at top of list panel
        (for example for set selection, custom list, search by word...)
    """
    def __init__(self, parent):
        super(topListPanel, self).__init__(parent)

        # attributes
        self.searchTerm = ''

        # controls
        searchTextStatic = wx.StaticText(self, -1, "Search by Title:")
        self.searchTextCtrl = wx.TextCtrl(self, -1,
                                          style=wx.TE_PROCESS_ENTER | wx.TE_RICH)
        self.searchButton = wx.Button(self, -1,
                                      label="search",
                                      style=wx.BU_NOTEXT,
                                      size=wx.Size(32, 32))
        self.showActiveListButton = wx.Button(self, -1,
                                              label="activeList",
                                              style=wx.BU_NOTEXT,
                                              size=wx.Size(32, 32))
        self.customAddListButton = wx.Button(self, -1,
                                          label="customAddList",
                                          style=wx.BU_NOTEXT,
                                          size=wx.Size(32, 32))
        self.customListButton = wx.Button(self, -1,
                                          label="customList",
                                          style=wx.BU_NOTEXT,
                                          size=wx.Size(32, 32))
        self.customDeleteListButton = wx.Button(self, -1,
                                                label="customDeleteList",
                                                style=wx.BU_NOTEXT,
                                                size=wx.Size(32, 32))

        # set images to buttons
        self.searchButton.SetBitmap(wx.Bitmap('icons/searchIcon.png', wx.BITMAP_TYPE_PNG))
        self.showActiveListButton.SetBitmap(wx.Bitmap('icons/listActiveIcon.png', wx.BITMAP_TYPE_PNG))
        self.customAddListButton.SetBitmap(wx.Bitmap('icons/listCustomAddIcon.png', wx.BITMAP_TYPE_PNG))
        self.customListButton.SetBitmap(wx.Bitmap('icons/listCustomIcon.png', wx.BITMAP_TYPE_PNG))
        self.customDeleteListButton.SetBitmap(wx.Bitmap('icons/listCustomDeleteIcon.png', wx.BITMAP_TYPE_PNG))

        # sizers
        topListSizer = wx.BoxSizer(wx.HORIZONTAL)
        topListSizer.Add((10, 0))
        topListSizer.Add(searchTextStatic, 0, wx.ALIGN_CENTER)
        topListSizer.Add((5, 0))
        topListSizer.Add(self.searchTextCtrl, 1, wx.ALIGN_CENTER)
        topListSizer.Add((10, 0))
        topListSizer.Add(self.searchButton, 0, wx.ALIGN_CENTER)
        topListSizer.Add((10, 0))
        topListSizer.Add(self.showActiveListButton, 0, wx.ALIGN_CENTER)
        topListSizer.Add((5, 0))
        topListSizer.Add(self.customAddListButton, 0, wx.ALIGN_CENTER)
        topListSizer.Add((5, 0))
        topListSizer.Add(self.customListButton, 0, wx.ALIGN_CENTER)
        topListSizer.Add((5, 0))
        topListSizer.Add(self.customDeleteListButton, 0, wx.ALIGN_CENTER)
        topListSizer.Add((5, 0))
        self.SetSizer(topListSizer)

        # events
        self.searchButton.Bind(wx.EVT_BUTTON, self.OnSearchButton)
        # self.searchTextCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnSearchButton)
        self.searchTextCtrl.Bind(wx.EVT_TEXT, self.OnSearchButton)

    def OnSearchButton(self, event):
        self.searchTerm = self.searchTextCtrl.GetValue()
        event.Skip()


class ObjectListClass(ObjectListView):

    def __init__(self, parent):
        super(ObjectListClass, self).__init__(parent,
                                              style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES,
                                              cellEditMode="CELLEDIT_NONE",
                                              useAlternateBackColors=False)

        # attributes
        self.TitleColumnSelected = "Title"
        self.activatedItem = {}
        self.myColumns = [
            ColumnDefn(title="Year", align="center", valueGetter="Year", isEditable=False, fixedWidth=75),
            ColumnDefn(title="Title", width=250, valueGetter="Title", isEditable=False, minimumWidth=200, isSearchable=True),
            ColumnDefn(title="IMDb Rating", align="center", valueGetter="IMDb Rating", isEditable=False, fixedWidth=125),
            ColumnDefn(title="Your Rating", align="center", valueGetter="Your Rating", isEditable=False, fixedWidth=125),
            ColumnDefn(title="Date Rated", align="center", valueGetter="Date Rated", isEditable=False, fixedWidth=125),
            ColumnDefn(title="Genres", width=250, valueGetter="Genres", minimumWidth=100, isEditable=False),
            ColumnDefn(title="Directors", width=250, valueGetter="Directors", minimumWidth=100, isEditable=False),
            ColumnDefn(title="Num Votes", valueGetter="Num Votes", isEditable=False, fixedWidth=125),
            ColumnDefn(title="Runtime (min.)", valueGetter="Runtime (mins)", isEditable=False, fixedWidth=150)]

        # initial settings
        self.SetEmptyListMsg("Open .csv file\n(Ctrl+O)")
        self.SetColumns(self.myColumns)

        # events
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColumn)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemListActivated)

    def OnColumn(self, event):
        self.TitleColumnSelected = self.myColumns[event.GetColumn()].title
        event.Skip()

    def OnItemListActivated(self, event):
        self.activatedItem = self.GetObjectAt(event.GetIndex())
        event.Skip()

    def SetElementsInList(self, activeTitles):
        self.SetObjects(activeTitles)


