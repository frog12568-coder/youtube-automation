from gtts import gTTS
import os
import random

# STEP 1: Story Parts

start = [
    "Ek gareeb bacha tha.",
    "Ek chota ladka tha.",
    "Ek bacha tha jiske paas kuch nahi tha.",
]

middle = [
    "Log uska mazak urate thay.",
    "Sab kehte thay tum kuch nahi kar sakte.",
    "Uske paas paise bhi nahi thay.",
]

ending = [
    "Lekin usne himmat nahi hari aur aaj woh successful hai.",
    "Magar usne mehnat ki aur sabko galat sabit kar diya.",
    "Aur aaj woh lakho logon ke liye inspiration hai.",
]

# STEP 2: Combine story
script = random.choice(start) + " " + random.choice(middle) + " " + random.choice(ending)

print(script)

# STEP 3: Voice
tts = gTTS(script, lang='ur')
tts.save("voice.mp3")

# STEP 4: Video
os.system("ffmpeg -loop 1 -i image.jpg -i voice.mp3 -vf scale=720:1280 -c:v libx264 -t 30 -pix_fmt yuv420p output.mp4")

print("New random story video created!")
