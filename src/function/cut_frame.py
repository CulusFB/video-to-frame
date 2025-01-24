import cv2
import os
from function import globals as gl
import flet


def frame_cut(frame_to_cut: int, prb: flet.ProgressBar, page: flet.Page):
    for path in range(len(gl.path)):
        my_file = cv2.VideoCapture(gl.path[path])

        new_directory = f'{gl.save_path}/{gl.filename[path].split(".")[0]}'
        if not os.path.isdir(new_directory):
            os.mkdir(new_directory)
        else:
            number_directory = 1
            while os.path.isdir(new_directory):
                new_directory = f'{gl.save_path}/{gl.filename[path].split(".")[0]}{number_directory}'
                number_directory += 1
            os.mkdir(new_directory)
        frame_number = 0
        total_frames = int(my_file.get(cv2.CAP_PROP_FRAME_COUNT))
        i = 0
        while True:
            # sys.stdout.write(f'\r{round((frame_number / total_frames) * 100, 1)} %')  # My progress bar
            frame_number += 1
            prb.value = (frame_number / total_frames)
            page.update()
            ret, frame = my_file.read()
            if not ret:
                break
            if frame_number % frame_to_cut == 0:
                save_path = f'{new_directory}\\{gl.filename[path].split(".")[0]}_{i}.jpg'
                if not cv2.imwrite(save_path, frame):
                    raise Exception("Could not write image")
                i += 1
