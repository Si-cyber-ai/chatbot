from flask import Flask, jsonify, request, render_template
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import mysql.connector
from dotenv import load_dotenv  # Load environment variables from .env file

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    user_input = request.json.get('query', '').lower()
    mood = get_mood_from_input(user_input)

    # Use Spotify API for dynamic mood-based recommendations
    if mood:
        recommendations = get_spotify_recommendations(mood, 3)  # Get 3 Spotify recommendations for the mood
        if recommendations:
            for recommendation in recommendations:
                save_recommendation(user_input, mood, recommendation['song'], recommendation['url'])
            return jsonify({'recommendations': recommendations})

    # Fallback for specific user query search
    try:
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
    """Determine mood based on keywords in the user's input."""
    if any(word in user_input for word in ["happy", "joy", "excited"]):
        return "happy"
    elif any(word in user_input for word in ["sad", "down", "blue"]):
        return "sad"
    elif any(word in user_input for word in ["relaxed", "calm", "chill"]):
        return "relaxed"
    elif any(word in user_input for word in ["energetic", "active", "hyped"]):
        return "energetic"
    return None

def get_spotify_recommendations(mood, count):
    """Fetch a specified number of mood-based recommendations from Spotify."""
    mood_queries = {
        "happy": "happy upbeat",
        "sad": "sad mellow",
        "relaxed": "relaxing calm",
        "energetic": "energetic workout"
    }
    
    recommendations = []
    query = mood_queries.get(mood, "chill")  # Fallback to 'chill' if mood not mapped
    
    # Spotify search for the mood-based songs
    try:
        results = sp.search(q=query, type='track', limit=count)
        for item in results['tracks']['items']:
            recommendations.append({
                'song': item['name'],
                'url': item['external_urls']['spotify']
            })
    except Exception as e:
        print(f"Error while fetching recommendations: {e}")
    
    return recommendations if recommendations else None

def save_recommendation(user_input, mood, song, url):
    """Save the user's recommendation to the MySQL database."""
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

