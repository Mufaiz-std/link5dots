import urllib.request
import wave
import math
import struct
import os

# Download fonts
font_dir = "assets/fonts"
os.makedirs(font_dir, exist_ok=True)
urllib.request.urlretrieve("https://github.com/googlefonts/RobotoMono/raw/main/fonts/ttf/RobotoMono-Regular.ttf", f"{font_dir}/RobotoMono-Regular.ttf")
urllib.request.urlretrieve("https://github.com/googlefonts/RobotoMono/raw/main/fonts/ttf/RobotoMono-Bold.ttf", f"{font_dir}/RobotoMono-Bold.ttf")

# Generate tak sound
sound_dir = "assets/sounds"
os.makedirs(sound_dir, exist_ok=True)
sound_path = f"{sound_dir}/tak.wav"

sample_rate = 44100
duration = 0.05 # very short tick
freq = 800

with wave.open(sound_path, 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    
    num_samples = int(sample_rate * duration)
    for i in range(num_samples):
        # exponential decay
        envelope = math.exp(-i / (sample_rate * 0.01))
        # mix some noise and a sine wave for a wooden tak sound
        val = int(envelope * 32767 * math.sin(2 * math.pi * freq * (i / sample_rate)))
        if val > 32767: val = 32767
        if val < -32768: val = -32768
        data = struct.pack('<h', val)
        wav_file.writeframesraw(data)
