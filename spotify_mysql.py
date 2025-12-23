# Scenario 2:
# Extracting the metadata and storing it in mySQL
# Can query the table in mySQL.

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import re
import mysql.connector

# My SQL connection
db_config={ 'host':'localhost',
            'user':'root',
            'password':'1234',
            'database':'spotify_db'
            }

# set up connection
connection=mysql.connector.connect(**db_config)

#Cursor creation
cursor=connection.cursor()

# Authentication
sp=spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="c0a02977008243f6b96f13531651befb",client_secret="b1e1f1ccb75c43daba42e6abfdcf41d6"))

# Track URL
track_url="https://open.spotify.com/track/2YoPh281gD3xPnTkojVSr3"

# Track Id search
track_id=re.search(r'track/([a-zA-Z0-9]+)',track_url).group(1)

# Track fetch
track=sp.track(track_id)

# Fetching Meta data
track_data={ 'Track Name':track['name'],
             'Artist':track['artists'][0]['name'],
             "Album":track["album"]["name"],
             "Popularity":track["popularity"],
             "Duration":round(track["duration_ms"]/60000,2)
            }

# inserting data into SQL
insert_query=""" Insert into spotify_tracks (Track_name, Artist, Album, Popularity, Duration_minutes) 
                values (%s,%s,%s,%s,%s)
                """

cursor.execute(insert_query,(track_data['Track Name'],track_data['Artist'],track_data['Album'],track_data['Popularity'],track_data['Duration']))
connection.commit()

print(f"Track '{track_data['Track Name']}' by artist '{track_data['Artist']}' is inserted into database")
cursor.close()
connection.close()

