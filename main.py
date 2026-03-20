import os
import random
import requests
import time
from gtts import gTTS

print(">> Zoro Shadow Warrior: Unique Script Mode Active...")

# ==========================================
# STEP 1: Huge Collection for Unique Stories
# ==========================================
# Jitne zyada options honge, utni hi unique har video hogi.
starts = [
    "Sannate ko chirte hue ek talwar ki awaaz aayi.",
    "Andheri raaton ka betaab musafir, Zoro phir laut aaya hai.",
    "Jab dunya so rahi hoti hai, tab Zoro jaag raha hota hai.",
    "Zoro... wo saya jo buraai ke liye maut ka paigham hai.",
    "Toofan se pehle ki khamoshi ko sirf Zoro samajhta hai.",
    "Ek purana dushman, aur ek nayi jung, Zoro taiyaar hai."
]

middles = [
    "Uska rasta mushkil hai, lekin uske irade lohe se mazboot hain.",
    "Wo na thakta hai, na rukta hai, bas apne maqsad ki taraf badhta hai.",
    "Dushman hazar hain, magar Zoro ki ek talwar hi kaafi hai.",
    "Andheron mein chhup kar waar karna uski fitrat nahi, wo samne se aata hai.",
    "Har zakhm uski taqat banta hai, har haar ek naya sabaq.",
    "Log kehte hain wo ek bhoot hai, magar wo insaaf ki zinda misaal hai."
]

ends = [
    "Abhi toh khel shuru hua hai, Zoro abhi baaki hai.",
    "Dushman ko dhool chatane ke baad, Zoro phir andheron mein kho gaya.",
    "Yaad rakhna, jab bhi zulm hoga, Zoro zaroori ayega.",
    "Zoro ki talwar ab thami hai, magar khatam nahi hui.",
    "Ye sirf ek kahani nahi, Zoro ka naya aaghaz hai.",
    "Agli baar dushman bach kar nahi jayega, ye Zoro ka waada hai."
]

# Unique combination banana
script = f"{random.choice(starts)} {random.choice(middles)} {random.choice(ends)}"
print(f"[{time.strftime('%H:%M:%S')}] New Unique Story: {script}")

# ==========================================
# STEP 2: Voiceover (Hindi/Urdu Mix)
# ==========================================
voice_filename = "voice.mp3"
try:
    tts = gTTS(text=script, lang='hi')
    tts.save(voice_filename)
    print("Voiceover generated successfully.")
except Exception as e:
    print(f"Voice Error: {e}")
    exit(1)

# ==========================================
# STEP 3: Dynamic Image Selection
# ==========================================
# Hum 3 random images uthayenge taake video bhi alag dikhe
image_urls = [
    "https://images.unsplash.com/photo-1519452635265-7b1fbfd1e4e0?q=80&w=720&h=1280&auto=format&fit=crop", # Samurai
    "https://images.unsplash.com/photo-1555597673-b21d5c935865?q=80&w=720&h=1280&auto=format&fit=crop", # Sword
    "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=720&h=1280&auto=format&fit=crop", # Night
    "https://images.unsplash.com/photo-1511367461989-f85a21fda167?q=80&w=720&h=1280&auto=format&fit=crop", # Sad/Dark
    "https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?q=80&w=720&h=1280&auto=format&fit=crop"  # Abstract/Intense
]

# Shuffle and pick 3
random.shuffle(image_urls)
selected_images = image_urls[:3]

downloaded = []
for i, url in enumerate(selected_images):
    filename = f"img{i}.jpg"
    res = requests.get(url)
    if res.status_code == 200:
        with open(filename, "wb") as f:
            f.write(res.content)
        downloaded.append(filename)

# ==========================================
# STEP 4: Render Final Video
# ==========================================
cmd = (
    f"ffmpeg -y -loop 1 -t 5 -i img0.jpg -loop 1 -t 5 -i img1.jpg -loop 1 -t 5 -i img2.jpg -i {voice_filename} "
    "-filter_complex \"[0:v][1:v][2:v]concat=n=3:v=1:a=0,scale=720:1280[v]\" "
    "-map \"[v]\" -map 3:a -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest output.mp4"
)
os.system(cmd)

if os.path.exists("output.mp4"):
    print("SUCCESS: Zoro's Unique Video is Ready!")
else:
    exit(1)
    
