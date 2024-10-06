import nltk
from flask import Flask, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# Initialize Flask app
app = Flask(__name__)

# Spotify API credentials (replace with your own)
SPOTIPY_CLIENT_ID = 'your_spotify_client_id'
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'

# Set up Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, 
    client_secret=SPOTIPY_CLIENT_SECRET))

# Download NLTK resources
nltk.download('punkt')

# NLP: Function to classify user intent
def classify_message(message):
    tokens = nltk.word_tokenize(message.lower())
    
    if any(word in tokens for word in ['relax', 'chill', 'calm']):
        return 'relaxing'
    elif any(word in tokens for word in ['pop', 'mainstream']):
        return 'pop'
    elif any(word in tokens for word in ['workout', 'exercise']):
        return 'workout'
    elif any(word in tokens for word in ['jazz', 'classic']):
        return 'jazz'
    elif any(word in tokens for word in ['trending', 'popular']):
        return 'trending'
    else:
        return 'unknown'

# Function to fetch music from Spotify API based on genre/intent
def get_spotify_recommendations(genre):
    genre_map = {
        'relaxing': 'chill',
        'pop': 'pop',
        'workout': 'workout',
        'jazz': 'jazz',
        'trending': 'toplists'
    }
    
    if genre in genre_map:
        result = sp.search(q=f'genre:{genre_map[genre]}', type='track', limit=5)
        recommendations = [track['name'] + ' by ' + track['artists'][0]['name'] for track in result['tracks']['items']]
        return recommendations
    else:
        return []

# Route to handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message').lower()

    # Classify user intent
    intent = classify_message(user_input)

    if intent != 'unknown':
        recommendations = get_spotify_recommendations(intent)
        if recommendations:
            response = f"Here are some {intent} songs: " + ", ".join(recommendations)
        else:
            response = f"Sorry, I couldn't find any {intent} music right now."
    else:
        response = "I can recommend relaxing, pop, workout, jazz, or trending music. What would you like?"

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
