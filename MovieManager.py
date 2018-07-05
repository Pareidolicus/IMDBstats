from __future__ import division
import csv
from copy import deepcopy

class MovieManagerClass(object):
    def __init__(self):
        self.meta = []
        self.allTitles = {'movies': [], 'series': [], 'videogames': []}
        self.filterParams = {}

    def clearProps(self):
        self.meta = []
        self.allTitles = {'movies': [], 'series': [], 'videogames': []}
        self.filterParams = {}

    def Latin1ToUnicodeDictReader(self, latin1_data, **kwargs):
        csv_reader = csv.DictReader(latin1_data, **kwargs)
        self.meta = csv_reader.fieldnames
        for row in csv_reader:
            yield {key: value.decode('latin-1').encode('utf8') if value else value for key, value in row.iteritems()}

    def readFile(self, csvFile):
        with open(csvFile, 'rb') as inFile:
            reader = self.Latin1ToUnicodeDictReader(inFile, delimiter=',')
            typesMoviesSet = {'video', 'movie', 'tvMovie'}
            typesSeriesSet = {'tvSeries', 'tvEpisode'}
            typesVideogamesSet = {'videoGame'}

            self.meta.append('Active')
            self.filterParams = {'movies': {self.meta[i]: [] for i in range(len(self.meta))},
                                 'series': {self.meta[i]: [] for i in range(len(self.meta))},
                                 'videogames': {self.meta[i]: [] for i in range(len(self.meta))}}
            for title in reader:
                title.update({'Active': True})
                title['Genres'] = set(title['Genres'].split(', '))
                title['Directors'] = set(title['Directors'].split(', '))
                if '' in title['Directors']:
                    title['Directors'] = set()
                if not title['IMDb Rating']:
                    title['IMDb Rating'] = None
                else:
                    title['IMDb Rating'] = float(title['IMDb Rating'])
                title['Your Rating'] = float(title['Your Rating'])
                title['Num Votes'] = int(title['Num Votes'])
                if not title['Runtime (mins)']:
                    title['Runtime (mins)'] = None
                else:
                    title['Runtime (mins)'] = int(title['Runtime (mins)'])

                if title['Title Type'] in typesMoviesSet:
                    self.allTitles['movies'].append(title)
                elif title['Title Type'] in typesSeriesSet:
                    self.allTitles['series'].append(title)
                elif title['Title Type'] in typesVideogamesSet:
                    self.allTitles['videogames'].append(title)

    def clearFilter(self, setName):
        """
        Deactivates all the parameters in filter for set 'setName'

        :param setName: name of set
        :return:
        """
        for f in self.meta:
            self.switchFilterParam(setName, f, False)

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

    def switchFilterParam(self, setName, field, activate):
        """
        This function activates or deactivates a parameter in search filter,
        for set setName and field. None values are not considered in search
        if field is activated (only shown if deactivated). If all values of a field
        are None, the field cannot be activated.

        :param setName: set of titles: movies, series or videogames
        :param field: field of parameter (title, year, rating...)
        :param activate: True if we want to activate field in search
        :return: True if activation/deactivation has been done successfully
        """

        if not activate:
            self.filterParams[setName][field] = []
            return True
        if field in {'Your Rating', 'IMDb Rating'}:
            self.filterParams[setName][field] += [0, 10]
            return True
        elif field in {'Date Rated', 'Release Date', 'Runtime (mins)', 'Num Votes'}:
            tempList = [x[field] for x in self.allTitles[setName]]
            # check if all values in field are None
            if tempList.count(None) is not len(tempList):
                self.filterParams[setName][field] += [self.minValueForField(setName, field),
                                                      self.maxValueForField(setName, field)]
                return True
            else:
                # if all values are non, field can't be activated
                self.filterParams[setName][field] = []
                return False
        elif field in {'Genres', 'Directors', 'Title Type'}:
            self.filterParams[setName][field] = set()
            for title in self.allTitles[setName]:
                self.filterParams[setName][field] |= title[field]
            return True

    def minValueForField(self, setName, field):
        return min(x[field] for x in self.allTitles[setName] if x is not None)

    def maxValueForField(self, setName, field):
        return max(x[field] for x in self.allTitles[setName])


if __name__ == '__main__':
    myMovies = MovieManagerClass()
    myMovies.readFile('ratings.csv')
    print(myMovies.meta)
    #print(myMovies.allTitles['movies'][0]['Release Date'])
