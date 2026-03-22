# 🎵 Tags & Songs Suggester (Chrome Extension + CLIP + Spotify)

A Chrome extension that analyzes uploaded images on social media platforms and suggests **relevant tags** and **songs** using a **CLIP vision model** and **Spotify API**.

---

## 🚀 Features

* 📸 Detects image upload on Instagram, YouTube, Twitter, LinkedIn
* 🧠 Uses OpenAI CLIP model for image understanding
* 🏷️ Generates top 3 semantic tags
* 🎵 Suggests songs using Spotify API
* ⚡ Real-time suggestions
* 🧩 Chrome Extension popup UI
* 💾 Uses chrome.storage for communication

---

## 🏗️ Project Architecture

```
User Upload Image
        ↓
content.js detects upload
        ↓
Image → Base64
        ↓
Flask Backend (app.py)
        ↓
CLIP Model → Tags
        ↓
Spotify API → Songs
        ↓
Return JSON
        ↓
chrome.storage
        ↓
popup.js
        ↓
popup.html UI
```

---

## 📂 Project Structure

```
Tags-Songs-Suggester/
│
├── app.py
├── content.js
├── manifest.json
├── popup.html
├── popup.js
├── popup.css
├── spotify.env
└── README.md
```

---

## 🧠 Tech Stack

* Python (Flask)
* OpenAI CLIP Model
* Spotify Web API
* JavaScript (Chrome Extension)
* HTML + CSS
* Chrome Storage API

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/tags-songs-suggester.git
cd tags-songs-suggester
```

---

### 2. Install dependencies

```bash
pip install flask flask-cors pillow torch transformers spotipy python-dotenv
```

---

### 3. Add Spotify credentials

Create `spotify.env`

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_secret
```

---

### 4. Run Flask backend

```bash
python app.py
```

Server runs on:

```
http://127.0.0.1:5000
```

---

### 5. Load Chrome Extension

1. Open Chrome
2. Go to `chrome://extensions/`
3. Enable **Developer mode**
4. Click **Load unpacked**
5. Select project folder

---

## 🧪 How It Works

1. Upload image on Instagram
2. Extension detects file input
3. Image converted to Base64
4. Sent to Flask backend
5. CLIP model predicts tags
6. Spotify returns songs
7. Popup displays results

---

## 🖼️ Example Output

**Tags**

```
#ganesh chaturthi
#navratri
#onam
```

**Songs**

```
Shendur Laal Chadhayo — Ravindra Sathe
Ganesh Chaturthi Dhol Tasha — DJ Seshi
```

---

## 🔐 Permissions Used

* activeTab
* scripting
* storage

---

## 👨‍💻 Author

Harshan R
CSE Student | ML Enthusiast

---

## ⭐ If you like this project

Give it a star on GitHub!
