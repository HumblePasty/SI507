"""
Name: Haolin Li
Date: 10/12/2021
Email: haolinli@umich.edu
Description: This is a python script that will be used to
                analyze the redlining data for Detroit.
"""

import requests
import json

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import random as random
from matplotlib.path import Path
import numpy as np

import re
from collections import Counter

import pickle  # for caching

# Step 1: Fetch the JSON data
url = "https://dsl.richmond.edu/panorama/redlining/static/downloads/geojson/MIDetroit1939.geojson"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Deserialize the JSON data into a Python object
    RedliningData = response.json()
    with open('request.json', 'w', encoding='utf-8') as file:
        json.dump(RedliningData, file, ensure_ascii=False, indent=4)
else:
    print(f"Failed to retrieve the data. HTTP Status Code: {response.status_code}")

# directly read cache instead of using request
with open('request.json', 'r', encoding='utf-8') as file:
    RedliningData = json.load(file)

# Step 2: Develop the data structure of the redlining data.
# Step 2.1: Defining Detroit District class
random.seed(17)

# Define arrays of x (longitude) and y (latitude) coordinates creating a grid over the Detroit region
xgrid = np.arange(-83.5, -82.8, .004)
ygrid = np.arange(42.1, 42.6, .004)

# Generate a meshgrid (2D grid) from the x and y coordinate arrays
xmesh, ymesh = np.meshgrid(xgrid, ygrid)

# Flatten the 2D meshgrid to 1D and create an array of [longitude, latitude] points for the entire grid
points = np.vstack((xmesh.flatten(), ymesh.flatten())).T


