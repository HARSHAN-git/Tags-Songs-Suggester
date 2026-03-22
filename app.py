from flask import Flask, request, jsonify
from flask_cors import CORS                 #Allows Chrome extension to call Flask API
from PIL import Image                       #Used to open image from bytes
import io
import base64
import torch
from transformers import CLIPProcessor, CLIPModel
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("spotify.env")

app = Flask(__name__)
CORS(app)

# Load CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Labels
labels = [
    "college", "school", "festival", "nature", "sunset", "beach",
    "street food", "birthday", "selfie", "temple", "night sky", "car",
    "bike", "love", "friends", "solo trip", "rain", "books", "classroom",
    "football", "cricket", "exam", "hostel", "library", "picnic", "DJ party",
    "independence day", "ganesh chaturthi", "holi", "onam", "eid", "navratri",
    "sleep", "gaming", "meme", "shopping", "chai", "coffee"
]

# Spotify setup
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )   
)

def analyze_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    image = image.convert("RGB")    #cause clip requires rgb
    inputs = processor(
        text=labels,
        images=image,
        return_tensors="pt",
        padding=True
    )
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1).detach().numpy()[0]
    top_indices = probs.argsort()[-3:][::-1]
    top_labels = [labels[i] for i in top_indices]
    return [f"#{label}" for label in top_labels], suggest_songs(top_labels)

def suggest_songs(keywords):
    songs = []
    try:
        for word in keywords:
            results = sp.search(
                q=word,
                type="track",
                limit=2,
                market="IN"
            )
            for item in results["tracks"]["items"]:
                song_name = item["name"]
                artist_name = item["artists"][0]["name"]
                songs.append(f"{song_name} by {artist_name}")
    except Exception as e:
        print("Spotify blocked:", e)
        songs = ["Spotify restricted"]
    return songs

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        image_b64 = data.get("image")
        if not image_b64:
            return jsonify({"error": "No image"}), 400
        # Remove data:image/... prefix if exists
        if "base64," in image_b64:
            image_b64 = image_b64.split("base64,")[1]
        # Fix padding
        missing_padding = len(image_b64) % 4
        if missing_padding:
            image_b64 += "=" * (4 - missing_padding)
        image_data = base64.b64decode(image_b64)
        tags, songs = analyze_image(image_data)
        return jsonify({
            "tags": tags,
            "songs": songs
        })
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Tag & Song API Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)