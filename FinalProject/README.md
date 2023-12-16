# SI507 Final Project: Artists Network

> Author: Haolin Li
>
> Email: haolinli@umich.edu
>
> Last Updated: 12/15/2023
>
> Github Repository: https://github.com/HumblePasty/SI507



This program is created to construct and visualize a relationship graph between artists through a list of songs or a list of artists based on fetched data from [MusicBrainz](https://musicbrainz.org/).



## Dependencies

**Libaries:**

- `Flask` - web framework for python
- `requests` - request library to fetch data from [**MusicBrainz API**](https://musicbrainz.org/doc/MusicBrainz_API)
- `Cytoscape` - for creating interactive graph

**Compatibility**

- python 3.9 (Anaconda)



## Data Source

All the data used for this project is fetched by [**MusicBrainz API**](https://musicbrainz.org/doc/MusicBrainz_API) ***(no key or token needed!)***

**Key Sources**:

- [The Rolling Stone Magazine’s 500 Greatest Songs of All Time: 2021 edition](https://musicbrainz.org/series/355b26c9-001e-4728-852e-82b4379adb82)
- A list of artists [Arrested for Drugs](https://musicbrainz.org/series/7ce0df17-ff61-4c5f-a1ac-43b645d51729)

Read more about how data is fetched from these source [HERE](https://github.com/HumblePasty/SI507/blob/master/FinalProject/Resources/Project_Submission_haolinli.md#fetching-method)



## Data Structure

Read data structure doc explaining fields and meanings [HERE](https://github.com/HumblePasty/SI507/blob/master/FinalProject/Resources/Project_Submission_haolinli.md#data-structure)

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



## How to Run

*Note: no key or token is needed for MusicBrainz API*

- Step 1: Clone the repository and go to the code directory

  ```
  git clone https://github.com/HumblePasty/SI507.git
  cd FinalProject
  cd src
  ```

- Step 2: Install flask, if haven’t already

  ```
  pip install flask
  ```

- Step 3: Run app.py

  ```
  python app.py
  ```

- Step 4: Open the link in browser

  ```
  http://127.0.0.1:5000/
  ```

  *Note: the specific port may vary. If you can not open the link, please follow the generated prompt instead*

- Step 5: Explore and Enjoy!



## Demo

**Click [here](https://drive.google.com/file/d/1ruVh3IF97ZobWIkNWTcBENRD0Ld8ZzPk/view?usp=sharing) or the image to redirect**

[<img src="https://rsdonkeyrepo1.oss-cn-hangzhou.aliyuncs.com/img/thumbnail.jpg">](https://drive.google.com/file/d/1ruVh3IF97ZobWIkNWTcBENRD0Ld8ZzPk/view?usp=sharing "Demo Video")



For more information, Click [HERE](https://github.com/HumblePasty/SI507/blob/master/FinalProject/Resources/Project_Submission_haolinli.md)