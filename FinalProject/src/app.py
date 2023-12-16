"""
author: Haolin Li (haolinli@umich.edu)
Last modified: 2023-12-15
Description:
    This file is the main file for the web app.
"""

from flask import Flask, jsonify, render_template
from models import *

app = Flask(__name__)


@app.route('/')
def graph():
    return render_template('main.html')


@app.route('/graph-data')
def graph_data():
    MyArtistGraph = ArtistGraph('Artist Graph for 500 Greatest Songs', load_from_file=True, filename='graph.json')
    graph_json = convert_to_cytoscape_format(MyArtistGraph)
    return jsonify(graph_json)


if __name__ == '__main__':
    # MyArtistGraph = ArtistGraph('Artist Graph for 500 Greatest Songs', load_from_file=True, filename='graph.json')
    app.run()
