'''from flask import Flask, jsonify, request, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Configure Spotify API credentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id="5031e779b10a49ffbac2d7ae75075e01",
    client_secret="5dc729c0a2314f78851e668b49f2d32d"
))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    data = request.json
    query = data.get('query')
    
    # Fetch recommendations based on user query
    result = sp.search(q=query, type='track', limit=1)
    track = result['tracks']['items'][0]
    track_name = track['name']
    track_url = track['external_urls']['spotify']
    
    return jsonify({'song': track_name, 'url': track_url})

if __name__ == '__main__':
    app.run(debug=True)'''
from flask import Flask, jsonify, request, render_template
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Configure Spotify API credentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id="5031e779b10a49ffbac2d7ae75075e01",                     
    client_secret="5dc729c0a2314f78851e668b49f2d32d"
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
    
    # Check for specific song requests
    if "recommend me" in user_input or "suggest a song" in user_input:
        # Respond with a random song recommendation
        additional_song = random.choice([
            {"song": "Shape of You by Ed Sheeran", "url": "https://open.spotify.com/track/7qiZsI1Y7C7W0M0F1O9k2f"},
            {"song": "Blinding Lights by The Weeknd", "url": "https://open.spotify.com/track/0VjIlz8d6xJgG8U1a8xJtC"},
            {"song": "Levitating by Dua Lipa", "url": "https://open.spotify.com/track/6p2eyZnCpTeGZ6NSU2RfEx"},
            {"song": "Don't Start Now by Dua Lipa", "url": "https://open.spotify.com/track/3DFe4rGoeU4LzJt2POw18j"}
        ])
        return jsonify({"additional_song": additional_song})

    # Determine the mood based on user input
    mood = None
    if any(word in user_input for word in ["happy", "joy", "excited"]):
        mood = "happy"
    elif any(word in user_input for word in ["sad", "down", "blue"]):
        mood = "sad"
    elif any(word in user_input for word in ["relaxed", "calm", "chill"]):
        mood = "relaxed"
    elif any(word in user_input for word in ["energetic", "active", "hyped"]):
        mood = "energetic"

    if mood and mood in mood_recommendations:
        recommendations = random.sample(mood_recommendations[mood], 3)  # Get 3 random recommendations
        return jsonify(recommendations)

    # Fetch general recommendations based on user query
    result = sp.search(q=user_input, type='track', limit=1)
    if result['tracks']['items']:
        track = result['tracks']['items'][0]
        track_name = track['name']
        track_url = track['external_urls']['spotify']
        return jsonify({'song': track_name, 'url': track_url})

    return jsonify({"message": "Sorry, I couldn't find any recommendations."})

if __name__ == '__main__':
    app.run(debug=True)
