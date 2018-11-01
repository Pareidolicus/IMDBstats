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

        tempParams = {self.meta[i]: [] for i in range(len(self.meta))}
        self.setFilterParams(setName, tempParams)
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
                    values = self.filterParams[setName][field]['values']
                    isInclusive = self.filterParams[setName][field]['mode']
                    cond1 = (not isInclusive) or values <= title[field]
                    cond2 = isInclusive or values & title[field]
                    act = cond1 and cond2
                else:
                    interval = self.filterParams[setName][field]
                    act = (interval[0] <= title[field]) and (title[field] <= interval[1])
                if not act:
                    break
            title['Active'] = act

    def getActiveTitlesID(self, setName):
        """
            Return the list of ID's ('const' field) for actives titles and set 'setName'
        :param setName: name of set
        :return: list of 'Const' strings
        """
        return [title['Const'] for title in self.allTitles[setName] if title['Active']]

    def getTitlesByID(self, setName, IDlist):
        """
            Given a list of of ID's ('Const' field), return the list of titles
            with all the fields (dictionary).
        :param setName: Name of set
        :param IDlist: List of 'Const' values
        :return: List of dictionary of titles
        """
        output = []
        for title in self.allTitles[setName]:
            if title['Const'] not in IDlist:
                continue

            outTitle = deepcopy(title)
            for field in ['Genres', 'Directors', 'Title Type']:
                outTitle[field] = ''
                for ind, word in enumerate(title[field]):
                    if ind == 0:
                        outTitle[field] += word
                    else:
                        outTitle[field] += ', ' + word
            output.append(outTitle)
        return output

    def searchTitlesByName(self, setName, IDList, searchTerm):
        """
            Given a list of ID's ('Const'), search 'searchTerm' in
            name of titles, and return a list of ID.
        :param setName: Name of set.
        :param IDList: List of 'Const' values of titles we want to do the searching
        :param searchTerm: string to search in name of given titles
        :return: List of ID of titles with coincidences in name
        """
        outList = []
        for title in self.allTitles[setName]:
            if title['Const'] not in IDList:
                continue
            name = title['Title']
            if searchTerm.lower() in name.decode('utf8').lower():
                outList.append(title['Const'])
        return outList

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

    def setFilterParams(self, setName, filterPanelParams):
        for field in filterPanelParams:

            if (field in {'Genres', 'Directors', 'Title Type'}) and ('values' in filterPanelParams[field]):
                values = filterPanelParams[field]['values']
            else:
                values = filterPanelParams[field]

            if not values:
                self.filterParams[setName][field] = []
                continue

            if (field == 'Runtime (mins)') and (setName == 'videogames'):
                # videogames has no runtime, so this field cant be activated for this set
                self.filterParams[setName][field] = []
                print(field + ' field in ' + setName + ' set cant be activated because videogames has no Runtime.')
                continue

            # Set values to filter parameter
            self.filterParams[setName][field] = filterPanelParams[field]

    def minValueForField(self, setName, field):
        return min(x[field] for x in self.allTitles[setName] if x is not None)

    def maxValueForField(self, setName, field):
        return max(x[field] for x in self.allTitles[setName])


if __name__ == '__main__':
    myMovies = MovieManagerClass()
    myMovies.readFile('ratings.csv')
    print(myMovies.meta)
