# Scenario 3:
# Getting data from multiple tracks from .txt file

import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector
import pandas as pd

# Set up Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='c0a02977008243f6b96f13531651befb',  # Replace with your Client ID
    client_secret='b1e1f1ccb75c43daba42e6abfdcf41d6'  # Replace with your Client Secret
))

# MySQL Database Connection
db_config = {
    'host': 'localhost',           # Change to your MySQL host
    'user': 'root',       # Replace with your MySQL username
    'password': '1234',   # Replace with your MySQL password
    'database': 'spotify_db'       # Replace with your database name
}

# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Read track URLs from file
file_path = "spotify_urls.txt"
with open(file_path, 'r') as file:
    track_urls = file.readlines()

# Empty list creation
all_tracks=[]

# Process each URL
for track_url in track_urls:
    track_url = track_url.strip()  # Remove any leading/trailing whitespace
    try:
        # Extract track ID from URL
        track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

        # Fetch track details from Spotify API
        track = sp.track(track_id)

        # Extract metadata
        track_data = {
            'Track Name': track['name'],
            'Artist': track['artists'][0]['name'],
            'Album': track['album']['name'],
            'Popularity': track['popularity'],
            'Duration (minutes)': round(track['duration_ms'] / 60000,2)
        }

        all_tracks.append(track_data)



        # Insert data into MySQL
        insert_query = """
        INSERT INTO all_spotify_tracks (track_name, artist, album, popularity, duration_minutes)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            track_data['Track Name'],
            track_data['Artist'],
            track_data['Album'],
            track_data['Popularity'],
            track_data['Duration (minutes)']
        ))
        connection.commit()

        print(f"Inserted: {track_data['Track Name']} by {track_data['Artist']} inserted into database")

    except Exception as e:
        print(f"Error processing URL: {track_url}, Error: {e}")

df=pd.DataFrame(all_tracks)
print(df)
df.to_csv("Spotify_all_tracks_data.csv",index=False)
# Close the connection
cursor.close()
connection.close()

print("All tracks have been processed and inserted into the database.")