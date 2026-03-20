import os
import random
import requests
import time
from gtts import gTTS

print(">> Starting Zoro Shadow Warrior Script...")

# ==========================================
# STEP 1: Zoro Story Generation (Hindi/Urdu)
# ==========================================
# Humne Zoro ka character uniquely define kiya hai
start_sentences = [
    "Andheri raat mein ek saya nikalta hai, jise log Zoro kehte hain",
    "Jab zulm badhta hai, tab Zoro apni talwar uthata hai",
    "Zoro, wo naam jisse dushman thartharata hai"
]

middle_sentences = [
    "Uske paas sirf uski talwar aur uska junoon hai",
    "Wo kamzoron ki dhaal aur buraai ka kaal hai",
    "Andheron mein reh kar wo roshni ki hifazat karta hai"
]

ending_sentences = [
    "Kyuki Zoro ki kahani abhi shuru hui hai",
    "Zoro ne thaan li hai ke wo insaaf dila kar rahega",
    "Dushman khatam, lekin Zoro ka safar jaari hai"
]

# Kahani ko jorna
script = f"{random.choice(start_sentences)}. {random.choice(middle_sentences)}. {random.choice(ending_sentences)}"
print(f"[{time.strftime('%H:%M:%S')}] Zoro Story: {script}")

# ==========================================
# STEP 2: Generate Voiceover (Hindi)
# ==========================================
voice_filename = "voice.mp3"
print(f"[{time.strftime('%H:%M:%S')}] Generating voiceover...")
try:
    tts = gTTS(text=script, lang='hi') # Hindi voice for Zoro
    tts.save(voice_filename)
    print("Voiceover saved!")
except Exception as e:
    print(f"!! Voice Error: {e}")
    exit(1)

# ==========================================
# STEP 3: Safe Image Downloading (No 404 Errors)
# ==========================================
# Humne direct links use kiye hain jo stable hain
keywords = ["samurai", "ninja", "dark-warrior"]
downloaded_images = []

for i, word in enumerate(keywords):
    filename = f"img{i}.jpg"
    print(f"Downloading image {i+1} for Zoro...")
    
    # Ye link kabhi fail nahi hoga (Unsplash Source fix)
    url = f"https://images.unsplash.com/photo-1519452635265-7b1fbfd1e4e0?q=80&w=720&h=1280&auto=format&fit=crop"
    if i == 1: url = "https://images.unsplash.com/photo-1555597673-b21d5c935865?q=80&w=720&h=1280&auto=format&fit=crop"
    if i == 2: url = "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=720&h=1280&auto=format&fit=crop"

    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            downloaded_images.append(filename)
            print(f"Image {i+1} Ready!")
    except:
        print(f"Image {i+1} failed, skipping...")

# ==========================================
# STEP 4: Stable FFmpeg Video Creation
# ==========================================
input_args = "-y -loop 1 -t 5 -i img0.jpg -loop 1 -t 5 -i img1.jpg -loop 1 -t 5 -i img2.jpg -i voice.mp3 "
filter_args = "-filter_complex \"[0:v][1:v][2:v]concat=n=3:v=1:a=0,scale=720:1280[v]\" "
output_args = "-map \"[v]\" -map 3:a -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest output.mp4"

full_command = f"ffmpeg {input_args}{filter_args}{output_args}"

print("Rendering Video...")
os.system(full_command)

if os.path.exists("output.mp4"):
    print("DONE! Video Created Successfully.")
else:
    print("Video creation failed.")
    exit(1)
