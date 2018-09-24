from __future__ import division
import csv
from copy import deepcopy


class MovieManagerClass(object):
    def __init__(self):
        self.meta = []
        self.allTitles = {'movies': [], 'series': [], 'videogames': []}
        self.filterParams = {}
        self.filterRanges = {}

    def clearProps(self):
        self.meta = []
        self.allTitles = {'movies': [], 'series': [], 'videogames': []}
        self.filterParams = {}
        self.filterRanges = {}

    def Latin1ToUnicodeDictReader(self, csv_reader):
        for row in csv_reader:
            yield {key: row[key].decode('latin-1').encode('utf8') if row[key] else row[key] for key in row}

    def readFile(self, csvFile):

        try:
            with open(csvFile, 'rb') as inFile:
                csv_reader = csv.DictReader(inFile, delimiter=',')
                self.meta = csv_reader.fieldnames
                self.meta.append('Active')
                typesMoviesSet = {'video', 'movie', 'tvMovie'}
                typesSeriesSet = {'tvSeries', 'tvEpisode'}
                typesVideogamesSet = {'videoGame'}
                self.filterParams = {'movies': {self.meta[i]: [] for i in range(len(self.meta))},
                                     'series': {self.meta[i]: [] for i in range(len(self.meta))},
                                     'videogames': {self.meta[i]: [] for i in range(len(self.meta))}}

                reader = self.Latin1ToUnicodeDictReader(csv_reader)
                for title in reader:
                    title.update({'Active': True})
                    # change to sets of words
                    title['Genres'] = set(title['Genres'].split(', '))
                    title['Directors'] = set(title['Directors'].split(', '))
                    if '' in title['Directors']:
                        title['Directors'] = set()

                    # change to floats
                    if not title['IMDb Rating']:
                        title['IMDb Rating'] = None
                    else:
                        title['IMDb Rating'] = float(title['IMDb Rating'])
                    title['Your Rating'] = float(title['Your Rating'])

                    # change to integers
                    title['Num Votes'] = int(title['Num Votes'])
                    if not title['Runtime (mins)']:
                        title['Runtime (mins)'] = None
                    else:
                        title['Runtime (mins)'] = int(title['Runtime (mins)'])

                    # Classify in set according to title type
                    if title['Title Type'] in typesMoviesSet:
                        title['Title Type'] = set(title['Title Type'].split(', '))
                        self.allTitles['movies'].append(title)
                    elif title['Title Type'] in typesSeriesSet:
                        title['Title Type'] = set(title['Title Type'].split(', '))
                        self.allTitles['series'].append(title)
                    elif title['Title Type'] in typesVideogamesSet:
                        title['Title Type'] = set(title['Title Type'].split(', '))
                        self.allTitles['videogames'].append(title)

            self.filterRanges = {'movies': {self.meta[i]: [] for i in range(len(self.meta))},
                                 'series': {self.meta[i]: [] for i in range(len(self.meta))},
                                 'videogames': {self.meta[i]: [] for i in range(len(self.meta))}}
            self.initFilterRanges('movies')
            self.initFilterRanges('series')
            self.initFilterRanges('videogames')
            inFile.close()
        except IOError:
            return False
        return True

    def clearFilter(self, setName):
        """
        Deactivates all the parameters in filter for set 'setName'

        :param setName: name of set
        :return:
        """
        for f in self.meta:
            self.switchFilterParam(setName, f, [], False)
        for title in self.allTitles[setName]:
            title['Active'] = True

    def applyFilter(self, setName):
        """
        Activate (or deactivate) titles in set 'setName' if they satisfy
        (or not) parameters in search filter.

        :param setName: Name of set (movies, series or videogames)
        :return:
        """

        for title in self.allTitles[setName]:
            act = True
            for field in self.meta:
                if not self.filterParams[setName][field]:
                    continue
                if field in {'Genres', 'Directors', 'Title Type'}:
                    if not title[field] & self.filterParams[setName][field]:
                        act = False
                        break
                else:
                    interval = self.filterParams[setName][field]
                    act = (interval[0] <= title[field]) and (title[field] <= interval[1])
                if not act:
                    break
            title['Active'] = act

    def getActiveTitles(self, setName):
        output = []
        for title in self.allTitles[setName]:
            outTitle = deepcopy(title)
            if title['Active']:
                for field in ['Genres', 'Directors', 'Title Type']:
                    outTitle[field] = ''
                    for ind, word in enumerate(title[field]):
                        if ind == 0:
                            outTitle[field] += word
                        else:
                            outTitle[field] += ', ' + word
                output.append(outTitle)
        return output

    def initFilterRanges(self, setName):
        """
         Initialize min and max possible values for some filter parameters.

        :param setName: name of set (series, movies or videogames)
        :return:
        """

        for field in {'Your Rating', 'IMDb Rating'}:
            self.filterRanges[setName][field] = [0, 10]
        for field in {'Date Rated', 'Release Date', 'Runtime (mins)', 'Num Votes'}:
            tempList = [x[field] for x in self.allTitles[setName]]
            # check if all values in field are None
            if tempList.count(None) is not len(tempList):
                self.filterRanges[setName][field] = [self.minValueForField(setName, field),
                                                     self.maxValueForField(setName, field)]
            else:
                self.filterRanges[setName][field] = []
        for field in {'Genres', 'Directors', 'Title Type'}:
            self.filterRanges[setName][field] = set()
            for title in self.allTitles[setName]:
                self.filterRanges[setName][field] |= title[field]

    def switchFilterParam(self, setName, field, values, activate):
        """
        This function activates or deactivates a parameter in search filter,
        for set setName and field. None values are not considered in search
        if field is activated (only shown if deactivated). If all values of a field
        are None, the field cannot be activated.

        :param setName: set of titles: movies, series or videogames
        :param field: field of parameter (title, year, rating...)
        :param values: value set in field when it is activated. It can be empty if activated is False.
        :param activate: True if we want to activate field in search
        :return: True if activation/deactivation has been done successfully
        """
        # If field is not active, filter param is set to empty list
        if not activate:
            self.filterParams[setName][field] = []
            return True

        # If field is active and no values are provided, return false.
        if not values:
            print(field + ' field in ' + setName + ' set cant be activated because values are empty.')
            self.filterParams[setName][field] = []
            return False

        # videogames has no runtime, so this field cant be activated for this set
        if (field == 'Runtime (mins)') and (setName == 'videogames'):
            self.filterParams[setName][field] = []
            print(field + ' field in ' + setName + ' set cant be activated because videogames has no Runtime.')
            return False

        # Set values to filter parameter
        self.filterParams[setName][field] = values
        return True

    def setFilterParams(self, setName, filterPanelParams):
        for field in filterPanelParams:
            activate = True
            if not filterPanelParams[field]:
                activate = False
            self.switchFilterParam(setName, field, filterPanelParams[field], activate)

    def minValueForField(self, setName, field):
        return min(x[field] for x in self.allTitles[setName] if x is not None)

    def maxValueForField(self, setName, field):
        return max(x[field] for x in self.allTitles[setName])


if __name__ == '__main__':
    myMovies = MovieManagerClass()
    myMovies.readFile('ratings.csv')
    print(myMovies.meta)
