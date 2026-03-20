import os
import random
import requests
import time
from gtts import gTTS

print(">> Starting Urdu Story Video Script...")

# ==========================================
# STEP 1: Story Generation (Urdu)
# ==========================================
start_sentences = [
    "Ek gareeb bacha tha",
    "Ek chota ladka tha",
    "Ek bacha tha jiske paas kuch nahi tha"
]

middle_sentences = [
    "log uska mazak urate thay",
    "sab kehte thay tum kuch nahi kar sakte",
    "uske paas paise bhi nahi thay"
]

ending_sentences = [
    "lekin usne himmat nahi hari",
    "magar usne mehnat ki",
    "aur ek din sab kuch badal gaya"
]

# Combine random parts to create a simple story
script = f"{random.choice(start_sentences)}. {random.choice(middle_sentences)}. {random.choice(ending_sentences)}"
print(f"[{time.strftime('%H:%M:%S')}] Story generated: {script}")

# ==========================================
# STEP 2: Generate Voiceover (gTTS)
# ==========================================
voice_filename = "voice.mp3"
print(f"[{time.strftime('%H:%M:%S')}] Generating voiceover (lang='ur')...")
try:
    tts = gTTS(text=script, lang='ur')
    tts.save(voice_filename)
    if os.path.exists(voice_filename):
        print(f"[{time.strftime('%H:%M:%S')}] Voiceover saved as {voice_filename}")
    else:
        raise FileNotFoundError("Voiceover file not created.")
except Exception as e:
    print(f"!! Error generating voiceover: {e}")
    exit(1) # Stop script if voice generation fails

# ==========================================
# STEP 3: Optimized Image Downloading
# ==========================================
keywords = ["sad child", "struggle", "success"]
downloaded_images = []

# Using direct image URLs as keywords/tags on source.unsplash.com are deprecated
# We use specific high-quality image IDs that fit the theme
image_ids = [
    "1511367461989-f85a21fda167", # generic sad/neutral
    "1594114131102-3c8c704f5e04", # struggle/darker
    "1622919932179-c5c7d8120e36"  # success/light
]

for i, img_id in enumerate(image_ids):
    filename = f"img{i}.jpg"
    print(f"[{time.strftime('%H:%M:%S')}] Downloading image {i+1}/{len(image_ids)}...")
    
    # Requesting a specific size suitable for portrait videos
    url = f"https://images.unsplash.com/photo-{img_id}?q=80&w=720&h=1280&auto=format&fit=crop"
    
    try:
        response = requests.get(url, stream=True, timeout=10) # 10-second timeout
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            
            # Basic validation
            if os.path.getsize(filename) > 1024: # Must be larger than 1KB
                print(f"[{time.strftime('%H:%M:%S')}] Image {i+1} saved as {filename}")
                downloaded_images.append(filename)
            else:
                raise ValueError("Downloaded file is empty or too small.")
        else:
            raise requests.exceptions.HTTPError(f"HTTP Error: {response.status_code}")

    except Exception as e:
        print(f"!! Error downloading image {i+1}: {e}")
        # Optionally, download a placeholder or continue with fewer images.
        # We will stop here to avoid creating a corrupted video.
        print("!! Video creation cannot continue safely. Stopping.")
        exit(1)

# Ensure we have all images before proceeding
if len(downloaded_images) != 3:
    print("!! Error: Not all images were downloaded successfully.")
    exit(1)

# ==========================================
# STEP 4: Stable FFmpeg Video Creation
# ==========================================
# The complex filter approach is generally more reliable on headless servers like GitHub Actions
# It ensures all inputs are concatenated and mapped correctly.

# We define the input flags, filter logic, and output flags separately for clarity.
input_args = (
    "-y " # Overwrite output if it exists
    "-loop 1 -t 6 -i img0.jpg " # 6 seconds for each image
    "-loop 1 -t 6 -i img1.jpg "
    "-loop 1 -t 6 -i img2.jpg "
    f"-i {voice_filename} "
)

# Concat images, scale them to portrait aspect, set name as [v], don't process audio from images [a=0]
filter_args = (
    "-filter_complex \"[0:v][1:v][2:v]concat=n=3:v=1:a=0,scale=720:1280[v]\" "
)

# Map the final video and the audio stream (input index 3), use standard codecs, finish with audio duration
output_args = (
    "-map \"[v]\" -map 3:a -c:v libx264 -c:a aac -b:a 128k -pix_fmt yuv420p -shortest output.mp4"
)

full_ffmpeg_command = f"ffmpeg {input_args}{filter_args}{output_args}"

print(f"[{time.strftime('%H:%M:%S')}] Starting video rendering (this may take up to 20 mins)...")
# Note: In production, you'd use subprocess for better control, but os.system is fine for this example.
os.system(full_ffmpeg_command)

# Verification
if os.path.exists("output.mp4") and os.path.getsize("output.mp4") > 1024: # Check existence and size > 1KB
    print(f"[{time.strftime('%H:%M:%S')}] SUCCESS: Video created as 'output.mp4'!")
else:
    print(f"[{time.strftime('%H:%M:%S')}] FAILURE: Video file was not created properly.")
    exit(1)

# Optional: Cleanup files
# os.remove(voice_filename)
# for img in downloaded_images: os.remove(img)
# print("Cleaned up temporary files.")

print(">> Script finished.")
