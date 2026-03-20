from gtts import gTTS
import os

# Step 1: Script
script = "Amazing facts about space that will shock you!"

# Step 2: Voice
tts = gTTS(script)
tts.save("voice.mp3")

# Step 3: Dummy video (1 image + audio)
os.system("ffmpeg -loop 1 -i image.jpg -i voice.mp3 -c:v libx264 -t 30 -pix_fmt yuv420p output.mp4")

print("Video created!")
