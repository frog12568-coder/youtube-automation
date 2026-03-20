import os
import random
import requests
import time
from gtts import gTTS

print(">> Zoro Alpha Mode: Using Stable Image Engine...")

# --- STEP 1: Unique Zoro Stories ---
stories = [
    {"text": "Andheri raat, sunsan raaste, aur Zoro ki chamakti talwar. Buraai ka waqt khatam hua.", "tag": "dark,warrior"},
    {"text": "Zoro ki ek jhalak hi dushman ko darane ke liye kaafi hai. Insaaf ab door nahi.", "tag": "samurai,action"},
    {"text": "Zoro ne thaan li hai, jab tak aakhri dushman zinda hai, wo rukega nahi.", "tag": "sword,ninja"}
]

selected = random.choice(stories)
script = selected["text"]
print(f"[{time.strftime('%H:%M:%S')}] Story: {script}")

# --- STEP 2: Voiceover (Hindi) ---
voice_file = "voice.mp3"
try:
    tts = gTTS(text=script, lang='hi')
    tts.save(voice_file)
    print("Voiceover generated.")
except Exception as e:
    print(f"Voice Error: {e}")
    exit(1)

# --- STEP 3: Stable Image Downloading (New Engine) ---
# Hum 'picsum.photos' use kar rahe hain jo 100% stable hai aur block nahi hota
for i in range(3):
    filename = f"img{i}.jpg"
    print(f"Downloading stable image {i+1}...")
    
    # Random High-Quality Images (Portrait Mode 720x1280)
    # Sig parameter ensures every image is different
    url = f"https://picsum.photos/720/1280?random={random.randint(1, 1000)}"
    
    try:
        r = requests.get(url, timeout=20, allow_redirects=True)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"Image {i} saved successfully.")
        else:
            raise Exception("Status code not 200")
    except Exception as e:
        print(f"Image {i} failed, using emergency placeholder.")
        # Emergency backup image if everything fails
        backup = requests.get("https://baconmockup.com/720/1280") 
        with open(filename, "wb") as f:
            f.write(backup.content)

# --- STEP 4: High-Quality FFmpeg Rendering ---
# Simple but effective command to avoid "Invalid Data" errors
cmd = (
    "ffmpeg -y "
    "-loop 1 -t 5 -i img0.jpg -loop 1 -t 5 -i img1.jpg -loop 1 -t 5 -i img2.jpg "
    "-i voice.mp3 "
    "-filter_complex \"[0:v]scale=720:1280,format=yuv420p[v0];"
    "[1:v]scale=720:1280,format=yuv420p[v1];"
    "[2:v]scale=720:1280,format=yuv420p[v2];"
    "[v0][v1][v2]concat=n=3:v=1:a=0[v]\" "
    "-map \"[v]\" -map 3:a -c:v libx264 -preset ultrafast -shortest output.mp4"
)

print("Finalizing Zoro Video...")
os.system(cmd)

if os.path.exists("output.mp4"):
    print("SUCCESS: Video is ready for download!")
else:
    print("Rendering failed.")
    exit(1)
