"""
author: Haolin Li (haolinli@umich.edu)
Last modified: 2023-12-15
Description:
    This program contains the models used in the project
"""

import requests
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import json


class Artist:
    def __init__(self, name, mbid):
        self.name = name
        self.mbid = mbid
        self.related_artists = {}
        self.related_artists_filtered = {}

    def add_related_artist(self, artist_name, rel_type, song, direction='forward'):
        newRelation = {
            'rel_type': rel_type,
            'song': song,
            'direction': direction
        }
        if artist_name not in self.related_artists:
            self.related_artists[artist_name] = [newRelation]
        elif newRelation not in self.related_artists[artist_name]:
            self.related_artists[artist_name].append(newRelation)

    def get_relationship(self, list_of_artists=None):
        # get the all the related artists for this artist

        # construct the url
        headers = {
            'user-agent': 'my-app/0.0.1',
        }
        url = f'https://musicbrainz.org/ws/2/artist/{self.mbid}?inc=artist-rels&fmt=json'
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            data = request.json()
            for artist_rel in data['relations']:
                self.add_related_artist(Artist(artist_rel['artist']['name'], artist_rel['artist']['id']),
                                        artist_rel['type'], artist_rel['direction'])

                # then add the relaship to the filtered list if it is in the list of artists
                if list_of_artists is not None:
                    if artist_rel['artist']['name'] in list_of_artists:
                        self.related_artists_filtered[artist_rel['artist']['name']] = \
                            {
                                'rel_type': artist_rel['type'],
                                'direction': artist_rel['direction']
                            }

    def to_dict(self):
        return {
            'name': self.name,
            'mbid': self.mbid,
            'related_artists': self.related_artists,
            'related_artists_filtered': self.related_artists_filtered
        }

    # dunder methods
    def __str__(self):
        return f'{self.name}'


# class Song:
#     def __init__(self, name, mbid, artist, related_artists={}):
#         self.name = name
#         self.mbid = mbid
#         self.artists = artist
#         self.related_artists = related_artists
#     def __str__(self):
#         return f'{self.name}'

class ArtistGraph:
    def __init__(self, name, mbid=None, load_from_file=False, filename=None):
        if load_from_file:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.name = data['name']
                self.mbid = data['mbid']
                self.artists = []
                for artist in data['artists']:
                    # add attributes to the artist
                    new_artist = Artist(artist['name'], artist['mbid'])
                    new_artist.related_artists = artist['related_artists']
                    new_artist.related_artists_filtered = artist['related_artists_filtered']
                    self.artists.append(new_artist)

        else:
            self.name = name
            self.mbid = mbid
            self.artists = []

    def add_artist(self, artist):
        self.artists.append(artist)

    def get_artist(self, artist_name):
        for artist in self.artists:
            if artist.name == artist_name:
                return artist
        return None

    def remove_artist(self, artist):
        self.artists.remove(artist)

    def construct_graph_from_list(self, mbid):
        headers = {
            'user-agent': 'my-app/0.0.1',
        }
        url = f'https://musicbrainz.org/ws/2/series/{mbid}?inc=artist-rels&fmt=json'

        request = requests.get(url, headers=headers)

        if request.status_code == 200:
            data = request.json()
            for song in data['relations']:
                self.artists.append(Artist(song['artist']['name'], song['artist']['id']))

    def construct_relationships(self):
        for artist_in_list in self.artists:
            artist_in_list.get_relationship(self.artists)

    def to_dict(self):
        return {
            'name': self.name,
            'mbid': self.mbid,
            'artists': [artist.to_dict() for artist in self.artists]
        }

    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    # dunder methods
    def __str__(self):
        return f'{self.name}'


