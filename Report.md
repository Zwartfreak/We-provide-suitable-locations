# We-provide-suitable-locations

## 1. Introduction

This repo is based on providing location insights to the client or the businessman.
Problem Statement:
Let's consider a man named Shray. Recently, he is shifted to Mumbai.
Now, he don't know much about the city and it's famous locations. He wants to open a restaurant in Mumbai.

Now our task is to provide him with enough data so that he could decide a place on his own for his new shop.

## 2. Data

#### Explaining data:
First of all I want to tell that I will be using Foursquare location API to get location data easily and convert it in an easy and understandable format.

Foursquare is the most trusted, independent location data platform for understanding how people move through the real world.

#### Dataset:
I have imported data of all the restaurants present in Mumbai using the Foursquare api. Now I will cluster data according to locations and categories provided by the api. This will provide me the relevant data of restaurants: Locations where there are more number of restaurants Categories of restaurants which are common.

I will use the API once as it will provide me with all the location of restaurants in Mumbai.

#####What data can be extracted:
Latitude of each restaurant
Longitude of each restaurant
Address of each restaurant
City in which they are located
Distance, Name of the restaurant
Category of the restaurant, ex: Indian, Chinese.

## 3. Methodology

#### Foursquare API:
This project would use Four-square API as its prime data gathering source as it has a database of millions of places, especially their places API which provides the ability to perform location search, location sharing and details about a business.

#### Work Flow:
Using credentials of Foursquare API features of near-by places of the neighborhoods would be mined. Due to http request limitations the number of places per neighborhood parameter would reasonably be set to 100 and the radius parameter would be set to 500.

#### Clustering Approach:
To compare the similarities of two cities, we decided to explore neighborhoods, segment them, and group them into clusters to find similar neighborhoods in a big city like New York and Toronto. To be able to do that, we need to cluster data which is a form of unsupervised machine learning: k-means clustering algorithm

#### Libraries Which are Used to Develope the Project:

Pandas: For creating and manipulating dataframes.

Folium: Python visualization library would be used to visualize the neighborhoods cluster distribution of using interactive leaflet map.

Scikit Learn: For importing k-means clustering.

JSON: Library to handle JSON files.

XML: To separate data from presentation and XML stores data in plain text format.

Geocoder: To retrieve Location Data.

Beautiful Soup and Requests: To scrap and library to handle http requests.

Matplotlib: Python Plotting Module.

## 4. Results

All results of cluseters are being shared on Code.
