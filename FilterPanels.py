import wx


class ClearApplyButtonsPanel(wx.Panel):
    """
        Panel for buttons at bottom of main filter panel
        (clear and apply buttons)
    """
    def __init__(self, parent):
        super(ClearApplyButtonsPanel, self).__init__(parent)

        self.appliedClicked = False
        self.clearClicked = False

        #controls
        Applybutton = wx.Button(self, -1, "Apply")
        Clearbutton = wx.Button(self, -1, "Clear")

        #sizers
        filterButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        filterButtonsSizer.Add(Clearbutton, 1, wx.EXPAND)
        filterButtonsSizer.Add(Applybutton, 1, wx.EXPAND)
        self.SetSizer(filterButtonsSizer)

        #events
        Applybutton.Bind(wx.EVT_BUTTON, self.OnApply)
        Clearbutton.Bind(wx.EVT_BUTTON, self.OnClear)

    def OnClear(self, event):
        self.clearClicked = True
        self.appliedClicked = False
        event.Skip()

    def OnApply(self, event):
        self.clearClicked = False
        self.appliedClicked = True
        event.Skip()

    # def OnButton(self, event):
    #     print('button clicked')
    #     event.Skip()


class ListSelectionPanel(wx.Panel):
    """
        Panel for selection of element in list (desplegable).
        For example for selection of set movies, series or videogames
    """

    def __init__(self, parent, inputList, title):
        super(ListSelectionPanel, self).__init__(parent)

        self.selectedItem = 0

        # controls
        staticTitle = wx.StaticText(self, -1, title)
        self.comboBox = wx.ComboBox(self,
                               value='Movies',
                               choices=inputList,
                               style=wx.CB_DROPDOWN
                               | wx.CB_READONLY
                               | wx.CB_SORT,
                               )

        # sizers
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(staticTitle, 0, wx.EXPAND)
        panelSizer.Add(self.comboBox, 0, wx.EXPAND)
        self.SetSizer(panelSizer)

        # events
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.OnListSelector)

    def OnListSelector(self, event):
        self.selectedItem = self.comboBox.GetCurrentSelection()
        event.Skip()
