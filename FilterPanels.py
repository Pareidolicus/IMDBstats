import wx
import wx.lib.scrolledpanel as scrolled
import wx.adv


class MainFilterPanel(wx.Panel):
    """
        Main panel for search filter settings
    """
    def __init__(self, parent):
        super(MainFilterPanel, self).__init__(parent)

        vert_spacer = 15
        self.selectedSet = 0
        self.setNames = ['movies', 'series', 'videogames']
        self.filterParams = {}
        self.filterRanges = {}

        # controls
        self.filterSetSelection = buttonsSetSelection(self)
        self.scrollPanel = scrolled.ScrolledPanel(self, style=wx.BORDER_SIMPLE)
        self.scrollPanel.SetupScrolling(scroll_x=False)
        self.filterYourRateSelection = MinMaxSpinCtrlPanel(self.scrollPanel, 0.0, 10.0, 0.1, 90, 'Your Rating')
        self.filterIMDBRateSelection = MinMaxSpinCtrlPanel(self.scrollPanel, 0.0, 10.0, 0.1, 90, 'IMDB Rating')
        self.filterRuntimeSelection = MinMaxSpinCtrlPanel(self.scrollPanel, 0, 100, 1, 90, 'Runtime (min)', True)
        self.filterNumVotesSelection = MinMaxSpinCtrlPanel(self.scrollPanel, 0, 100000, 500, 90, 'Num. Votes', True)
        self.filterDateReleaseSelection = MinMaxDateCtrlPanel(self.scrollPanel, '1900-01-01', '2100-01-01', -1, 'Release Date')
        self.filterDateRatedSelection = MinMaxDateCtrlPanel(self.scrollPanel, '1900-01-01', '2100-01-01', -1, 'Date Rated')
        self.filterGenreSelection = CheckListBoxPanel(self.scrollPanel, [], 200, 'Genres')
        self.filterDirectorSelection = CheckListBoxPanel(self.scrollPanel, [], 200, 'Directors')

        self.clearApplyButtons = ClearApplyButtonsPanel(self)

        # sizers
        filterParamsSizer = wx.BoxSizer(wx.VERTICAL)
        filterParamsSizer.Add((0, vert_spacer))
        filterParamsSizer.Add(self.filterYourRateSelection, 0, wx.EXPAND)
        filterParamsSizer.Add((0, vert_spacer))
        filterParamsSizer.Add(self.filterIMDBRateSelection, 0, wx.EXPAND)
        filterParamsSizer.Add((0, vert_spacer))
        filterParamsSizer.Add(self.filterRuntimeSelection, 0, wx.EXPAND)
        filterParamsSizer.Add((0, vert_spacer))
        filterParamsSizer.Add(self.filterNumVotesSelection, 0, wx.EXPAND)
        filterParamsSizer.Add((0, vert_spacer))
        filterParamsSizer.Add(self.filterDateReleaseSelection, 0, wx.EXPAND)
        filterParamsSizer.Add((0, vert_spacer))
        filterParamsSizer.Add(self.filterDateRatedSelection, 0, wx.EXPAND)
        filterParamsSizer.Add((0, vert_spacer))
        filterParamsSizer.Add(self.filterGenreSelection, 0, wx.EXPAND)
        filterParamsSizer.Add((0, vert_spacer))
        filterParamsSizer.Add(self.filterDirectorSelection, 0, wx.EXPAND)
        self.scrollPanel.SetSizer(filterParamsSizer)

        filterSizer = wx.BoxSizer(wx.VERTICAL)
        filterSizer.Add((0, vert_spacer))
        filterSizer.Add(self.filterSetSelection, 0, wx.ALIGN_CENTER)
        filterSizer.Add((0, vert_spacer))
        filterSizer.Add(self.scrollPanel, 1, wx.EXPAND)
        filterSizer.Add(self.clearApplyButtons, 0, wx.EXPAND)
        self.SetSizer(filterSizer)

        # events
        self.filterSetSelection.Bind(wx.EVT_BUTTON, self.OnSetSelection)
        self.filterYourRateSelection.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnYourRateSelection)
        self.filterYourRateSelection.Bind(wx.EVT_CHECKBOX, self.OnYourRateSelectionCheckBox)
        self.filterIMDBRateSelection.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnIMDBRateSelection)
        self.filterIMDBRateSelection.Bind(wx.EVT_CHECKBOX, self.OnIMDBRateSelectionCheckBox)
        self.filterRuntimeSelection.Bind(wx.EVT_SPINCTRL, self.OnRuntimeSelection)
        self.filterRuntimeSelection.Bind(wx.EVT_CHECKBOX, self.OnRuntimeSelectionCheckBox)
        self.filterNumVotesSelection.Bind(wx.EVT_SPINCTRL, self.OnNumVotesSelection)
        self.filterNumVotesSelection.Bind(wx.EVT_CHECKBOX, self.OnNumVotesSelectionCheckBox)
        self.filterDateReleaseSelection.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateReleaseSelection)
        self.filterDateReleaseSelection.Bind(wx.EVT_CHECKBOX, self.OnDateReleaseSelectionCheckBox)
        self.filterDateRatedSelection.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateRatedSelection)
        self.filterDateRatedSelection.Bind(wx.EVT_CHECKBOX, self.OnDateRatedSelectionCheckBox)
        self.filterGenreSelection.Bind(wx.EVT_CHECKLISTBOX, self.OnGenreSelection)
        self.filterGenreSelection.Bind(wx.EVT_CHECKBOX, self.OnGenreSelectionCheckBox)
        self.filterDirectorSelection.Bind(wx.EVT_CHECKLISTBOX, self.OnDirectorSelection)
        self.filterDirectorSelection.Bind(wx.EVT_CHECKBOX, self.OnDirectorSelectionCheckBox)

    def OnSetSelection(self, event):
        label = event.GetEventObject().GetLabel()
        self.selectedSet = self.setNames.index(label)
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

    def OnIMDBRateSelectionCheckBox(self, event):
        setName = self.setNames[self.selectedSet]
        if self.filterIMDBRateSelection.isActive:
            self.filterParams[setName]['IMDb Rating'] = self.filterRanges[setName]['IMDb Rating']
        else:
            self.filterParams[setName]['IMDb Rating'] = []

    def OnRuntimeSelection(self, event):
        setName = self.setNames[self.selectedSet]
        self.filterParams[setName]['Runtime (mins)'] = [self.filterRuntimeSelection.selectedValueMin,
                                                        self.filterRuntimeSelection.selectedValueMax]

    def OnRuntimeSelectionCheckBox(self, event):
        setName = self.setNames[self.selectedSet]
        if self.filterRuntimeSelection.isActive:
            self.filterParams[setName]['Runtime (mins)'] = self.filterRanges[setName]['Runtime (mins)']
        else:
            self.filterParams[setName]['Runtime (mins)'] = []

    def OnNumVotesSelection(self, event):
        setName = self.setNames[self.selectedSet]
        self.filterParams[setName]['Num Votes'] = [self.filterNumVotesSelection.selectedValueMin,
                                                   self.filterNumVotesSelection.selectedValueMax]

    def OnNumVotesSelectionCheckBox(self, event):
        setName = self.setNames[self.selectedSet]
        if self.filterNumVotesSelection.isActive:
            self.filterParams[setName]['Num Votes'] = self.filterRanges[setName]['Num Votes']
        else:
            self.filterParams[setName]['Num Votes'] = []

    def OnDateReleaseSelection(self, event):
        setName = self.setNames[self.selectedSet]
        self.filterParams[setName]['Release Date'] = [self.filterDateReleaseSelection.selectedValueMin,
                                                      self.filterDateReleaseSelection.selectedValueMax]

    def OnDateReleaseSelectionCheckBox(self, event):
        setName = self.setNames[self.selectedSet]
        if self.filterDateReleaseSelection.isActive:
            self.filterParams[setName]['Release Date'] = self.filterRanges[setName]['Release Date']
        else:
            self.filterParams[setName]['Release Date'] = []

    def OnDateRatedSelection(self, event):
        setName = self.setNames[self.selectedSet]
        self.filterParams[setName]['Date Rated'] = [self.filterDateRatedSelection.selectedValueMin,
                                                    self.filterDateRatedSelection.selectedValueMax]

    def OnDateRatedSelectionCheckBox(self, event):
        setName = self.setNames[self.selectedSet]
        if self.filterDateRatedSelection.isActive:
            self.filterParams[setName]['Date Rated'] = self.filterRanges[setName]['Date Rated']
        else:
            self.filterParams[setName]['Date Rated'] = []

    def OnGenreSelection(self, event):
        setName = self.setNames[self.selectedSet]
        self.filterParams[setName]['Genres'] = self.filterGenreSelection.currentSelection.copy()

    def OnGenreSelectionCheckBox(self, event):
        setName = self.setNames[self.selectedSet]
        if self.filterGenreSelection.isActive:
            self.filterParams[setName]['Genres'] = self.filterGenreSelection.currentSelection.copy()
        else:
            self.filterParams[setName]['Genres'] = []

    def OnDirectorSelection(self, event):
        setName = self.setNames[self.selectedSet]
        self.filterParams[setName]['Directors'] = self.filterDirectorSelection.currentSelection.copy()

    def OnDirectorSelectionCheckBox(self, event):
        setName = self.setNames[self.selectedSet]
        if self.filterDirectorSelection.isActive:
            self.filterParams[setName]['Directors'] = self.filterDirectorSelection.currentSelection.copy()
        else:
            self.filterParams[setName]['Directors'] = []

    def updateSetSelection(self, setId):
        self.selectedSet = setId
        self.updateFilterRanges(self.setNames[self.selectedSet])
        self.showCurrentValues()

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
        self.filterIMDBRateSelection.Enable(enable)
        self.filterRuntimeSelection.Enable(enable)
        self.filterNumVotesSelection.Enable(enable)
        self.filterDateReleaseSelection.Enable(enable)
        self.filterDateRatedSelection.Enable(enable)
        self.filterGenreSelection.Enable(enable)
        self.filterDirectorSelection.Enable(enable)

    def setFilterRanges(self, filterRanges):
        setName = self.setNames[self.selectedSet]
        self.filterRanges = filterRanges
        self.updateFilterRanges(setName)

    def setFilterParams(self, filterParams):
        self.filterParams = filterParams
        self.showCurrentValues()

    def updateFilterRanges(self, setName):
        runtimeRange = self.filterRanges[setName]['Runtime (mins)']
        if not runtimeRange:
            runtimeRange = [0, 100]
        self.filterRuntimeSelection.SetSpinSelectorRanges(runtimeRange)

        NumVotesRange = self.filterRanges[setName]['Num Votes']
        self.filterNumVotesSelection.SetSpinSelectorRanges(NumVotesRange)

        DateReleaseRange = self.filterRanges[setName]['Release Date']
        self.filterDateReleaseSelection.SetDateSelectorRanges(DateReleaseRange)

        DateRatedRange = self.filterRanges[setName]['Date Rated']
        self.filterDateRatedSelection.SetDateSelectorRanges(DateRatedRange)

        GenresRange = self.filterRanges[setName]['Genres']
        self.filterGenreSelection.SetCheckListSelectorRanges(GenresRange)

        DirectorsRange = self.filterRanges[setName]['Directors']
        self.filterDirectorSelection.SetCheckListSelectorRanges(DirectorsRange)

    def clearProps(self):
        self.filterParams = {}
        self.filterRanges = {}

        self.resetFilter()

    def showCurrentValues(self):
        setName = self.setNames[self.selectedSet]
        self.filterYourRateSelection.SetCurrentValues(self.filterParams[setName]['Your Rating'])
        self.filterIMDBRateSelection.SetCurrentValues(self.filterParams[setName]['IMDb Rating'])
        self.filterRuntimeSelection.SetCurrentValues(self.filterParams[setName]['Runtime (mins)'])
        self.filterNumVotesSelection.SetCurrentValues(self.filterParams[setName]['Num Votes'])
        self.filterDateReleaseSelection.SetCurrentValues(self.filterParams[setName]['Release Date'])
        self.filterDateRatedSelection.SetCurrentValues(self.filterParams[setName]['Date Rated'])
        self.filterGenreSelection.SetCurrentValues(self.filterParams[setName]['Genres'])
        self.filterDirectorSelection.SetCurrentValues(self.filterParams[setName]['Directors'])

    def resetFilter(self):
        self.filterYourRateSelection. SetSpinSelectorRanges([0, 10])
        self.filterYourRateSelection.SetCurrentValues([])
        self.filterIMDBRateSelection.SetSpinSelectorRanges([0, 10])
        self.filterIMDBRateSelection.SetCurrentValues([])
        self.filterRuntimeSelection.SetSpinSelectorRanges([0, 100])
        self.filterRuntimeSelection.SetCurrentValues([])
        self.filterNumVotesSelection.SetSpinSelectorRanges([0, 100000])
        self.filterNumVotesSelection.SetCurrentValues([])

        self.filterDateReleaseSelection.SetDateSelectorRanges(['1900-01-01', '2100-01-01'])
        self.filterDateReleaseSelection.SetCurrentValues([])
        self.filterDateRatedSelection.SetDateSelectorRanges(['1900-01-01', '2100-01-01'])
        self.filterDateRatedSelection.SetCurrentValues([])

        self.filterGenreSelection.SetCheckListSelectorRanges(set())
        self.filterGenreSelection.SetCurrentValues(set())
        self.filterDirectorSelection.SetCheckListSelectorRanges(set())
        self.filterDirectorSelection.SetCurrentValues(set())


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
        (NOT USED AT THE MOMENT)
        Panel for selection of element in list (dropdown).
        For example for selection of set movies, series or videogames
    """

    def __init__(self, parent, inputList, title):
        super(ListSelectionPanel, self).__init__(parent)

        self.selectedItem = 0

        # controls
        #staticTitle = wx.StaticText(self, -1, title)
        self.comboBox = wx.ComboBox(self,
                                    value='Movies',
                                    choices=inputList,
                                    style=wx.CB_DROPDOWN
                                    | wx.CB_READONLY
                                    )
        self.Disable()

        # sizers
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        #panelSizer.Add(staticTitle, 0, wx.ALIGN_CENTER)
        panelSizer.Add(self.comboBox, 0, wx.EXPAND)
        self.SetSizer(panelSizer)

        # events
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.OnListSelector)

    def OnListSelector(self, event):
        self.selectedItem = self.comboBox.GetCurrentSelection()
        event.Skip()


class buttonsSetSelection(wx.Panel):

    def __init__(self, parent):
        super(buttonsSetSelection, self).__init__(parent)

        # controls
        self.moviesButton = wx.Button(self, -1,
                                      label="movies",
                                      style=wx.BU_NOTEXT,
                                      size=wx.Size(64, 64))
        self.seriesButton = wx.Button(self, -1,
                                      label="series",
                                      style=wx.BU_NOTEXT,
                                      size=wx.Size(64, 64))
        self.videogamesButton = wx.Button(self, -1,
                                      label="videogames",
                                      style=wx.BU_NOTEXT,
                                      size=wx.Size(64, 64))
        self.Disable()

        # set images to buttons
        self.moviesButton.SetBitmap(wx.Bitmap('icons/moviesIcon.png', wx.BITMAP_TYPE_PNG))
        self.seriesButton.SetBitmap(wx.Bitmap('icons/seriesIcon.png', wx.BITMAP_TYPE_PNG))
        self.videogamesButton.SetBitmap(wx.Bitmap('icons/videogamesIcon.png', wx.BITMAP_TYPE_PNG))

        # sizers
        setSelectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        setSelectionSizer.Add(self.moviesButton, 0, wx.ALIGN_CENTER)
        setSelectionSizer.Add(20, 0)
        setSelectionSizer.Add(self.seriesButton, 0, wx.ALIGN_CENTER)
        setSelectionSizer.Add(20, 0)
        setSelectionSizer.Add(self.videogamesButton, 0, wx.ALIGN_CENTER)
        self.SetSizer(setSelectionSizer)


class MinMaxSpinCtrlPanel(wx.Panel):
    """
        Panel for selection of number using a spin control (real numbers by default).
    """

    def __init__(self, parent, minValue, maxValue, inc, width, title, isInteger=False):
        super(MinMaxSpinCtrlPanel, self).__init__(parent)

        self.selectedValueMin = minValue
        self.selectedValueMax = maxValue
        self.isActive = False

        # controls
        self.checkBox = wx.CheckBox(self, -1, title)
        staticMinText = wx.StaticText(self, -1, 'Min: ')
        staticMaxText = wx.StaticText(self, -1, 'Max: ')
        spinPanelStyle = wx.SP_ARROW_KEYS | wx.SP_VERTICAL

        if not isInteger:
            self.spinCtrlMin = self.initSpinCtrlDouble(width, spinPanelStyle, minValue,
                                                       maxValue, self.selectedValueMin, inc)
            self.spinCtrlMax = self.initSpinCtrlDouble(width, spinPanelStyle, minValue,
                                                       maxValue, self.selectedValueMax, inc)
        else:
            self.spinCtrlMin = self.initSpinCtrlInteger(width, spinPanelStyle, minValue,
                                                        maxValue, self.selectedValueMin)
            self.spinCtrlMax = self.initSpinCtrlInteger(width, spinPanelStyle, minValue,
                                                        maxValue, self.selectedValueMin)
        self.Disable()

        # sizers
        spinCtrlsSizer = wx.BoxSizer(wx.HORIZONTAL)
        spinCtrlsSizer.Add((5, 0))
        spinCtrlsSizer.Add(staticMinText, 0, wx.EXPAND)
        spinCtrlsSizer.Add(self.spinCtrlMin, 0, wx.EXPAND)
        spinCtrlsSizer.Add((5, 0))
        spinCtrlsSizer.Add(staticMaxText, 0, wx.EXPAND)
        spinCtrlsSizer.Add(self.spinCtrlMax, 0, wx.EXPAND)
        spinCtrlsSizer.Add((5, 0))
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.checkBox, 0, wx.ALIGN_LEFT)
        panelSizer.Add((0, 5))
        panelSizer.Add(spinCtrlsSizer, 0, wx.ALIGN_CENTER)
        self.SetSizer(panelSizer)

        # events
        eventName = wx.EVT_SPINCTRLDOUBLE
        if isInteger:
            eventName = wx.EVT_SPINCTRL
        self.spinCtrlMin.Bind(eventName, self.OnSpinSelectorMin)
        self.spinCtrlMax.Bind(eventName, self.OnSpinSelectorMax)
        self.checkBox.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)

    def initSpinCtrlDouble(self, width, spinPanelStyle, minValue, maxValue, initialValue, inc):
        spinCtrl = wx.SpinCtrlDouble(self, value="", size=(width, -1), style=spinPanelStyle,
                                     min=minValue, max=maxValue, initial=initialValue, inc=inc)
        spinCtrl.Disable()
        spinCtrl.SetDigits(1)
        return spinCtrl

    def initSpinCtrlInteger(self, width, spinPanelStyle, minValue, maxValue, initialValue):
        spinCtrl = wx.SpinCtrl(self, value="", size=(width, -1), style=spinPanelStyle,
                               min=minValue, max=maxValue, initial=initialValue)
        spinCtrl.Disable()
        return spinCtrl

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


class MinMaxDateCtrlPanel(wx.Panel):
    """
        Panel for selection of date interval.
    """

    def __init__(self, parent, minValue, maxValue, width, title):
        super(MinMaxDateCtrlPanel, self).__init__(parent)

        self.selectedValueMin = minValue
        self.selectedValueMax = maxValue
        self.isActive = False

        # controls
        self.checkBox = wx.CheckBox(self, -1, title)
        staticMinText = wx.StaticText(self, -1, 'From: ')
        staticMaxText = wx.StaticText(self, -1, 'To: ')
        datePanelStyle = wx.adv.DP_DROPDOWN
        initMinDate = wx.DateTime()
        initMinDate.ParseFormat(minValue, "%Y-%m-%d")
        self.dateCtrlMin = wx.adv.DatePickerCtrl(self,
                                                 dt=initMinDate,
                                                 size=(width, -1),
                                                 style=datePanelStyle
                                                 )
        self.dateCtrlMin.Disable()
        initMaxDate = wx.DateTime()
        initMaxDate.ParseFormat(maxValue, "%Y-%m-%d")
        self.dateCtrlMax = wx.adv.DatePickerCtrl(self,
                                                 dt=initMaxDate,
                                                 size=(width, -1),
                                                 style=datePanelStyle
                                                 )
        self.dateCtrlMax.Disable()
        self.Disable()

        # sizers
        dateCtrlsSizer = wx.BoxSizer(wx.HORIZONTAL)
        dateCtrlsSizer.Add((5, 0))
        dateCtrlsSizer.Add(staticMinText, 0, wx.EXPAND)
        dateCtrlsSizer.Add(self.dateCtrlMin, 0, wx.EXPAND)
        dateCtrlsSizer.Add((5, 0))
        dateCtrlsSizer.Add(staticMaxText, 0, wx.EXPAND)
        dateCtrlsSizer.Add(self.dateCtrlMax, 0, wx.EXPAND)
        dateCtrlsSizer.Add((5, 0))
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.checkBox, 0, wx.ALIGN_LEFT)
        panelSizer.Add((0, 5))
        panelSizer.Add(dateCtrlsSizer, 0, wx.ALIGN_CENTER)
        self.SetSizer(panelSizer)

        # events
        self.dateCtrlMin.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateSelectorMin)
        self.dateCtrlMax.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateSelectorMax)
        self.checkBox.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)

    def OnDateSelectorMin(self, event):
        self.selectedValueMin = self.dateCtrlMin.GetValue().Format("%Y-%m-%d")
        if self.selectedValueMin > self.selectedValueMax:
            self.selectedValueMin = self.selectedValueMax
            tempDate = wx.DateTime()
            tempDate.ParseFormat(self.selectedValueMin, "%Y-%m-%d")
            self.dateCtrlMin.SetValue(tempDate)
        event.Skip()

    def OnDateSelectorMax(self, event):
        self.selectedValueMax = self.dateCtrlMax.GetValue().Format("%Y-%m-%d")
        if self.selectedValueMax < self.selectedValueMin:
            self.selectedValueMax = self.selectedValueMin
            tempDate = wx.DateTime()
            tempDate.ParseFormat(self.selectedValueMax, "%Y-%m-%d")
            self.dateCtrlMax.SetValue(tempDate)
        event.Skip()

    def OnCheckBox(self, event):
        self.isActive = not self.isActive
        self.enableDateSelectors(self.isActive)
        if not self.isActive:
            self.SetCurrentValues([])
        event.Skip()

    def SetCurrentValues(self, values):
        if values:
            if not self.isActive:
                # it should be enabled!
                self.isActive = True
                self.checkBox.SetValue(self.isActive)
                self.enableDateSelectors(self.isActive)
            self.selectedValueMin = values[0]
            self.selectedValueMax = values[1]
        else:
            if self.isActive:
                # it should be disabled!
                self.isActive = False
                self.checkBox.SetValue(self.isActive)
                self.enableDateSelectors(self.isActive)
            self.selectedValueMin = self.dateCtrlMin.GetRange()[1].Format("%Y-%m-%d")
            self.selectedValueMax = self.dateCtrlMax.GetRange()[2].Format("%Y-%m-%d")
        tempDateMin = wx.DateTime()
        tempDateMin.ParseFormat(self.selectedValueMin, "%Y-%m-%d")
        self.dateCtrlMin.SetValue(tempDateMin)
        tempDateMax = wx.DateTime()
        tempDateMax.ParseFormat(self.selectedValueMax, "%Y-%m-%d")
        self.dateCtrlMax.SetValue(tempDateMax)

    def SetDateSelectorRanges(self, ranges):
        if ranges:
            minDate = wx.DateTime()
            minDate.ParseFormat(ranges[0], "%Y-%m-%d")
            maxDate = wx.DateTime()
            maxDate.ParseFormat(ranges[1], "%Y-%m-%d")
            self.dateCtrlMin.SetRange(minDate,
                                      maxDate)
            self.dateCtrlMax.SetRange(minDate,
                                      maxDate)

    def enableDateSelectors(self, enable):
        self.dateCtrlMin.Enable(enable)
        self.dateCtrlMax.Enable(enable)


class CheckListBoxPanel(wx.Panel):
    """
        Panel for multiple selection of items in a list
    """
    def __init__(self, parent, items_list, height, title):
        super(CheckListBoxPanel, self).__init__(parent)

        # attributes
        self.selectedSet = set()
        self.selectedMode = False
        self.currentSelection = {'values': self.selectedSet, 'mode': self.selectedMode}
        self.isActive = False
        self.checkListName = title

        # controls
        self.checkBox = wx.CheckBox(self, -1, self.checkListName)
        checkListBoxStyle = wx.LB_MULTIPLE | wx.LB_HSCROLL | wx.LB_NEEDED_SB
        self.checkListBox = wx.CheckListBox(self,
                                            size=(-1, height),
                                            choices=items_list,
                                            style=checkListBoxStyle
                                            )
        self.checkListBox.Disable()
        self.checkMode = wx.CheckBox(self, -1, "Inclusive mode", style=wx.ALIGN_RIGHT)
        self.checkMode.Disable()
        self.Disable()

        # sizers
        listBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        listBoxSizer.Add((5, 0))
        listBoxSizer.Add(self.checkListBox, 1, wx.EXPAND)
        listBoxSizer.Add((5, 0))

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.checkBox, 0, wx.ALIGN_LEFT)
        panelSizer.Add((0, 5))
        panelSizer.Add(listBoxSizer, 0, wx.EXPAND)
        panelSizer.Add(self.checkMode, 0, wx.EXPAND)
        self.SetSizer(panelSizer)

        # events
        self.checkBox.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        self.checkListBox.Bind(wx.EVT_CHECKLISTBOX, self.OnCheckListSelector)
        self.checkMode.Bind(wx.EVT_CHECKBOX, self.OnCheckMode)

    def OnCheckBox(self, event):
        self.isActive = not self.isActive
        self.enableCheckListSelector(self.isActive)
        if not self.isActive:
            self.SetCurrentValues([])
            self.updateSelectedInfo()
        event.Skip()

    def OnCheckMode(self, event):
        self.selectedMode = not self.selectedMode
        self.currentSelection['mode'] = self.selectedMode
        event.Skip()

    def OnCheckListSelector(self, event):
        selectedTuple = self.checkListBox.GetCheckedStrings()
        self.selectedSet = set([x for x in selectedTuple])
        self.currentSelection['values'] = self.selectedSet
        self.updateSelectedInfo()
        event.Skip()

    def SetCurrentValues(self, dictValuesMode):
        if dictValuesMode:
            if not self.isActive:
                # it should be enabled!
                self.isActive = True
                self.checkBox.SetValue(self.isActive)
                self.enableCheckListSelector(self.isActive)
            self.selectedSet = dictValuesMode['values'].copy()
        else:
            if self.isActive:
                # it should be disabled!
                self.isActive = False
                self.checkBox.SetValue(self.isActive)
                self.enableCheckListSelector(self.isActive)
            self.selectedSet = set()
        self.currentSelection['values'] = self.selectedSet
        unicodeValues = [x for x in self.selectedSet]
        self.checkListBox.SetCheckedStrings(unicodeValues)
        self.updateSelectedInfo()

    def SetCheckListSelectorRanges(self, ranges):
        self.checkListBox.Clear()
        if ranges:
            sortedList = list(ranges)
            sortedList.sort()
            self.checkListBox.InsertItems(sortedList, 0)
        self.updateSelectedInfo()

    def enableCheckListSelector(self, enable):
        self.checkListBox.Enable(enable)
        self.checkMode.Enable(enable)

    def updateSelectedInfo(self):
        numberCheckedItems = len(self.selectedSet)
        self.checkBox.SetLabel(self.checkListName + ' (' + str(numberCheckedItems) + '/' + str(self.checkListBox.GetCount()) + ')')
        self.checkBox.Fit()
        self.Show()
