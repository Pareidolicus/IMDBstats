import wx
import wx.lib.scrolledpanel as scrolled


class MainFilterPanel(wx.Panel):
    """
        Main panel for search filter settings
    """
    def __init__(self, parent):
        super(MainFilterPanel, self).__init__(parent)

        self.selectedSet = 0
        self.setNames = ['movies', 'series', 'videogames']
        self.filterParams = {}
        self.filterRanges = {}

        # controls
        self.scrollPanel = scrolled.ScrolledPanel(self)
        self.scrollPanel.SetupScrolling(scroll_x=False)
        self.filterSetSelection = ListSelectionPanel(self.scrollPanel,
                                                     ['Movies', 'Series', 'Videogames'],
                                                     'Set')
        self.filterYourRateSelection = MinMaxSpinCtrlPanel(self.scrollPanel, 0.0, 10.0, 0.1, 'Your Rating')
        self.filterIMDBRateSelection = MinMaxSpinCtrlPanel(self.scrollPanel, 0.0, 10.0, 0.1, 'IMDB Rating')
        self.filterRuntimeSelection = MinMaxSpinCtrlPanel(self.scrollPanel, 0, 100, 1, 'Runtime (min)')
        self.clearApplyButtons = ClearApplyButtonsPanel(self)
        self.customListButton = wx.Button(self, -1, "Custom List")
        self.customListButton.Disable()

        # sizers
        filterParamsSizer = wx.BoxSizer(wx.VERTICAL)
        filterParamsSizer.Add(self.filterSetSelection, 0, wx.EXPAND)
        filterParamsSizer.Add(self.filterYourRateSelection, 0, wx.EXPAND)
        filterParamsSizer.Add(self.filterIMDBRateSelection, 0, wx.EXPAND)
        filterParamsSizer.Add(self.filterRuntimeSelection, 0, wx.EXPAND)
        self.scrollPanel.SetSizer(filterParamsSizer)
        filterSizer = wx.BoxSizer(wx.VERTICAL)
        filterSizer.Add(self.scrollPanel, 1, wx.EXPAND)
        filterSizer.Add(self.customListButton, 0, wx.EXPAND)
        filterSizer.Add(self.clearApplyButtons, 0, wx.EXPAND)
        self.SetSizer(filterSizer)

        # events
        self.filterSetSelection.Bind(wx.EVT_COMBOBOX, self.OnSetSelection)
        self.filterYourRateSelection.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnYourRateSelection)
        self.filterYourRateSelection.Bind(wx.EVT_CHECKBOX, self.OnYourRateSelectionCheckBox)
        self.filterIMDBRateSelection.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnIMDBRateSelection)
        self.filterIMDBRateSelection.Bind(wx.EVT_CHECKBOX, self.filterIMDBRateSelectionCheckBox)
        self.filterRuntimeSelection.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnRuntimeSelection)
        self.filterRuntimeSelection.Bind(wx.EVT_CHECKBOX, self.filterRuntimeSelectionCheckBox)

    def OnSetSelection(self, event):
        self.selectedSet = self.filterSetSelection.selectedItem
        self.updateFilterRanges(self.setNames[self.selectedSet])
        self.showCurrentValues()
        event.Skip()

    def OnYourRateSelection(self, event):
        setName = self.setNames[self.selectedSet]
        self.filterParams[setName]['Your Rating'] = [self.filterYourRateSelection.selectedValueMin,
                                                     self.filterYourRateSelection.selectedValueMax]

    def OnYourRateSelectionCheckBox(self, event):
        setName = self.setNames[self.selectedSet]
        if self.filterYourRateSelection.isActive:
            self.filterParams[setName]['Your Rating'] = self.filterRanges[setName]['Your Rating']
        else:
            self.filterParams[setName]['Your Rating'] = []

    def OnIMDBRateSelection(self, event):
        setName = self.setNames[self.selectedSet]
        self.filterParams[setName]['IMDb Rating'] = [self.filterIMDBRateSelection.selectedValueMin,
                                                     self.filterIMDBRateSelection.selectedValueMax]

    def filterIMDBRateSelectionCheckBox(self, event):
        setName = self.setNames[self.selectedSet]
        if self.filterIMDBRateSelection.isActive:
            self.filterParams[setName]['IMDb Rating'] = self.filterRanges[setName]['IMDb Rating']
        else:
            self.filterParams[setName]['IMDb Rating'] = []

    def OnRuntimeSelection(self, event):
        setName = self.setNames[self.selectedSet]
        self.filterParams[setName]['Runtime (mins)'] = [self.filterRuntimeSelection.selectedValueMin,
                                                        self.filterRuntimeSelection.selectedValueMax]

    def filterRuntimeSelectionCheckBox(self, event):
        setName = self.setNames[self.selectedSet]
        if self.filterRuntimeSelection.isActive:
            self.filterParams[setName]['Runtime (mins)'] = self.filterRanges[setName]['Runtime (mins)']
        else:
            self.filterParams[setName]['Runtime (mins)'] = []

    def EnableFilter(self, enable):
        """
            Enable/disables all the filter panel.

        :param enable: True if all filter panel is enabled (not grey). False otherwise.
        a filter parameter can be disabled even if this filter panel is enabled.
        :return:
        """
        self.clearApplyButtons.Enable(enable)
        self.customListButton.Enable(enable)
        self.filterSetSelection.Enable(enable)
        self.filterYourRateSelection.Enable(enable)
        self.filterIMDBRateSelection.Enable(enable)
        self.filterRuntimeSelection.Enable(enable)

    def setFilterRanges(self, filterRanges):
        setName = self.setNames[self.selectedSet]
        self.filterRanges = filterRanges
        self.updateFilterRanges(setName)

    def setFilterParams(self, filter):
        self.filterParams = filter
        self.showCurrentValues()

    def updateFilterRanges(self, setName):
        runtimeRange = self.filterRanges[setName]['Runtime (mins)']
        self.filterRuntimeSelection.SetSpinSelectorRanges(runtimeRange)

    def clearProps(self):
        self.selectedSet = 0
        self.filterParams = {}
        self.filterRanges = {}

        self.resetFilter()

    def showCurrentValues(self):
        setName = self.setNames[self.selectedSet]
        self.filterYourRateSelection.SetCurrentValues(self.filterParams[setName]['Your Rating'])
        self.filterIMDBRateSelection.SetCurrentValues(self.filterParams[setName]['IMDb Rating'])
        self.filterRuntimeSelection.SetCurrentValues(self.filterParams[setName]['Runtime (mins)'])

    def resetFilter(self):
        self.filterYourRateSelection. SetSpinSelectorRanges([0, 10])
        self.filterYourRateSelection.SetCurrentValues([])
        self.filterIMDBRateSelection.SetSpinSelectorRanges([0, 10])
        self.filterIMDBRateSelection.SetCurrentValues([])
        self.filterRuntimeSelection.SetSpinSelectorRanges([0, 100])
        self.filterRuntimeSelection.SetCurrentValues([])


