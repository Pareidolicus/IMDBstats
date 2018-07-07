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


class ListSelectionPanel(wx.Panel):
    """
        Panel for selection of element in list (dropdown).
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
                                    )

        # sizers
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(staticTitle, 0, wx.ALIGN_CENTER)
        panelSizer.Add(self.comboBox, 0, wx.EXPAND)
        self.SetSizer(panelSizer)

        # events
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.OnListSelector)

    def OnListSelector(self, event):
        self.selectedItem = self.comboBox.GetCurrentSelection()
        event.Skip()


class SliderPanel(wx.Panel):
    """
        Panel for selection of number using a slider (integer number).
    """

    def __init__(self, parent, minValue, maxValue, title):
        super(SliderPanel, self).__init__(parent)

        self.selectedValueMin = (maxValue-minValue)/2
        self.selectedValueMax = (maxValue - minValue) / 2

        # controls
        staticTitle = wx.StaticText(self, -1, title)
        sliderStyle = wx.SL_HORIZONTAL | wx.SL_LABELS
        self.sliderCtrlMin = wx.Slider(self,
                                    value=self.selectedValueMin,
                                    minValue=minValue,
                                    maxValue=maxValue,
                                    style=sliderStyle
                                    )
        self.sliderCtrlMax = wx.Slider(self,
                                    value=self.selectedValueMax,
                                    minValue=minValue,
                                    maxValue=maxValue,
                                    style=sliderStyle
                                    )

        # sizers
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(staticTitle, 0, wx.ALIGN_CENTER)
        panelSizer.Add(self.sliderCtrlMin, 0, wx.EXPAND)
        panelSizer.Add(self.sliderCtrlMax, 0, wx.EXPAND)
        self.SetSizer(panelSizer)

        # events
        #self.sliderCtrl.Bind(wx.EVT_, self.OnSliderSelector)

    def OnSliderSelector(self, event):
        #self.selectedValue = self.sliderCtrl
        event.Skip()


class SpinCtrlPanel(wx.Panel):
    """
        Panel for selection of number using a spin control (real numbers).
    """

    def __init__(self, parent, minValue, maxValue, title):
        super(SpinCtrlPanel, self).__init__(parent)

        self.selectedValueMin = 0.0
        self.selectedValueMax = 10.0

        # controls
        staticTitle = wx.StaticText(self, -1, title)
        staticMinText = wx.StaticText(self, -1, 'Min: ')
        staticMaxText = wx.StaticText(self, -1, 'Max: ')
        spinPanelStyle = wx.SP_ARROW_KEYS | wx.SP_VERTICAL

        self.spinCtrlMin = wx.SpinCtrlDouble(self,
                                             value="",
                                             size=(55, -1),
                                             style=spinPanelStyle,
                                             min=minValue,
                                             max=maxValue,
                                             initial=self.selectedValueMin,
                                             inc=0.1
                                             )
        self.spinCtrlMax = wx.SpinCtrlDouble(self,
                                             value="",
                                             size=(55, -1),
                                             style=spinPanelStyle,
                                             min=minValue,
                                             max=maxValue,
                                             initial=self.selectedValueMax,
                                             inc=0.1
                                             )

        # sizers
        spinCtrlsSizer = wx.BoxSizer(wx.HORIZONTAL)
        spinCtrlsSizer.Add(staticMinText, 0, wx.EXPAND)
        spinCtrlsSizer.Add(self.spinCtrlMin, 0, wx.EXPAND)
        spinCtrlsSizer.Add(staticMaxText, 0, wx.EXPAND)
        spinCtrlsSizer.Add(self.spinCtrlMax, 0, wx.EXPAND)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(staticTitle, 0, wx.ALIGN_CENTER)
        panelSizer.Add(spinCtrlsSizer, 0, wx.ALIGN_CENTER)
        self.SetSizer(panelSizer)

        # events
        self.spinCtrlMin.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnSpinSelectorMin)
        self.spinCtrlMax.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnSpinSelectorMax)

    def OnSpinSelectorMin(self, event):
        self.selectedValueMin = self.spinCtrlMin.GetValue()
        if self.selectedValueMin > self.selectedValueMax:
            self.selectedValueMin = self.selectedValueMax
            self.spinCtrlMin.SetValue(self.selectedValueMin)
        event.Skip()

    def OnSpinSelectorMax(self, event):
        self.selectedValueMax = self.spinCtrlMax.GetValue()
        if self.selectedValueMax < self.selectedValueMin:
            self.selectedValueMax = self.selectedValueMin
            self.spinCtrlMax.SetValue(self.selectedValueMax)
        event.Skip()
