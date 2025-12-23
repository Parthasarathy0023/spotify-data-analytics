# Scenario 1:
# Extracting data and csv file from single track
# Printing the dataframe
# Displaying the bar chart

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import re

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

# Print the values
print(f"\n Name of the track: {track_data['Track Name']}")
print(f"Artist name: {track_data['Artist']}")
print(f"Album : {track_data['Album']}")
print(f"Popularity: {track_data['Popularity']}")
print(f"Duration: {track_data['Duration']}")

# converting to dataframe
df=pd.DataFrame([track_data])


# Print the dataframe
print("\n The dataframe is below:")
print(df)

# Save metadata to csv file
df.to_csv("spotify_data_adiyae_kolluthey_.csv",index=False)

# Bar graph
features=["Popularity","Duration"]
values=[track_data["Popularity"],track_data["Duration"]]
plt.figure(figsize=(5,8))
plt.bar(features,values,color="Red",edgecolor="Blue")
plt.title(f"\n Title of the track {track_data['Track Name']}")
plt.ylabel("Duration")
plt.show()
