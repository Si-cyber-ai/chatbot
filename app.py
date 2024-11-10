from flask import Flask, jsonify, request, render_template
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv  # Importing load_dotenv to load environment variables from .env file

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure Spotify API credentials using environment variables
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),  # Updated to fetch from environment variables
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")  # Updated to fetch from environment variables
))

# Sample recommendations based on moods
mood_recommendations = {
    "happy": [
        {"song": "Happy by Pharrell Williams", "url": "https://open.spotify.com/track/3PVd8jZ2L6ZbGRU6p2qUHA"},
        {"song": "Good Vibrations by The Beach Boys", "url": "https://open.spotify.com/track/0Ddr8qW4J9r9V0MQu43yLt"},
        {"song": "Uptown Funk by Mark Ronson ft. Bruno Mars", "url": "https://open.spotify.com/track/0eP6b33mZp2sl5Z2Lg74O4"},
        {"song": "Shake It Off by Taylor Swift", "url": "https://open.spotify.com/track/6pHnJgVqIp3Z6wVwYH9Y9n"}
    ],
    "sad": [
        {"song": "Someone Like You by Adele", "url": "https://open.spotify.com/track/0zW1E2M3x0J6HyD4N9R1gB"},
        {"song": "Fix You by Coldplay", "url": "https://open.spotify.com/track/4pTg8BBcKXb8xM7U2FwRaO"},
        {"song": "Let Her Go by Passenger", "url": "https://open.spotify.com/track/4Q3G0DmbAez0yqgFBLd9t3"},
        {"song": "Back to December by Taylor Swift", "url": "https://open.spotify.com/track/6dr0Qv5AYclT0zFmqx9uxV"}
    ],
    "relaxed": [
        {"song": "Weightless by Marconi Union", "url": "https://open.spotify.com/track/7q2aJwLgRJpVxG3OUK4KrD"},
        {"song": "Sunset Lover by Petit Biscuit", "url": "https://open.spotify.com/track/3rZ9TzPmqn6L5h0rZ1wKP4"},
        {"song": "Cold Little Heart by Michael Kiwanuka", "url": "https://open.spotify.com/track/2HSmTffDe26QuWzYzXWsUp"},
        {"song": "River by Leon Bridges", "url": "https://open.spotify.com/track/3gqVJ4LkGtIitFJd7bMRW2"}
    ],
    "energetic": [
        {"song": "Can’t Stop the Feeling! by Justin Timberlake", "url": "https://open.spotify.com/track/6mQV1N7tnjG06wBSSmH5U9"},
        {"song": "Titanium by David Guetta ft. Sia", "url": "https://open.spotify.com/track/0b9jY52yA2fB9sVfXJd9Z0"},
        {"song": "Bang Bang by Jessie J, Ariana Grande, Nicki Minaj", "url": "https://open.spotify.com/track/1qk2i6eJhbSgjO4DmrNYX4"},
        {"song": "Stronger by Kanye West", "url": "https://open.spotify.com/track/1nOV8LeD5NG9g35G2CbmMn"}
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    user_input = request.json.get('query', '').lower()
    mood = get_mood_from_input(user_input)
    
    if mood:
        recommendations = random.sample(mood_recommendations[mood], 3)  # Get 3 random recommendations
        return jsonify({'recommendations': recommendations})

    try:
        # If no mood match, search Spotify
        result = sp.search(q=user_input, type='track', limit=1)
        if result['tracks']['items']:
            track = result['tracks']['items'][0]
            track_name = track['name']
            track_url = track['external_urls']['spotify']
            return jsonify({'song': track_name, 'url': track_url})

        return jsonify({"message": "Sorry, I couldn't find any recommendations."})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"message": "An error occurred while fetching the recommendation."})

def get_mood_from_input(user_input):
    if any(word in user_input for word in ["happy", "joy", "excited"]):
        return "happy"
    elif any(word in user_input for word in ["sad", "down", "blue"]):
        return "sad"
    elif any(word in user_input for word in ["relaxed", "calm", "chill"]):
        return "relaxed"
    elif any(word in user_input for word in ["energetic", "active", "hyped"]):
        return "energetic"
    return None

if __name__ == '__main__':
    app.run(debug=True)
