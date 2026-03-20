import os
import random
import requests
import time
from gtts import gTTS

print(">> Zoro Story-Sync Mode: Downloading Relevant Images...")

# --- STEP 1: Unique Zoro Script & Keywords ---
# Humne har part ke sath ek keyword jora hai taaki image story se match kare
stories = [
    {
        "text": "Andheri raaton ka wo akela rahi, Zoro phir laut aaya hai.",
        "keywords": ["night-city", "dark-warrior", "moonlight"]
    },
    {
        "text": "Jab zulm had se badhta hai, tab Zoro ki talwar garajti hai.",
        "keywords": ["angry-man", "sword-fight", "fire-background"]
    },
    {
        "text": "Dushman hazar hain, magar Zoro ki ek talwar hi kaafi hai.",
        "keywords": ["samurai-action", "victory", "shadow-ninja"]
    }
]

selected = random.choice(stories)
script = selected["text"]
keywords = selected["keywords"]

print(f"[{time.strftime('%H:%M:%S')}] Story: {script}")

# --- STEP 2: Voiceover Generation ---
voice_file = "voice.mp3"
tts = gTTS(text=script, lang='hi')
tts.save(voice_file)

# --- STEP 3: Downloading Images based on Keywords ---
# Har keyword ke liye Unsplash se alag image download hogi
for i, word in enumerate(keywords):
    filename = f"img{i}.jpg"
    print(f"Downloading image for '{word}'...")
    url = f"https://images.unsplash.com/photo-1?q=80&w=720&h=1280&auto=format&fit=crop&{word}"
    
    try:
        res = requests.get(url, timeout=15)
        with open(filename, "wb") as f:
            f.write(res.content)
        print(f"Image {i+1} ({word}) saved!")
    except:
        print(f"Failed to get image for {word}")

# --- STEP 4: Cinematic Rendering (Zoom Effect) ---
# Ye images ko hilaayega (Motion) taaki video boring na lage
ffmpeg_cmd = (
    "ffmpeg -y "
    "-loop 1 -t 5 -i img0.jpg -loop 1 -t 5 -i img1.jpg -loop 1 -t 5 -i img2.jpg "
    "-i voice.mp3 "
    "-filter_complex "
    "\"[0:v]scale=1280:2276,zoompan=z='min(zoom+0.0015,1.5)':d=125:s=720x1280[v0]; "
    "[1:v]scale=1280:2276,zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=720x1280[v1]; "
    "[2:v]scale=1280:2276,zoompan=z='min(zoom+0.0015,1.5)':d=125:s=720x1280[v2]; "
    "[v0][v1][v2]concat=n=3:v=1:a=0[v]\" "
    "-map \"[v]\" -map 3:a -c:v libx264 -pix_fmt yuv420p -shortest output.mp4"
)

print("Rendering Professional Zoro Video...")
os.system(ffmpeg_cmd)
print("SUCCESS: Story-Sync Video Created!")
