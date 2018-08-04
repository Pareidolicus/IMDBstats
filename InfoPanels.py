import wx
from ObjectListView import ObjectListView, ColumnDefn


class MainInfoPanel(wx.Notebook):
    """

    """
    def __init__(self, parent):
        super(MainInfoPanel, self).__init__(parent)

        # controls
        self.objectList = ObjectListClass(self)

        self.AddPage(self.objectList, "List")
        self.AddPage(wx.Panel(self), "Graphs")
        #infoNb.AddPage(wx.Panel(infoNb), "Records")


class ObjectListClass(ObjectListView):
    """

    """
    def __init__(self, parent):
        super(ObjectListClass, self).__init__(parent,
                                              style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES,
                                              cellEditMode="CELLEDIT_NONE",
                                              useAlternateBackColors=False)

        # attributes
        self.TitleColumnSelected = "Title"
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
        #self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemListSelected)
        #self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemListDeselected)

    def OnColumn(self, event):
        self.TitleColumnSelected = self.myColumns[event.GetColumn()].title
        event.Skip()
