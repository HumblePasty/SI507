#########################################
##### Name: Haolin Li               #####
##### Uniqname: haolinli            #####
#########################################


import json
import json as js
import urllib.parse
from datetime import datetime
import requests
import urllib.parse
import webbrowser


class Media:
    """
    Media class
    ----------
    Instance Attributes:
        title: string
        author: string
        release_year: string
        url: string
    """

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):
        if json is not None:
            # if json is not none, create from json
            # parse the json
            if isinstance(json, dict):
                json = js.dumps(json)
            json_str = js.loads(json)
            self.author = json_str["artistName"]
            self.release_year = str(datetime.fromisoformat(json_str["releaseDate"][:-1]).year)
            if "kind" in json_str:
                self.title = json_str["trackName"]
                self.url = json_str["trackViewUrl"]
                if json_str["kind"] == "feature-movie":
                    # movie type
                    self.rating = json_str["contentAdvisoryRating"]
                    self.movie_length = json_str["trackTimeMillis"]
                elif json_str["kind"] == "song":
                    # song type
                    self.album = json_str["collectionName"]
                    self.genre = json_str["primaryGenreName"]
                    self.track_length = json_str["trackTimeMillis"]
                    # Construct a song instance
            else:
                # other type
                self.title = json_str["collectionName"]
                self.url = json_str["collectionViewUrl"]
        else:
            # else, create with explicit parameters
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url

    # Methods
    def info(self):
        """
        The method that return the infomation of the media

        Returns
        -------
        string
            <title> by <author> (<release year>)

        """
        # question: what to return if the infomation is unknown?
        returnStr = str(self.title) + " by " + str(self.author) + " (" + str(self.release_year) + ")"

        return returnStr

    def length(self):
        """
        returns the length of the media, in this class returns zero

        Returns
        -------
        int
            length of the media, 0 for Media class

        """
        return 0

    def __str__(self):
        attributes = vars(self)
        output = [f"{name.capitalize()}: {attributes[name]}" for name in sorted(attributes.keys())]
        return "\n".join(output)


# Other classes, functions, etc. should go here

class Song(Media):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL",
                 album="No Album", genre="No Genre", track_length=0, json=None):
        if json is not None:
            super().__init__(json=json)
        else:
            super().__init__(title, author, release_year, url, json=None)
            self.album = album
            self.genre = genre
            self.track_length = track_length

    def info(self):
        """
        Return the infomation of the song

        Returns
        -------
        str
            <title> by <author> (<release year>) [<genre>]

        """
        returnStr = super().info() + " [" + str(self.genre) + "]"

        return returnStr

    def length(self):
        """
        return the length of the song in seconds, rounded to nearest second

        Returns
        -------

        """
        return round(self.track_length / 1000)


class Movie(Media):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL",
                 rating="No Rating", movie_length=0, json=None):
        if json is not None:
            super().__init__(json=json)
        else:
            super().__init__(title, author, release_year, url, json=None)
            self.rating = rating
            self.movie_length = movie_length

    def info(self):
        return super().info() + ' [' + str(self.rating) + ']'

    def length(self):
        """
        return the movie length in nearest rounded minute

        Returns
        -------

        """
        return round(self.movie_length / 60000)


class Search:
    def __init__(self, term, country='US', limit=50):
        self.term = term
        self.country = country
        self.limit = limit
        self.results = {
            "Movies": [],
            "Songs": [],
            "Others": []
        }

    def __str__(self):
        output = []
        flag = 1

        for key, mediatype in self.results.items():
            output.append(f"{key}:")

            for items in mediatype:
                output.append(f"    - {flag}: {items.info()}")
                flag += 1
            output.append("")

        return "\n".join(output)

    def __getitem__(self, index):
        # make search class subscriptable
        total_processed = 0
        for key in self.results:
            if index < total_processed + len(self.results[key]):
                return self.results[key][index - total_processed]
            total_processed += len(self.results[key])
        raise IndexError("Index out of range")

    def __len__(self):
        total_length = 0
        for key in self.results:
            total_length += len(self.results[key])
        return total_length

    def requestResults(self):
        # request the result using the iTunes API
        result_str = requests.get(
            f"https://itunes.apple.com/search?term={urllib.parse.quote(self.term)}&country={self.country}&limit={str(self.limit)}").text
        # parsing the response text
        result_dict = json.loads(result_str)
        # creating the objects
        for item in result_dict["results"]:
            if "kind" in item:
                if item["kind"] == "feature-movie":
                    m = Movie(json=json.dumps(item))
                    self.results["Movies"].append(m)
                elif item["kind"] == "song":
                    m = Song(json=json.dumps(item))
                    self.results["Songs"].append(m)
            else:
                m = Media(json=json.dumps(item))
                self.results["Others"].append(m)


if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here

    while True:
        searchTerm = input("Enter a search term, or \"exit\" to quit: ")
        if searchTerm == "exit":
            quit()
        # searchCountry = input("Enter country of searching (default US): ")
        # if searchCountry == '':
        #     searchCountry = "US"
        # searchLimit = input("Enter number limit (default 50): ")
        # if searchLimit == '':
        #     searchLimit = 50

        # construct a search object
        mySearch = Search(term=searchTerm, limit=50, country="US")
        # conduct search
        try:
            mySearch.requestResults()
        except:
            print("Error occurred while searching, check internet connection.")
            continue
        # print(mySearch)
        print("--------------------Search Result--------------------")
        print(mySearch)

        # detail activities conversations
        while True:
            detailsIndex = input("Enter a number for detailed info, \"back\" for another search, or \"exit\" to quit: ")
            if detailsIndex == "exit":
                quit()
            elif detailsIndex == 'back':
                break
            else:
                try:
                    numberIndex = int(detailsIndex) - 1
                    if 0 <= numberIndex <= len(mySearch) - 1:
                        # if a valid number is input, then log the detailed infomation of the item and provide
                        # further conversation
                        print(mySearch[numberIndex])
                        while True:
                            keyConfirm = input("Do you want to open the page? (y/N or \"exit\" to quit): ")
                            if keyConfirm == 'y' or keyConfirm == 'Y':
                                print("Opening the page...")
                                webbrowser.open(mySearch[numberIndex].url)
                                break
                            elif keyConfirm == 'n' or keyConfirm == 'N':
                                print("Back to indexing...")
                                break
                            elif keyConfirm == 'exit':
                                quit()
                            else:
                                print("Input not valid, please try again")
                    else:
                        print("Input number out of range")
                except ValueError:
                    print("Input not valid, please try again")