class DetroitDistrict:
    def __init__(self, data, json=False):
        if(json):
            self.Coordinates = data['Coordinates']
            self.HolcGrade = data['HolcGrade']
            self.HolcColor = data['HolcColor']
            self.name = data['name']
            self.QualitativeDescription = data['QualitativeDescription']
            self.RandomLat = data['RandomLat']
            self.RandomLong = data['RandomLong']
            self.MedianIncome = data['MedianIncome']
            self.PercentBlack = data['PercentBlack']
            self.CensusTract = data['CensusTract']
            # self.IncomeRank = data['IncomeRank']
        else:
            self.Coordinates = self.extract_coordinates(data)
            self.HolcGrade = data['properties']['holc_grade']
            self.HolcColor = self.grade_to_color(self.HolcGrade)
            self.name = self.extract_name(data)
            self.QualitativeDescription = self.extract_section_8(data)
            self.RandomLong, self.RandomLat = self.choose_ramdom_pt()
            self.CensusTract = self.get_census_tract_code()
            self.MedianIncome = self.get_median_income()
            self.PercentBlack = self.get_percent_black()
            # self.IncomeRank = None

    def to_dict(self):
        return {
            'Coordinates': self.Coordinates,
            'HolcGrade': self.HolcGrade,
            'HolcColor': self.HolcColor,
            'name': self.name,
            'QualitativeDescription': self.QualitativeDescription,
            'RandomLat': self.RandomLat,
            'RandomLong': self.RandomLong,
            'MedianIncome': self.MedianIncome,
            'CensusTract': self.CensusTract,
            'PercentBlack': self.PercentBlack,  # assuming you added this
            # 'IncomeRank': self.IncomeRank  # assuming you added this
        }

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
        return data['properties']['holc_id']

    def extract_section_8(self, data):
        return data['properties']["area_description_data"]["8"]

    def choose_ramdom_pt(self):
        p = Path(self.Coordinates[0][0])
        grid = p.contains_points(points)
        point = points[random.choice(list(np.where(grid)[0]))]
        return point[0], point[1]

    # Step 5: Define a function to fetch census tract code for given latitude and longitude
    def get_census_tract_code(self):
        base_url = "https://geo.fcc.gov/api/census/block/find"
        params = {
            "latitude": self.RandomLat,
            "longitude": self.RandomLong,
            "censusYear": 2010,
            "format": "json"
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data["Block"]["FIPS"][:11]  # Tract code is the first 11 characters of FIPS
        else:
            print(f"Failed to get the tract data for {self.name}. HTTP Status Code: {response.status_code}")
            return None

    # Step 6: get MEDIAN HOUSEHOLD INCOME IN THE PAST 12 MONTHS
    def get_median_income(self):
        if self.CensusTract is None:
            print(f"Failed to get the income data for {self.name}. Census tract code is not available.")
            return None

        base_url = "https://api.census.gov/data/2018/acs/acs5"
        params = {
            # "get": "DP03_0062E", # not correct
            "get": "B19013_001E",  # median household income
            "for": f"tract:{self.CensusTract[5:11]}",
            "in": f"state:{self.CensusTract[:2]} county:{self.CensusTract[2:5]}",
            "key": "e3ad0cfc73b38d5637c909f70a91a7dcc9d40210"
        }

        # response = requests.get(base_url)
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            return int(data[1][0])
        else:
            print(f"Failed to get the income data for {self.name}. HTTP Status Code: {response.status_code}")
            return None

    # Bonus: get the percentage of black residents
    def get_percent_black(self):
        if self.CensusTract is None:
            print(
                f"Failed to get the percentage black resident data for {self.name}. Census tract code is not available.")
            return None
        base_url = "https://api.census.gov/data/2018/acs/acs5"
        params = {
            "get": "B02001_001E,B02001_003E",  # total population, black population
            "for": f"tract:{self.CensusTract[5:11]}",
            "in": f"state:{self.CensusTract[:2]} county:{self.CensusTract[2:5]}",
            "key": "e3ad0cfc73b38d5637c909f70a91a7dcc9d40210"
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            return int(data[1][1]) / int(data[1][0])  # black population / total population
        else:
            print(
                f"Failed to get the percentage black resident data for {self.name}. HTTP Status Code: {response.status_code}")
            return None


# Step 2.2: Defining Detroit Districts class
# Districts = [DetroitDistrict(data) for data in RedliningData['features']]  # comment this line if you want to use cache
#
# # Confirming that 238 objects are created
# print(len(Districts))
#
# # cache the data
# with open('Districts.pickle', 'wb') as file:
#     pickle.dump(Districts, file)
#
# # load the data from pickle file
# with open('Districts.pickle', 'rb') as file:
#     Districts = pickle.load(file)
#
# Convert each DetroitDistrict object to a dictionary
# districts_data = [district.to_dict() for district in Districts]
#
# # Save the list of dictionaries to a JSON file
# with open('Districts.json', 'w', encoding='utf-8') as file:
#     json.dump(districts_data, file, ensure_ascii=False, indent=4)

# Load the data from the JSON file
with open('Districts.json', 'r', encoding='utf-8') as file:
    districts_data = json.load(file)

# Recreate the list of DetroitDistrict objects
Districts = [DetroitDistrict(district,json=True) for district in districts_data]

# Step 3: plot the district data
fig, ax = plt.subplots()

# Iterate through each district in the Districts list
for district in Districts:
    # Extract the color of the district
    color = district.HolcColor

    # Some districts might have multiple polygons (non-contiguous). Handle such cases.
    for polygon_coords in district.Coordinates:
        # Check for Polygon or MultiPolygon (based on the data structure of the GeoJSON)
        if district.Coordinates[0][0][0][0] is not None and isinstance(district.Coordinates[0][0][0][0],
                                                                       (int, float, complex)):
            polygon = patches.Polygon(polygon_coords[0], closed=True, edgecolor='black', facecolor=color)
            ax.add_patch(polygon)
        else:
            for coords in polygon_coords:
                polygon = patches.Polygon(coords[0], closed=True, edgecolor='black', facecolor=color)
                ax.add_patch(polygon)

ax.autoscale()
plt.rcParams["figure.figsize"] = (15, 15)
plt.show()

# Step 4: pick a latitude and longitude coordinate from each of the districts.

# Set a fixed random seed for reproducibility
# random.seed(17)
#
# # Define arrays of x (longitude) and y (latitude) coordinates creating a grid over the Detroit region
# xgrid = np.arange(-83.5, -82.8, .004)
# ygrid = np.arange(42.1, 42.6, .004)
#
# # Generate a meshgrid (2D grid) from the x and y coordinate arrays
# xmesh, ymesh = np.meshgrid(xgrid, ygrid)
#
# # Flatten the 2D meshgrid to 1D and create an array of [longitude, latitude] points for the entire grid
# points = np.vstack((xmesh.flatten(), ymesh.flatten())).T
#
# # Loop over each district in the Districts list
# for j in Districts:
#     # Convert the coordinates of the district into a Path object for point-in-polygon checks
#     p = Path(j.Coordinates[0][0])
#
#     # Check which points from our grid are inside this district's polygon
#     grid = p.contains_points(points)
#
#     # Pick and print a random point from the ones inside the district
#     print(j, " : ", points[random.choice(list(np.where(grid)[0]))])
#
#     # Pick a random point from the ones inside the district
#     point = points[random.choice(list(np.where(grid)[0]))]
#
#     # Assign the randomly selected longitude and latitude to the district's attributes
#     j.RandomLong = point[0]
#     j.RandomLat = point[1]

# Step 5-6: Fetch census tract code and median income for each district
# See in the DetroitDistrict class

# Step 7: Load json file from the cache, see in Step 1


# Step 8: Calculate the mean and median of the median household income
# Initialize lists to store median incomes for each grade
A_incomes = [int(district.MedianIncome) for district in Districts if
             district.HolcGrade == 'A' and district.MedianIncome is not None]
B_incomes = [int(district.MedianIncome) for district in Districts if
             district.HolcGrade == 'B' and district.MedianIncome is not None]
C_incomes = [int(district.MedianIncome) for district in Districts if
             district.HolcGrade == 'C' and district.MedianIncome is not None]
D_incomes = [int(district.MedianIncome) for district in Districts if
             district.HolcGrade == 'D' and district.MedianIncome is not None]

# Calculate mean and median incomes for each grade
A_mean_income = sum(A_incomes) / len(A_incomes)
A_median_income = sorted(A_incomes)[len(A_incomes) // 2]
print(f"Mean avarage of income in A: {A_mean_income}")
print(f"Median of income in A: {A_median_income}")
B_mean_income = sum(B_incomes) / len(B_incomes)
B_median_income = sorted(B_incomes)[len(B_incomes) // 2]
print(f"Mean avarage of income in B: {B_mean_income}")
print(f"Median of income in B: {B_median_income}")
C_mean_income = sum(C_incomes) / len(C_incomes)
C_median_income = sorted(C_incomes)[len(C_incomes) // 2]
print(f"Mean avarage of income in C: {C_mean_income}")
print(f"Median of income in C: {C_median_income}")
D_mean_income = sum(D_incomes) / len(D_incomes)
D_median_income = sorted(D_incomes)[len(D_incomes) // 2]
print(f"Mean avarage of income in D: {D_mean_income}")
print(f"Median of income in D: {D_median_income}")

# Step 9: Use a list comprehension or other method to combine all the qualitative description strings for each
# district category.

# Combine the qualitative description strings for each district category
A_combined = ' '.join([district.QualitativeDescription for district in Districts if district.HolcGrade == 'A'])
B_combined = ' '.join([district.QualitativeDescription for district in Districts if district.HolcGrade == 'B'])
C_combined = ' '.join([district.QualitativeDescription for district in Districts if district.HolcGrade == 'C'])
D_combined = ' '.join([district.QualitativeDescription for district in Districts if district.HolcGrade == 'D'])

# Split each combined string into words using regex
A_words = re.findall(r'\w+', A_combined.lower())
B_words = re.findall(r'\w+', B_combined.lower())
C_words = re.findall(r'\w+', C_combined.lower())
D_words = re.findall(r'\w+', D_combined.lower())

# Filler words to filter out
filler_words = {'the', 'of', 'and', 'in', 'to', 'is', 'with', 'a', 'as', 'for', 'by', 'on', 'are', 'it', 'this', 'that',
                'an', 'at'}

# Filter out filler words and get word occurrences
A_word_counts = Counter(word for word in A_words if word not in filler_words)
B_word_counts = Counter(word for word in B_words if word not in filler_words)
C_word_counts = Counter(word for word in C_words if word not in filler_words)
D_word_counts = Counter(word for word in D_words if word not in filler_words)

# Find the 10 most common words unique to each category
all_most_common = set(
    word[0] for grade in [A_word_counts, B_word_counts, C_word_counts, D_word_counts] for word in grade.most_common(10))

A_10_Most_Common = [word[0] for word in A_word_counts.most_common() if
                    word[0] not in all_most_common - set(A_word_counts)][:10]
B_10_Most_Common = [word[0] for word in B_word_counts.most_common() if
                    word[0] not in all_most_common - set(B_word_counts)][:10]
C_10_Most_Common = [word[0] for word in C_word_counts.most_common() if
                    word[0] not in all_most_common - set(C_word_counts)][:10]
D_10_Most_Common = [word[0] for word in D_word_counts.most_common() if
                    word[0] not in all_most_common - set(D_word_counts)][:10]

print(A_10_Most_Common)
print(B_10_Most_Common)
print(C_10_Most_Common)
print(D_10_Most_Common)

# Bonus:
# 1. Add an attribute of black population percentage to the DetroitDistrict class
# See in the DetroitDistrict class

# 2. Add the rank attribute to the DetroitDistrict class
# Convert the median income to integer
for district in Districts:
    district.MedianIncome = int(district.MedianIncome) if district.MedianIncome is not None else None

# Filtering out districts that do not have an income_rank assigned
sorted_districts = sorted((district for district in Districts if district.MedianIncome is not None),
                          key=lambda x: x.MedianIncome, reverse=True)
# sorted_districts = sorted(Districts, key=lambda x: x.MedianIncome, reverse=True)

for rank, district in enumerate(sorted_districts, 1):
    district.IncomeRank = rank
# 3. Visually compare the income rank with the grade
# Initialize lists to store income ranks for each grade
A_ranks = [district.IncomeRank for district in Districts if district.MedianIncome is not None and district.HolcGrade == 'A']
B_ranks = [district.IncomeRank for district in Districts if district.MedianIncome is not None and district.HolcGrade == 'B']
C_ranks = [district.IncomeRank for district in Districts if district.MedianIncome is not None and district.HolcGrade == 'C']
D_ranks = [district.IncomeRank for district in Districts if district.MedianIncome is not None and district.HolcGrade == 'D']

# Create the boxplot
plt.boxplot([A_ranks, B_ranks, C_ranks, D_ranks], vert=True, patch_artist=True)

# Set labels
plt.xlabel('District Category')
plt.ylabel('Income Rank (1 being highest income)')
plt.title('Income Rank by District Category')
plt.xticks([1, 2, 3, 4], ['A', 'B', 'C', 'D'])

plt.show()

# Answer to the question:
# Findings:
# We found that districts with higher grades (A and B) generally have
# lower percentages of black or African American residents and higher income ranks. In contrast, districts with lower
# grades (C and D) have higher percentages of black or African American residents and lower income ranks. This
# pattern would suggest a historical trend of racial and economic segregation in Detroit's districts. Such findings
# would be consistent with the goals and outcomes of redlining, where districts with higher minority populations were
# often given lower grades, making them ineligible for certain financial services and further exacerbating
# socio-economic disparities.
#
# Reflection:
# This exercise further emphasizes the long-lasting implications of residential segregation policies from
# the past. While the findings were somewhat expected given what's known about redlining, seeing the clear trends in
# modern data highlights the long-term impact these policies have had on communities. It underscores the importance
# of understanding history when analyzing current socio-economic patterns.
