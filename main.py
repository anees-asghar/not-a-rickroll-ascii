import os
import time
from PIL import Image

N_FRAMES = 90
SLEEP_TIME = 0.05 # can be lower for faster machines
FRAME_HEIGHT = 150 # can be higher (200-250) for faster machines
MAX_INTENSITY = 255
ASCII_SCALE = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def get_pixel_matrix(img, height, width):
    pixel_matrix = []

    pixels = img.load()
    for y in range(height):
        row = []
        for x in range(width):
            row.append(pixels[x, y])
        pixel_matrix.append(row)
    
    return pixel_matrix

def get_intensity_matrix(pixel_matrix):
    intensity_matrix = []
    
    for row in pixel_matrix:
        new_row = []
        for pixel in row:
            R, G, B = pixel
            mono = int((R+G+B)/3)
            new_row.append(mono)
        intensity_matrix.append(new_row) 
    
    return intensity_matrix

def get_char_matrix(intensity_matrix):
    char_matrix = []
    
    for row in intensity_matrix:
        new_row = []
        for pixel_intensity in row:
            char = convert_to_char(pixel_intensity)
            new_row.append(char)
        char_matrix.append(new_row)
    
    return char_matrix

def convert_to_char(pixel_intensity):
    global ASCII_SCALE, MAX_INTENSITY
    idx = int(pixel_intensity / MAX_INTENSITY * (len(ASCII_SCALE)-1))
    return ASCII_SCALE[idx]

def get_ascii_frame(frame_name):
    # load file
    filepath = f"images/{frame_name}"
    img = Image.open(filepath)

    # reduce image size
    img.thumbnail((1000, FRAME_HEIGHT))
    width, height = img.size

    # convert image to a pixel matrix of size height x width, where each pixel is 
    # a tuple of rgb values
    pixel_matrix = get_pixel_matrix(img, height, width)

    # transform pixel matrix to represent each pixel using a single number instead of a tuple
    intensity_matrix = get_intensity_matrix(pixel_matrix)

    # create char matrix assigning each pixel an ascii character based on its intensity
    char_matrix = get_char_matrix(intensity_matrix)
    
    # create frame
    frame = ""
    for row in char_matrix:
        # each char in row is multiplied by 3 as the height of a char in terminal is
        # 3 times its width
        row = "".join([c*3 for c in row])
        frame += row + '\n'
    
    return frame

if __name__ == "__main__":
    # load all frames
    print('Loading frames...')
    frames = []
    for i in range(N_FRAMES):
        frame = get_ascii_frame(f"rick-roll-{i}.jpg")
        frames.append(frame)

    # loop over frames to display each frame
    clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    frame_no = 0
    while True:
        os.system(clear_cmd) # clear terminal
        print(frames[frame_no])

        # allow enough time to let the terminal print the whole frame
        time.sleep(SLEEP_TIME)

        # increment frame number, set to 0 if last frame is reached
        frame_no = 0 if frame_no == N_FRAMES-1 else frame_no+1 