def construct_graph_from_song_list(mbid):
    """
    this funciton use the song list to and the artist relationship of each song to construct the graph

    :param mbid:
        the mbid of the song list, in this program, 500 Greatest Songs of All Time by Rolling Stone magazine is used
    :return:
        the graph constructed from the song list
    """
    # get the song list
    headers = {
        'user-agent': 'my-app/0.0.1',
    }
    url = f'https://musicbrainz.org/ws/2/series/{mbid}?inc=recording-rels&fmt=json'

    # get the song list from musicbrainz
    request = requests.get(url, headers=headers)

    if request.status_code == 200:
        MArtistGraph = ArtistGraph('Artist Graph for 500 Greatest Songs')
        data = request.json()

        # loop through the songs on the list
        for song in data['relations'][0:100]:  # only use the first 100 songs for now
            song_title = song['recording']['title']
            song_mbid = song['recording']['id']

            # get the detailed information of the song
            song_url = f'https://musicbrainz.org/ws/2/recording/{song_mbid}?inc=artist-credits+artist-rels&fmt=json'
            song_request = requests.get(song_url, headers=headers)

            if song_request.status_code == 200:
                song_data = song_request.json()

                # get the main artist of the song
                song_artist = song_data['artist-credit'][0]['artist']['name']
                # add the main artist to the graph if it is not already in the graph
                if song_artist not in [artist_in_graph.name for artist_in_graph in MArtistGraph.artists]:
                    MArtistGraph.add_artist(Artist(song_artist, song_data['artist-credit'][0]['artist']['id']))

                # for all the related artists of the song
                for rel_artist in song_data['relations']:
                    # add the related artist to the graph if it is not already in the graph
                    if rel_artist['artist']['name'] not in [artist_in_graph.name for artist_in_graph in
                                                            MArtistGraph.artists]:
                        MArtistGraph.add_artist(Artist(rel_artist['artist']['name'], rel_artist['artist']['id']))

                    # add the relationship to the artist
                    if rel_artist['artist']['name'] == song_artist:
                        # if the artist is the main artist of the song, continue
                        continue
                    # if this kind of relationship already exists bwteen the two artists
                    # elif rel_artist['artist']['name'] in MArtistGraph.get_artist(song_artist).related_artists:
                    #     continue
                    else:
                        # else, add new relationship
                        MArtistGraph.get_artist(song_artist).add_related_artist(rel_artist['artist']['name'],
                                                                                rel_artist['type'], song_title,
                                                                                "backward")
                        # and the reverse relationship
                        MArtistGraph.get_artist(rel_artist['artist']['name']).add_related_artist(song_artist,
                                                                                                 rel_artist['type'],
                                                                                                 song_title,
                                                                                                 "forward")

        return MArtistGraph


def convert_to_cytoscape_format(artist_graph):
    """
    this function converts the artist graph to a format that can be used by cytoscape.js

    :param artist_graph:
        the artist graph to be converted
    :return:
        the converted graph
    """
    cytoscape_graph = {
        'nodes': [],
        'edges': []
    }
    added_egdes = set()

    for artist in artist_graph.artists:
        cytoscape_graph['nodes'].append({
            'data': {
                'id': artist.name,
                'label': artist.name
            }
        })
        for related_artist, relaitonships in artist.related_artists.items():
            for relaitonship in relaitonships:
                # newEdge = {
                #     'source': artist.name if relaitonship['direction'] == 'forward' else related_artist,
                #     'target': related_artist if relaitonship['direction'] == 'forward' else artist.name,
                #     'label': relaitonship['rel_type'] + '(' + relaitonship['song'] + ')'
                # }
                edge_id = tuple(sorted([artist.name, related_artist, relaitonship['rel_type']]))
                if edge_id not in added_egdes:
                    added_egdes.add(edge_id)
                    newEdge = {
                        'id': f"{edge_id[0]}-{edge_id[1]}-{edge_id[2]}",
                        'source': artist.name,
                        'target': related_artist,
                        'label': relaitonship['rel_type'] + '(' + relaitonship['song'] + ')'
                    }
                    cytoscape_graph['edges'].append({
                        'data': newEdge
                    })

    return cytoscape_graph


# debug
if __name__ == '__main__':
    # legacy code: using the artist list to create the graph ##################################################
    # get artist list from musicbrainz
    # ArrestedForDrugs = ArtistGraph('ArrestedForDrugs', '7ce0df17-ff61-4c5f-a1ac-43b645d51729')
    # Billboard200 = ArtistGraph('Billboard200', 'cd4b51c5-116b-49d5-8622-8047c34067b2')
    # HollywoodWalkOfFame = ArtistGraph('HollywoodWalkOfFame', '20a6efaf-3580-4948-b8e3-cad42fcf5cc7')

    # get the related artists for each artist in the list
    # ArrestedForDrugs.construct_relationships()
    # Billboard200.construct_relationships()
    # HollywoodWalkOfFame.construct_relationships()

    # try constructing the graph from the song list
    # MyArtistGraph = construct_graph_from_song_list('355b26c9-001e-4728-852e-82b4379adb82')

    # cache the data to a json file
    # MyArtistGraph.save_to_json('graph.json')

    # load the data from the json file to prevent making too many requests to the musicbrainz api
    MyArtistGraph = ArtistGraph('Artist Graph for 500 Greatest Songs', load_from_file=True, filename='graph.json')

    # convert the graph to a format that can be used by cytoscape.js
    graph_json = convert_to_cytoscape_format(MyArtistGraph)

    # load the data from the json file to prevent making too many requests to the musicbrainz api
    # MyArtistGraph = ArtistGraph('Artist Graph for 500 Greatest Songs', load_from_file=True, filename='graph.json')

    pass
