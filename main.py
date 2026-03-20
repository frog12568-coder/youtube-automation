from gtts import gTTS
import os
import random
import requests

# STEP 1: Story parts
start = ["Ek gareeb bacha tha", "Ek chota ladka tha"]
middle = ["log uska mazak urate thay", "uske paas paise nahi thay"]
ending = ["lekin usne himmat nahi hari", "aur aaj woh successful hai"]

# Combine story
script = random.choice(start) + ". " + random.choice(middle) + ". " + random.choice(ending)

print(script)

# STEP 2: Voice
tts = gTTS(script, lang='ur')
tts.save("voice.mp3")

# STEP 3: Keywords (simple)
keywords = ["sad child", "struggle", "success"]

# STEP 4: Download images
for i, word in enumerate(keywords):
    url = f"https://source.unsplash.com/800x1200/?{word}"
    img_data = requests.get(url).content
    with open(f"img{i}.jpg", "wb") as f:
        f.write(img_data)

# STEP 5: Create video with multiple images
os.system("""
ffmpeg -y \
-loop 1 -t 10 -i img0.jpg \
-loop 1 -t 10 -i img1.jpg \
-loop 1 -t 10 -i img2.jpg \
-i voice.mp3 \
-filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]" \
-map "[outv]" -map 3:a \
-vf scale=720:1280 -shortest output.mp4
""")

print("Story video with multiple images created!")