class ClearApplyButtonsPanel(wx.Panel):
    """
        Panel for buttons at bottom of main filter panel
        (clear and apply buttons)
    """
    def __init__(self, parent):
        super(ClearApplyButtonsPanel, self).__init__(parent)

        # controls
        Applybutton = wx.Button(self, -1, "Apply")
        Clearbutton = wx.Button(self, -1, "Clear")
        self.Disable()

        # sizers
        filterButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        filterButtonsSizer.Add(Clearbutton, 1, wx.EXPAND)
        filterButtonsSizer.Add(Applybutton, 1, wx.EXPAND)
        self.SetSizer(filterButtonsSizer)


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
        self.Disable()

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

    def __init__(self, parent, minValue, maxValue, inc, title):
        super(MinMaxSpinCtrlPanel, self).__init__(parent)

        self.selectedValueMin = minValue
        self.selectedValueMax = maxValue
        self.isActive = False

        # controls
        self.checkBox = wx.CheckBox(self, -1, title)
        staticMinText = wx.StaticText(self, -1, 'Min: ')
        staticMaxText = wx.StaticText(self, -1, 'Max: ')
        spinPanelStyle = wx.SP_ARROW_KEYS | wx.SP_VERTICAL
        self.spinCtrlMin = wx.SpinCtrlDouble(self,
                                             value="",
                                             size=(60, -1),
                                             style=spinPanelStyle,
                                             min=minValue,
                                             max=maxValue,
                                             initial=self.selectedValueMin,
                                             inc=inc
                                             )
        self.spinCtrlMin.Disable()
        self.spinCtrlMax = wx.SpinCtrlDouble(self,
                                             value="",
                                             size=(60, -1),
                                             style=spinPanelStyle,
                                             min=minValue,
                                             max=maxValue,
                                             initial=self.selectedValueMax,
                                             inc=inc
                                             )
        self.spinCtrlMax.Disable()
        self.Disable()

        # sizers
        spinCtrlsSizer = wx.BoxSizer(wx.HORIZONTAL)
        spinCtrlsSizer.Add(staticMinText, 0, wx.EXPAND)
        spinCtrlsSizer.Add(self.spinCtrlMin, 0, wx.EXPAND)
        spinCtrlsSizer.Add(staticMaxText, 0, wx.EXPAND)
        spinCtrlsSizer.Add(self.spinCtrlMax, 0, wx.EXPAND)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.checkBox, 0, wx.ALIGN_LEFT)
        panelSizer.Add(spinCtrlsSizer, 0, wx.ALIGN_CENTER)
        self.SetSizer(panelSizer)

        # events
        self.spinCtrlMin.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnSpinSelectorMin)
        self.spinCtrlMax.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnSpinSelectorMax)
        self.checkBox.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)

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

    def OnCheckBox(self, event):
        self.isActive = not self.isActive
        self.enableSpinSelectors(self.isActive)
        if not self.isActive:
            self.SetCurrentValues([])
        event.Skip()

    def SetCurrentValues(self, values):
        if values:
            if not self.isActive:
                # it should be enabled!
                self.isActive = True
                self.checkBox.SetValue(self.isActive)
                self.enableSpinSelectors(self.isActive)
            self.selectedValueMin = values[0]
            self.selectedValueMax = values[1]
        else:
            if self.isActive:
                # it should be disabled!
                self.isActive = False
                self.checkBox.SetValue(self.isActive)
                self.enableSpinSelectors(self.isActive)
            self.selectedValueMin = self.spinCtrlMin.GetRange()[0]
            self.selectedValueMax = self.spinCtrlMin.GetRange()[1]
        self.spinCtrlMin.SetValue(self.selectedValueMin)
        self.spinCtrlMax.SetValue(self.selectedValueMax)

    def SetSpinSelectorRanges(self, ranges):
        if ranges:
            self.spinCtrlMin.SetRange(ranges[0],
                                      ranges[1])
            self.spinCtrlMax.SetRange(ranges[0],
                                      ranges[1])

    def enableSpinSelectors(self, enable):
        self.spinCtrlMin.Enable(enable)
        self.spinCtrlMax.Enable(enable)
