#!/usr/bin/env python
# coding: utf-8

# #                              We Provide Suitable Locations

# ## Part 1 - Web Scrapping

# In this part, we will collect some important data from internet
# 
# **For Link of the page: <a href='https://en.wikipedia.org/wiki/List_of_neighbourhoods_in_Mumbai'>Click here<a/>**

# In[1]:


import urllib.request


# In[2]:


page = urllib.request.urlopen('https://en.wikipedia.org/wiki/List_of_neighbourhoods_in_Mumbai')


# **Import the BeautifulSoup library so we can parse HTML and XML documents**

# In[3]:


from bs4 import BeautifulSoup


# In[4]:


soup = BeautifulSoup(page, "lxml")


# In[5]:


soup.title.string


# **To see all the tables present in the page**

# In[6]:


all_tables = soup.find_all('table')


# In[7]:


right_table=soup.find('table', class_='wikitable sortable')
#right_table


# In[8]:


A=[]
B=[]
C=[]
D=[]


for row in right_table.findAll('tr'):
    cells=row.findAll('td')
    if len(cells)==4:
        A.append(cells[0].find(text=True))
        B.append(cells[1].find(text=True))
        C.append(cells[2].find(text=True))
        D.append(cells[3].find(text=True))


# In[9]:


import pandas as pd

mumbai_neighborhoods = pd.DataFrame(A,columns=['Area'])
mumbai_neighborhoods['Location'] = B
mumbai_neighborhoods['Latitude'] = C
mumbai_neighborhoods['Longitude'] = D


# In[10]:


mumbai_neighborhoods.dtypes


# In[11]:


mumbai_neighborhoods['Latitude'] = mumbai_neighborhoods['Latitude'].astype('float')
mumbai_neighborhoods['Longitude'] = mumbai_neighborhoods['Longitude'].astype('float')


# In[12]:


mumbai_neighborhoods.head()


# In[13]:


mumbai_neighborhoods.shape


# **We found out 93 areas of Mumbai**

# ### Now let's found out mumbai coordinates and plot neighborhoods in its map

# In[157]:


import folium

#!conda install -c conda-forge folium=0.5.0 --yes
#import folium # plotting library

from geopy.geocoders import Nominatim

#!conda install -c conda-forge geopy --yes 
#from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values


# In[15]:


address = 'Mumbai, India'
geolocator = Nominatim(user_agent='ny_explorer')
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# In[16]:


map_neigh = folium.Map(location=[latitude, longitude], zoom_start=13)
map_neigh


# In[17]:


for lat, lon, neighborhood in zip(mumbai_neighborhoods['Latitude'], mumbai_neighborhoods['Longitude'], mumbai_neighborhoods['Area']):
    label = '{}'.format(neighborhood)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_neigh)

    
map_neigh 


# In[ ]:





# ## Part 2 - Foursquare

# Now let's find out all venues in all mentioned areas above

# In[158]:


import requests # library to handle requests
import numpy as np # library to handle data in a vectorized manner
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize


# In[19]:


CLIENT_ID = 'REPHQH1ZB4HATS1S03UMIVN4QT0PLNM0EB0DMZPKELFWTDXJ' # your Foursquare ID
CLIENT_SECRET = 'TU1OYK5MXOKWNPRLQI0CORK4CY3XORQTAVTORKNZ5PX4M0GO' # your Foursquare Secret
VERSION = '20180604'
#LIMIT = 30
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# In[20]:


radius = 2000
LIMIT = 30
venues = []

for lat, lon, neighborhood in zip(mumbai_neighborhoods['Latitude'], mumbai_neighborhoods['Longitude'], mumbai_neighborhoods['Area']):
    url = 'https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&ll={},{}&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, lat, lon, VERSION, radius, LIMIT)
    
    results = requests.get(url).json()['response']['groups'][0]['items']
    
    for venue in results:
        venues.append((
            neighborhood,
            lat, 
            lon, 
            venue['venue']['name'], 
            venue['venue']['location']['lat'], 
            venue['venue']['location']['lng'],  
            venue['venue']['categories'][0]['name']))


# In[21]:


final_dataset = pd.DataFrame(venues)


# In[22]:


final_dataset.columns=['Area', 'Latitude', 'Longitude', 'Venue Name', 'Venue Latitude', 'Venue Longitude', 'Venue Category']
final_dataset.shape


# In[23]:


final_dataset.head()


# In[34]:


final_dataset.dtypes


# In[59]:


final_dataset.isnull().sum()


# The dataset don't have any null values

# In[30]:


Area_grouped_data = final_dataset.groupby(['Area']).count()


# In[91]:


Area_grouped_data.head()


# In[46]:


Area_grouped_data['less_than_10'] = Area_grouped_data['Latitude']<=10


# This will tell us which Areas have less than 10 stalls or restaurants

# In[ ]:


Area_grouped_data = Area_grouped_data.reset_index()


# In[61]:


