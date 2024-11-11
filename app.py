from flask import Flask, jsonify, request, render_template
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import mysql.connector
from dotenv import load_dotenv  # Importing load_dotenv to load environment variables from .env file

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure Spotify API credentials using environment variables
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

# Configure MySQL connection using environment variables
db_config = {
    'host': os.getenv("MYSQL_HOST"),
    'user': os.getenv("MYSQL_USER"),
    'password': os.getenv("MYSQL_PASSWORD"),
    'database': os.getenv("MYSQL_DATABASE")
}

# Sample recommendations based on moods
mood_recommendations = {
    "happy": [
        {"song": "Happy by Pharrell Williams", "url": "https://open.spotify.com/track/3PVd8jZ2L6ZbGRU6p2qUHA"},
        {"song": "Good Vibrations by The Beach Boys", "url": "https://open.spotify.com/track/0Ddr8qW4J9r9V0MQu43yLt"},
        {"song": "Uptown Funk by Mark Ronson ft. Bruno Mars", "url": "https://open.spotify.com/track/0eP6b33mZp2sl5Z2Lg74O4"},
        {"song": "Shake It Off by Taylor Swift", "url": "https://open.spotify.com/track/6pHnJgVqIp3Z6wVwYH9Y9n"}
    ],
    # Add other mood recommendations here
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
        for recommendation in recommendations:
            save_recommendation(user_input, mood, recommendation['song'], recommendation['url'])
        return jsonify({'recommendations': recommendations})

    try:
        # If no mood match, search Spotify
        result = sp.search(q=user_input, type='track', limit=1)
        if result['tracks']['items']:
            track = result['tracks']['items'][0]
            track_name = track['name']
            track_url = track['external_urls']['spotify']
            save_recommendation(user_input, "custom", track_name, track_url)
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

def save_recommendation(user_input, mood, song, url):
    """Save recommendation to MySQL database."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO recommendations (user_input, mood, song, url)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_input, mood, song, url))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
