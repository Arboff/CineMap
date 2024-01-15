
# CineMap


![App Screenshot](https://iili.io/JYN4kq7.md.png)

Cinemap is a free-to-use software that creates a tilemap of 9 frames from a provided video. No install required. Drag and drop operation. 




## Installation on Linux

```
git clone https://github.com/Arboff/CineMap.git
cd CineMap
python main.py
```

## Installation on Windows

Application comes pre-compiled to Cinemap.exe. Just drag and drop the video file over the exe or double click for GUI usage.

# DEPENDENCIES

```
tkinter
pillow
opencv-python
numpy
```

## Usage & Operation

There are 2 ways of Operation:

### Drag and Drop Method
You will find a compiled .exe. Drag and drop your videofile on it to pipe it in the application. The output image will be saved in the directory of the supplied source video file.

### GUI
Double click on CineMap.exe to be presented with a TKinter GUI windows to locate your video file. The output tilemap will be saved again, to the directory of the source provided.

# Functions and Operations

## Imports

```
import os
import sys
from tkinter import Tk, filedialog
from PIL import Image
import cv2
import numpy as np
import shutil
import time
```

## Exctracting Frames to Create tilemap

```
def extract_frames(video_path, output_folder, num_frames=9):
    cap = cv2.VideoCapture(video_path)
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    indices = [int(i * total_frames / (num_frames - 1)) for i in range(num_frames)]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for index in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ret, frame = cap.read()
        if ret:
            output_path = os.path.join(output_folder, f"frame_{index}.jpg")
            cv2.imwrite(output_path, frame)
            print(f"Frame {index} saved at {output_path}")

    cap.release()
```

## Creating TileMap 

```
def create_image_tileplate(image_folder, output_path, video_height, video_width):
    image_files = sorted([file for file in os.listdir(image_folder) if file.endswith(".jpg")])
    num_rows = 3
    num_cols = 3
    tileplate = Image.new("RGB", (video_width * num_cols, video_height * num_rows))

    for i, image_file in enumerate(image_files):
        image_path = os.path.join(image_folder, image_file)
        img = Image.open(image_path)
        row = i // num_cols
        col = i % num_cols
        tileplate.paste(img, (col * video_width, row * video_height))

    tileplate.save(output_path)
    print(f"Tileplate saved at {output_path}")
```

## Apply Signature and Info bar on top

```
def add_white_bar_with_text_opencv(input_image_path, output_image_folder, creator="github.com/arboff"):
    original_image = cv2.imread(input_image_path)
    bar_height = original_image.shape[0] // 8
    white_bar = np.ones((bar_height, original_image.shape[1], 3), dtype=np.uint8) * 255
    new_image = np.vstack([white_bar, original_image])

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3 if video_height > video_width else 1
    font_thickness = 2

    filename = os.path.splitext(os.path.basename(input_image_path))[0]
    output_filename = os.path.basename(video_path)
    text_line1 = f"Filename: {output_filename}"
    text_line2 = f"Created by {creator}"

    text_size_line1 = cv2.getTextSize(text_line1, font, font_scale, font_thickness)[0]
    text_size_line2 = cv2.getTextSize(text_line2, font, font_scale, font_thickness)[0]

    text_position_line1 = ((new_image.shape[1] - text_size_line1[0]) // 2, bar_height // 2 - text_size_line1[1])
    text_position_line2 = ((new_image.shape[1] - text_size_line2[0]) // 2, bar_height // 2 + text_size_line2[1])

    cv2.putText(new_image, text_line1, text_position_line1, font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)
    cv2.putText(new_image, text_line2, text_position_line2, font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

    # Change the output image filename to match the dragged filename
    output_image_path = os.path.join(output_image_folder, f"{output_filename}_Tiles.jpg")
    cv2.imwrite(output_image_path, new_image)
    print(f"Output image saved at {output_image_path}")
```

## Cleanup
```
os.remove("tileplate.jpg")
shutil.rmtree('frames')
```
## Screenshots



![App Screenshot](https://iili.io/JYNguB1.md.jpg)



![App Screenshot](https://iili.io/JYN4qDQ.md.png)



## Authors

- [@arboff](https://www.github.com/arboff)


## License

[MIT](https://choosealicense.com/licenses/mit/)

