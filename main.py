from pydub import AudioSegment
import numpy as np
from PIL import Image, ImageDraw

# Audio laden (Mono ist einfacher für die Visualisierung)
audio = AudioSegment.from_file("file.mp3").set_channels(1)
samples = np.array(audio.get_array_of_samples())

# Bildgröße und Parameter
width = 1500
height = 400
img = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(img)

# Normieren auf Bereich [-1, 1]
samples = samples / np.max(np.abs(samples))

# Schrittweite pro Pixelspalte
step = len(samples) // width
center_y = height // 2

for x in range(width):
    segment = samples[x * step:(x + 1) * step]
    if len(segment) == 0:
        continue
    peak = int(np.max(segment) * (height // 2))
    trough = int(np.min(segment) * (height // 2))
    draw.line([(x, center_y - peak), (x, center_y - trough)], fill="black")

# Speichern
img.save("waveform1.png")
print("Wellenform gespeichert als waveform.png")
