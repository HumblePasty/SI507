# Final Project Submission - SI507

> Author: Haolin Li
>
> Email: haolinli@umich.edu
>
> Last Updated: 12/14/2023
>



## Project Code Repository

Course Github Repository: https://github.com/HumblePasty/SI507

- **See project folder**: https://github.com/HumblePasty/SI507/tree/master/FinalProject



## Data Sources

### Description:

- **[MusicBrainz](https://musicbrainz.org/)** is an open music encyclopedia that collects music metadata and makes it available to the public. It is similar to the freedb project, but with richer data and a more advanced underlying structure that allows for better data retrieval and understanding.
- [**Documentation**](https://musicbrainz.org/doc/MusicBrainz_Documentation)

**Key Sources**:

- [The Rolling Stone Magazine’s 500 Greatest Songs of All Time: 2021 edition](https://musicbrainz.org/series/355b26c9-001e-4728-852e-82b4379adb82)
- A list of artists [Arrested for Drugs](https://musicbrainz.org/series/7ce0df17-ff61-4c5f-a1ac-43b645d51729)



### Data Format:

The expect data fetching method for this project is through [the provided API](https://musicbrainz.org/doc/MusicBrainz_API) by MusicBrainz.

The API's architecture follows the REST design principles. Interaction with the API is done using HTTP and all content is served in a simple but flexible format, in either **XML or JSON**. 



### Fetching Method

Library `requests` is used to get data from API. The general steps for fetching data from api are:

- Step 1: construct header

  ```python
  headers = {
              'user-agent': 'my-app/0.0.1',
          }
  ```

- Step 2: determine the url

  ```
  url = f'https://[BASE_URL]/[DATA_TYPE]?[PARAMETER]=[VALUE]&...
  ```

- Step 3: make requests

  ```python
  request = requests.get(url, headers=headers)
  if request.status_code == 200:
      data = request.json()
      # process the data
  ```



**Url of key requests used in this project:**

1. Get a list of songs from the [The Rolling Stone Magazine’s 500 Greatest Songs of All Time: 2021 edition](https://musicbrainz.org/series/355b26c9-001e-4728-852e-82b4379adb82)

   ```
   https://musicbrainz.org/ws/2/series/355b26c9-001e-4728-852e-82b4379adb82?inc=recording-rels&fmt=json
   ```

2. Get a list of artists from [Arrested for Drugs](https://musicbrainz.org/series/7ce0df17-ff61-4c5f-a1ac-43b645d51729)

   ```
   https://musicbrainz.org/ws/2/series/7ce0df17-ff61-4c5f-a1ac-43b645d51729?inc=artist-rels&fmt=json
   ```

3. Get all the related artist of a specific song

   ```
   https://musicbrainz.org/ws/2/recording/{song_mbid}?inc=artist-credits+artist-rels&fmt=json
   ```

4. Get all the related artists of a specific artist

   ```
   https://musicbrainz.org/ws/2/artist/{song_mbid}?inc=artist-rels&fmt=json
   ```



*Notes*

- *Records are cached in **graph.json***
- *See examples of output at https://musicbrainz.org/doc/MusicBrainz_API/Examples*



## Data Structure

**Artists Network (Graph)**

In this project, the highest data structure level is the network of artists. This is represented as a graph where each node represents an artist and each edge represents a relationship between two artists.

The attributes of the Artists Network are:

- **name**: `string`

  The name of the network. Usually represents a specific theme. For example, artists arrested for drugs, artists on the Billboard 200 list etc.

- **mbid**: `string`

  The MusicBrainz ID of the list of artists or the list of other types of entities from which the artists network can be constructed. This attribute is the fundamental source of data.

  Read more about [MusicBrainz ID](https://musicbrainz.org/doc/MusicBrainz_Identifier), [MusicBrainz Entities](https://musicbrainz.org/doc/MusicBrainz_Entity), [Series](https://musicbrainz.org/doc/Series) and [Relationships](https://musicbrainz.org/relationships)

- **artists**: `list`

  The list of artists in the network. Represented as nodes.



**Artists (Node)**

The attributes of the Artists are:

- **name**: `string`

  The name of the artist.

- **mbid**: `string`

  The MusicBrainz ID of the artist. This attribute provides information to make API requests to get more detailed data about this artist.

  Read more about [MusicBrainz ID](https://musicbrainz.org/doc/MusicBrainz_Identifier), [MusicBrainz Entities](https://musicbrainz.org/doc/MusicBrainz_Entity), [Series](https://musicbrainz.org/doc/Series) and [Relationships](https://musicbrainz.org/relationships)

- **related_artists**: `dict`

  The list of artists in the network. Represented as nodes.

- **degree_centrality**: `numeric`

  The degree centrality of the node. This attributed is not represented in the data. But was calculated through Cytoscape library.



**Relationships (Edge)**

The attributes of the Artists are:

- **rel_type**: `string`

  The type of relationship between artists. 

- **song**: `string`

  The name of the song by which the two artists are related. This field is specifically design for a artists network constructed from a song list.

- **direction**: `string`

  `backward` or `forward`

  The direction of the relationship. For example, if artist A play the keyboard for artist B in a specific song, then this field would be `forward` for artist A and `backward` for artist B



**Data Example**

*Note: see complete file in graph.json*

```json
{
    "name": "Artist Graph for 500 Greatest Songs",
    "mbid": null,
    "artists": [
        {
            "name": "Britney Spears",
            "mbid": "45a663b5-b1cb-4a91-bff6-2bef7bbfdd76",
            "related_artists": {
                "Johan Carlberg": [
                    {
                        "rel_type": "instrument",
                        "song": "\u2026Baby One More Time",
                        "direction": "backward"
                    },
                    ...
                ],
                ...
        },
        ...
    ]
}
```



Rubric Requirement:

- A python file that constructs your graphs or trees from your stored data using classes (or some other method)

  ```
  models.py
  ```

- JSON file with your graphs or trees

  ```
  graph.json
  ```

- A stand alone python file that reads the json of your graphs or trees.

  ```python
  # read_network_from_file.py (not actually used)
  
  from models import *
  
  MyArtistGraph = ArtistGraph('Artist Graph for 500 Greatest Songs', load_from_file=True, filename='graph.json')
  ```



## Interaction and Presentation Options

![1702718769990](https://rsdonkeyrepo1.oss-cn-hangzhou.aliyuncs.com/img/1702718769990.png)

1. Dropdown menu, allows for different layouts of the network;
2. Zoom button, fit the extent to all the existing nodes and edges;
3. Reset button, reset the whole web page to the original status;
4. Search box, allows for searching artists by name and display the search result only;
5. Statistics box, presents the status of the network. The last attribute will be updated if a specific node is selected.
6. Main panel



## Demo

**Click [here](https://drive.google.com/file/d/1ruVh3IF97ZobWIkNWTcBENRD0Ld8ZzPk/view?usp=sharing) or the image to redirect**

[<img src="https://rsdonkeyrepo1.oss-cn-hangzhou.aliyuncs.com/img/thumbnail.jpg">](https://drive.google.com/file/d/1ruVh3IF97ZobWIkNWTcBENRD0Ld8ZzPk/view?usp=sharing "Demo Video")