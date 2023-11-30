class Artist:
    """ Class to represent an artist. """
    def __init__(self, alias, primary_alias, area, arid, artist, artistaccent, begin, beginarea,
                 comment, country, end, endarea, ended, gender, ipi, isni, sortname, tag, artType):
        self.alias = alias
        self.primary_alias = primary_alias
        self.area = area
        self.arid = arid
        self.artist = artist
        self.artistaccent = artistaccent
        self.begin = begin
        self.beginarea = beginarea
        self.comment = comment
        self.country = country
        self.end = end
        self.endarea = endarea
        self.ended = ended
        self.gender = gender
        self.ipi = ipi
        self.isni = isni
        self.sortname = sortname
        self.tag = tag
        self.type = artType
        self.connections = set()

    def add_connection(self, other_artist):
        """ Add a connection to another artist. """
        self.connections.add(other_artist)

    def remove_connection(self, other_artist):
        """ Remove a connection to another artist. """
        if other_artist in self.connections:
            self.connections.remove(other_artist)

    def list_connections(self):
        """ List all connections. """
        return self.connections

    def display_info(self):
        """ Display information about the artist. """
        info = f"Artist: {self.artist}\nType: {self.type}\nCountry: {self.country}\n"
        info += f"Begin: {self.begin}, End: {self.end}\nGender: {self.gender}\n"
        info += f"Connections: {[artist.artist for artist in self.connections]}\n"
        return info
