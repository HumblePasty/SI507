"""
Name: Haolin Li
Date: 10/12/2021
Email: haolinli@umich.edu
Description: This is a python script that will be used to
                analyze the redlining data for Detroit.
"""


# Step 1: Using the python methods we used in class obtain the json file
import requests
import json

# Step 1: Fetch the JSON data
url = "https://dsl.richmond.edu/panorama/redlining/static/downloads/geojson/MIDetroit1939.geojson"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Step 2: Deserialize the JSON data into a Python object
    RedliningData = response.json()
else:
    print(f"Failed to retrieve the data. HTTP Status Code: {response.status_code}")

# parse the response into a python object
DetroitDistricts = json.loads(response.text)


# Step 2: Develop a mental map of the data structure of the redlining data.
# Step 2.1: Defining Detroit District class
class DetroitDistrict:
    def __init__(self, data):
        self.Coordinates = self.extract_coordinates(data)
        self.HolcGrade = data['properties']['holc_grade']
        self.HolcColor = self.grade_to_color(self.HolcGrade)
        self.name = self.extract_name(data)  # Here we can define our extraction method
        self.QualitativeDescription = self.extract_section_8(data)
        self.RandomLat = None
        self.RandomLong = None
        self.MedianIncome = None
        self.CensusTract = None

    def extract_coordinates(self, data):
        # Extracting coordinates considering the fact that some districts can be non-contiguous
        return data['geometry']['coordinates']

    def grade_to_color(self, grade):
        color_map = {
            'A': 'darkgreen',
            'B': 'cornflowerblue',
            'C': 'gold',
            'D': 'maroon'
        }
        return color_map.get(grade, 'unknown')  # 'unknown' will be returned if grade is not in A, B, C, or D

    def extract_name(self, data):
        # This is a placeholder. You can define the logic to extract the name or assign an iterator as required
        # For now, I'm returning the id of the district as its name
        return data['properties']['id']

    def extract_section_8(self, data):
        return data['properties']['section8']

# Example of creating an instance:
# district_data = RedliningData['features'][0]  # Assuming RedliningData is the deserialized JSON data
# detroit_district = DetroitDistrict(district_data)
