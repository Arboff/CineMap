import os
import sys
from tkinter import Tk, filedialog
from PIL import Image
import cv2
import numpy as np
import shutil
import time

os.system("title CineMap")
os.system("color 4")

print(f"""

 ██████╗██╗███╗   ██╗███████╗███╗   ███╗ █████╗ ██████╗ 
██╔════╝██║████╗  ██║██╔════╝████╗ ████║██╔══██╗██╔══██╗
██║     ██║██╔██╗ ██║█████╗  ██╔████╔██║███████║██████╔╝
██║     ██║██║╚██╗██║██╔══╝  ██║╚██╔╝██║██╔══██║██╔═══╝ 
╚██████╗██║██║ ╚████║███████╗██║ ╚═╝ ██║██║  ██║██║     
 ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     
                                                        

""")



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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_path = os.path.normpath(sys.argv[1])

        # Make the path absolute if it is relative
        if not os.path.isabs(video_path):
            video_path = os.path.abspath(video_path)
    else:
        root = Tk()
        root.withdraw()
        video_path = filedialog.askopenfilename(title="Select a video file",
                                                filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])

        if not video_path:
            print("No file selected. Exiting.")
            sys.exit()

    output_folder = "frames"
    num_frames = 10

    cap = cv2.VideoCapture(video_path)
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap.release()

    extract_frames(video_path, output_folder, num_frames)

    tileplate_output_path = "tileplate.jpg"
    create_image_tileplate(output_folder, tileplate_output_path, video_height, video_width)

    input_image_path = "tileplate.jpg"
    output_image_folder = os.path.dirname(video_path)  # Use the same folder as the video
    add_white_bar_with_text_opencv(input_image_path, output_image_folder)

    os.remove("tileplate.jpg")
    shutil.rmtree('frames')


os.system("cls")

print(f"""

 ██████╗██╗███╗   ██╗███████╗███╗   ███╗ █████╗ ██████╗ 
██╔════╝██║████╗  ██║██╔════╝████╗ ████║██╔══██╗██╔══██╗
██║     ██║██╔██╗ ██║█████╗  ██╔████╔██║███████║██████╔╝
██║     ██║██║╚██╗██║██╔══╝  ██║╚██╔╝██║██╔══██║██╔═══╝ 
╚██████╗██║██║ ╚████║███████╗██║ ╚═╝ ██║██║  ██║██║     
 ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     


""")

print("Finished.")

time.sleep(2)