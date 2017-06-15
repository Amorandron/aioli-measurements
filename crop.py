import cv2
from frame import Frame

# Global variables
current_crop = None
highest_line = None
lowest_line = None


def recalibrate():
    highest_line = None
    lowest_line = None


def crop_image(image, lines, tray_size):
    """ Takes in an image, Hough-Lines, and the width of the tray and returns a cropped image """
    global current_crop
    global highest_line
    global lowest_line

    image_h, image_w, _ = image.frame.shape

    if current_crop is None:
        current_crop = image.frame

    if highest_line is None and lowest_line is None:
        highest_line = [0, image_h / 2, image_w, image_h / 2]
        lowest_line = highest_line

    for x in lines:
        for x1, y1, x2, y2 in x:
            line = [0, y1, image_w, y2]

            if lowest_line[1] > y1 and lowest_line[3] > y2:
                lowest_line = line
            elif highest_line[1] < y1 and highest_line[3] < y2:
                highest_line = line

    top_crop = (highest_line[1] + highest_line[3]) / 2 - tray_size
    bottom_crop = (lowest_line[1] + lowest_line[3]) / 2 + tray_size

    return Frame(image.frame[bottom_crop:top_crop, 0:])