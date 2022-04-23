import os
import time
from PIL import Image


N_FRAMES = 90 # the number of frames we have available
SLEEP_TIME = 0.05 # how long we want to give the program to print a frame before loading the next frame
FRAME_HEIGHT = 150 # height of a single frame in characters, can be higher (200-250) for faster machines
MAX_INTENSITY = 255 # the max intensity of a single pixel (0-255)
INTENSITY_SCALE = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" # ASCII sorted by the how much background they cover


def get_pixel_matrix(img, height, width):
    """
        Return a pixel matrix of size height x width from the image provided, where each pixel is 
        a tuple of rgb values.
    """
    pixel_matrix = []

    # we extract a PixelAccess object from image which is used for easier access to image pixels
    pixels = img.load()

    for y in range(height):
        row = [pixels[x, y] for x in range(width)]
        pixel_matrix.append(row)
    
    return pixel_matrix


def get_intensity_matrix(pixel_matrix):
    """
        Return an intensity matrix provided a pixel matrix, where the intensity of a pixel is the 
        average of its rgb values.
    """
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
    """
        Return a character matrix provided an intensity matrix, where each pixel is assigned a 
        character from the INTENSITY_SCALE based on its intensity.
    """
    char_matrix = []
    
    for row in intensity_matrix:
        new_row = [convert_to_char(pi) for pi in row]
        char_matrix.append(new_row)
    
    return char_matrix


def convert_to_char(pixel_intensity):
    """
        Return a character from the INTENSITY_SCALE based on the pixel_intensity provided.
    """
    idx = int(pixel_intensity / MAX_INTENSITY * (len(INTENSITY_SCALE)-1))
    return INTENSITY_SCALE[idx]


def get_ascii_frame(frame_name):
    """
        Return a frame as string that can be printed on the terminal provided a frame_name.
    """
    # load file
    filepath = f"images/{frame_name}"
    img = Image.open(filepath)

    # reduce image size
    img.thumbnail((1000, FRAME_HEIGHT))
    width, height = img.size

    # extract pixel matrix from image
    pixel_matrix = get_pixel_matrix(img, height, width)

    # get intensity matrix from pixel_matrix
    intensity_matrix = get_intensity_matrix(pixel_matrix)

    # get character matrix from intensity matrix
    char_matrix = get_char_matrix(intensity_matrix)
    
    # create frame
    frame = ""
    for row in char_matrix:
        # the height of a character on a terminal window is roughly 3 times its width, to offset
        # this we print each character of each row of char_matrix 3 times
        row = "".join([c*3 for c in row])
        frame += row + '\n'
    
    return frame


def main():
    """
        Load all frames then keep looping over them to display each one.
    """
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


if __name__ == "__main__":
    main()
