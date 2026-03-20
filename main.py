from gtts import gTTS
import os
import random
import requests

print("Starting script...")

# STEP 1: Story parts
start = [
    "Ek gareeb bacha tha",
    "Ek chota ladka tha",
    "Ek bacha tha jiske paas kuch nahi tha"
]

middle = [
    "log uska mazak urate thay",
    "sab kehte thay tum kuch nahi kar sakte",
    "uske paas paise bhi nahi thay"
]

ending = [
    "lekin usne himmat nahi hari",
    "magar usne mehnat ki",
    "aur ek din sab kuch badal gaya"
]

# Combine story
script = random.choice(start) + ". " + random.choice(middle) + ". " + random.choice(ending)
print("Story:", script)

# STEP 2: Voice
tts = gTTS(script, lang='ur')
tts.save("voice.mp3")

# STEP 3: Download images
keywords = ["sad child", "struggle", "success"]

for i, word in enumerate(keywords):
    url = f"https://source.unsplash.com/720x1280/?{word}"
    img_data = requests.get(url).content
    with open(f"img{i}.jpg", "wb") as f:
        f.write(img_data)

# STEP 4: Create video (simple & working)
os.system("ffmpeg -y -loop 1 -t 10 -i img0.jpg -loop 1 -t 10 -i img1.jpg -loop 1 -t 10 -i img2.jpg -i voice.mp3 -vf scale=720:1280 -c:v libx264 -pix_fmt yuv420p -shortest output.mp4")

print("Video created successfully!")
