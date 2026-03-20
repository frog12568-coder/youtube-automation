import os
import random
import requests
import time
from gtts import gTTS

print(">> Zoro Pro Video Mode: Zoom + Motion Active...")

# ==========================================
# STEP 1: Unique Story
# ==========================================
starts = ["Sannate ko chirte hue Zoro ki talwar garji.", "Andheri raaton ka wo akela rahi, Zoro.", "Jab zulm badhta hai, tab Zoro nikalta hai."]
middles = ["Dushman hazar hain, magar uski ek talwar kaafi hai.", "Wo thakta nahi, wo rukta nahi, bas badhta jata hai.", "Uska nishana kabhi nahi chukta."]
ends = ["Zoro ka insaaf abhi shuru hua hai.", "Yaad rakhna, Zoro laut kar zaroor ayega.", "Ye sirf aaghaz hai, anjam abhi baaki hai."]

script = f"{random.choice(starts)} {random.choice(middles)} {random.choice(ends)}"
voice_filename = "voice.mp3"

# Voice Generation
tts = gTTS(text=script, lang='hi')
tts.save(voice_filename)

# ==========================================
# STEP 2: Images Download
# ==========================================
image_urls = [
    "https://images.unsplash.com/photo-1519452635265-7b1fbfd1e4e0?q=80&w=720&h=1280&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1555597673-b21d5c935865?q=80&w=720&h=1280&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=720&h=1280&auto=format&fit=crop"
]

for i, url in enumerate(image_urls):
    res = requests.get(url)
    with open(f"img{i}.jpg", "wb") as f:
        f.write(res.content)

# ==========================================
# STEP 3: Professional FFmpeg (Zoom + Music)
# ==========================================
# Hum yahan 'zoompan' filter use kar rahe hain jo image ko animate karega
cmd = (
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

print("Rendering Professional Video...")
os.system(cmd)
print("Done!")
