import wx


class MainFilterPanel(wx.Panel):
    """

    """
    def __init__(self, parent):
        super(MainFilterPanel, self).__init__(parent)

        self.appliedClicked = False
        self.clearClicked = False
        self.selectedSet = 0
        self.selectedYourRate = [0, 10]
        self.fieldList = []
        self.filterParams = {}
        # clear all props!

        # controls
        self.filterSetSelection = ListSelectionPanel(self,
                                                     ['Movies', 'Series', 'Videogames'],
                                                     'Set')
        self.filterSetSelection.Disable()
        self.filterYourRateSelection = MinMaxSpinCtrlPanel(self, 0.0, 10.0, 'Your Rating')
        self.filterYourRateSelection.Disable()
        self.clearApplyButtons = ClearApplyButtonsPanel(self)
        self.clearApplyButtons.Disable()

        # sizers
        filterParamsSizer = wx.BoxSizer(wx.VERTICAL)
        filterParamsSizer.Add(self.filterSetSelection, 0, wx.EXPAND)
        filterParamsSizer.Add(self.filterYourRateSelection, 0, wx.EXPAND)
        filterSizer = wx.BoxSizer(wx.VERTICAL)
        filterSizer.Add(filterParamsSizer, 1, wx.EXPAND)
        filterSizer.Add(self. clearApplyButtons, 0, wx.EXPAND)
        self.SetSizer(filterSizer)

        # events
        self.clearApplyButtons.Bind(wx.EVT_BUTTON, self.OnCAButton)
        self.filterSetSelection.Bind(wx.EVT_COMBOBOX, self.OnSetSelection)
        self.filterYourRateSelection.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnYourRateSelection)

    def OnCAButton(self, event):
        self.clearClicked = self.clearApplyButtons.clearClicked
        self.appliedClicked = self.clearApplyButtons.appliedClicked
        event.Skip()

    def OnSetSelection(self, event):
        self.selectedSet = self.filterSetSelection.selectedItem
        event.Skip()

    def OnYourRateSelection(self, event):
        self.selectedYourRate = [self.filterYourRateSelection.selectedValueMin,
                                 self.filterYourRateSelection.selectedValueMax]
        event.Skip()

    def EnableFilter(self, enable):
        """
            Enable/disables all the filter panel.

        :param enable: True if all filter panel is enabled (not grey). False otherwise.
        a filter parameter can be disabled even if this filter panel is enabled.
        :return:
        """
        self.clearApplyButtons.Enable(enable)
        self.filterSetSelection.Enable(enable)
        self.filterYourRateSelection.Enable(enable)

    def setFilterFields(self, fieldList):
        self.fieldList = fieldList
        self.filterParams = {'movies': {self.fieldList[i]: [] for i in range(len(self.fieldList))},
                             'series': {self.fieldList[i]: [] for i in range(len(self.fieldList))},
                             'videogames': {self.fieldList[i]: [] for i in range(len(self.fieldList))}}

    def clearProps(self):
        self.appliedClicked = False
        self.clearClicked = False
        self.selectedSet = 0
        self.selectedYourRate = [0, 10]
        self.fieldList = []
        self.filterParams = {}

        self.showCurrentValues()

    def showCurrentValues(self):
        self.filterYourRateSelection.SetCurrentValues(self.selectedYourRate)


class ClearApplyButtonsPanel(wx.Panel):
    """
        Panel for buttons at bottom of main filter panel
        (clear and apply buttons)
    """
    def __init__(self, parent):
        super(ClearApplyButtonsPanel, self).__init__(parent)

        self.appliedClicked = True
        self.clearClicked = False

        # controls
        Applybutton = wx.Button(self, -1, "Apply")
        Clearbutton = wx.Button(self, -1, "Clear")

        # sizers
        filterButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        filterButtonsSizer.Add(Clearbutton, 1, wx.EXPAND)
        filterButtonsSizer.Add(Applybutton, 1, wx.EXPAND)
        self.SetSizer(filterButtonsSizer)

        # events
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

        self.selectedValue = (maxValue-minValue)/2

        # controls
        staticTitle = wx.StaticText(self, -1, title)
        sliderStyle = wx.SL_HORIZONTAL | wx.SL_LABELS
        self.sliderCtrl = wx.Slider(self,
                                    value=self.selectedValue,
                                    minValue=minValue,
                                    maxValue=maxValue,
                                    style=sliderStyle
                                    )

        # sizers
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(staticTitle, 0, wx.ALIGN_CENTER)
        panelSizer.Add(self.sliderCtrl, 0, wx.EXPAND)
        self.SetSizer(panelSizer)

        # events
        #self.sliderCtrl.Bind(wx.EVT_, self.OnSliderSelector)

    def OnSliderSelector(self, event):
        event.Skip()


class MinMaxSpinCtrlPanel(wx.Panel):
    """
        Panel for selection of number using a spin control (real numbers).
    """

    def __init__(self, parent, minValue, maxValue, title):
        super(MinMaxSpinCtrlPanel, self).__init__(parent)

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

    def SetCurrentValues(self, values):
        self.spinCtrlMin.SetValue(values[0])
        self.spinCtrlMax.SetValue(values[1])
