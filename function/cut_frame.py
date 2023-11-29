import cv2
import os
import sys
from function import globals as gl
import flet
import time


def frame_cut(file: str, frame_to_cut: int, save_dir: str, prb, page):
    myfile = cv2.VideoCapture(gl.path)
    new_directory = f'{save_dir}/{file.split(".")[0]}'
    if not os.path.isdir(new_directory):
        os.mkdir(new_directory)
    else:
        number_directory = 1
        while os.path.isdir(new_directory):
            new_directory = f'{save_dir}/{file.split(".")[0]}{number_directory}'
            number_directory += 1
        os.mkdir(new_directory)
    framenumber = 0
    total_frames = int(myfile.get(cv2.CAP_PROP_FRAME_COUNT))
    i = 0
    while True:
        # sys.stdout.write(f'\r{round((framenumber / total_frames) * 100, 1)} %')  # My progress bar
        framenumber += 1
        prb.value = (framenumber / total_frames)
        page.update()
        ret, frame = myfile.read()
        if not ret:
            break
        if framenumber % frame_to_cut == 0:
            cv2.imwrite(f'{new_directory}/{file.split(".")[0]}_{i}.jpg', frame)
            i += 1