namesof_less_than_10 = [Area_grouped_data['Area'][i] for i in range(len(Area_grouped_data['less_than_10'])) if Area_grouped_data['less_than_10'][i]==True]


# In[62]:


namesof_less_than_10


# **These are some areas which have less than 10 stalls/restaurants**

# ## Part 3 - Analyzing

# In[27]:


print('There are {} uniques categories.'.format(len(final_dataset['Venue Category'].unique())))


# In[115]:


# one hot encoding
mumbai_onehot = pd.get_dummies(final_dataset[['Venue Category']], prefix="", prefix_sep="")

# add neighborhood column back to dataframe
mumbai_onehot['Area'] = final_dataset['Area'] 

# move neighborhood column to the first column
fixed_columns = [mumbai_onehot.columns[-1]] + list(mumbai_onehot.columns[:-1])
mumbai_onehot = mumbai_onehot[fixed_columns]

print(mumbai_onehot.shape)
mumbai_onehot.head()


# #### Next, let's group rows by neighborhood and by taking the mean of the frequency of occurrence of each category

# In[117]:


mumbai_grouped = mumbai_onehot.groupby(["Area"]).mean().reset_index()

print(mumbai_grouped.shape)
mumbai_grouped


# In[114]:


mumbai_onehot.shape


# #### Let's print each neighborhood along with the top 5 most common venues

# In[118]:


num_top_venues = 5

for hood in mumbai_grouped['Area']:
    print("----"+hood+"----")
    temp = mumbai_grouped[mumbai_grouped['Area'] == hood].T.reset_index()
    temp.columns = ['venue','freq']
    temp = temp.iloc[1:]
    temp['freq'] = temp['freq'].astype(float)
    temp = temp.round({'freq': 2})
    print(temp.sort_values('freq', ascending=False).reset_index(drop=True).head(num_top_venues))
    print('\n')


# #### Let's put that into a *pandas* dataframe

# First, let's write a function to sort the venues in descending order.

# In[119]:


def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)
    
    return row_categories_sorted.index.values[0:num_top_venues]


# Now let's create the new dataframe and display the top 10 venues for each neighborhood.

# In[131]:


num_top_venues = 10

indicators = ['st', 'nd', 'rd']

# create columns according to number of top venues
columns = ['Area']
for ind in range(num_top_venues):
    if ind<=2:
        columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
    else:    
        columns.append('{}th Most Common Venue'.format(ind+1))


# In[132]:


columns


# In[134]:


# create a new dataframe
areas_venues_sorted = pd.DataFrame(columns=columns)
areas_venues_sorted['Area'] = mumbai_grouped['Area']

for ind in range(mumbai_grouped.shape[0]):
    areas_venues_sorted.iloc[ind, 1:] = return_most_common_venues(mumbai_grouped.iloc[ind, :], num_top_venues)

areas_venues_sorted.head()


# ## Part 4 - Clustering

# In[138]:


# set number of clusters
kclusters = 5

mumbai_grouped_clustering = mumbai_grouped.drop('Area', 1)

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(mumbai_grouped_clustering)

# check cluster labels generated for each row in the dataframe
kmeans.labels_[0:10] 


# In[139]:


# add clustering labels
areas_venues_sorted.insert(0, 'Cluster Labels', kmeans.labels_)

mumbai_merged = mumbai_neighborhoods

# merge toronto_grouped with toronto_data to add latitude/longitude for each neighborhood
mumbai_merged = mumbai_merged.join(areas_venues_sorted.set_index('Area'), on='Area')

mumbai_merged.head() # check the last columns!


# In[147]:


# create map
map_clusters = folium.Map(location=[latitude, longitude], zoom_start=11)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i + x + (i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(mumbai_merged['Latitude'], mumbai_merged['Longitude'], mumbai_merged['Area'], mumbai_merged['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_clusters)
       
map_clusters


# ## Part 5 - Clusters

# #### Cluster 1

# In[148]:


mumbai_merged.loc[mumbai_merged['Cluster Labels'] == 0, mumbai_merged.columns[[1] + list(range(5, mumbai_merged.shape[1]))]]


# #### Cluster 2

# In[149]:


mumbai_merged.loc[mumbai_merged['Cluster Labels'] == 1, mumbai_merged.columns[[1] + list(range(5, mumbai_merged.shape[1]))]]


# #### Cluster 3

# In[150]:


mumbai_merged.loc[mumbai_merged['Cluster Labels'] == 2, mumbai_merged.columns[[1] + list(range(5, mumbai_merged.shape[1]))]]


# #### Cluster 4

# In[151]:


mumbai_merged.loc[mumbai_merged['Cluster Labels'] == 3, mumbai_merged.columns[[1] + list(range(5, mumbai_merged.shape[1]))]]


# #### Cluster 5

# In[152]:


mumbai_merged.loc[mumbai_merged['Cluster Labels'] == 4, mumbai_merged.columns[[1] + list(range(5, mumbai_merged.shape[1]))]]

