import time

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import uic
import pandas as pd

import cv2
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys

## This method borrowed from this tutorial by github user docPhil99:
## https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self, video_frames,  *args, **kwargs):
        super(MainWindow, self).__init__(*args, ** kwargs)
        self.setWindowTitle("Video Log Viewer")
        self.setFixedWidth(800)
        #uic.loadUi('main_window.ui', self)
        self.vid_pos = 0
        self.video_frames = video_frames

        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        slider_widget = QSlider(Qt.Orientation.Horizontal)
        slider_widget.setMinimum(0)
        slider_widget.setMaximum(len(video_frames) - 1)
        slider_widget.sliderMoved.connect(self.slider_position)



        self.video_widget = QLabel("Video")
        firstFrame = video_frames[0]
        self.video_widget.setPixmap(QPixmap(self.convert_cv_qt(self.video_frames[0]).scaledToWidth(400)))

        self.df = pd.read_csv("fake_data_logs/fake_encoder_data.csv")
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot(self.df["time_stamp"], self.df["encoder_value"])
        self.sc.axes.set_xlim([-10, 10])




        ##layout adding
        layout_left.addWidget(self.video_widget)
        layout_left.addWidget(slider_widget)


        layout_right.addWidget(self.sc)

        layout = QHBoxLayout()
        layout.addLayout(layout_left)
        layout.addLayout(layout_right)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def slider_position(self, p):
        print("vid position", p)
        self.vid_pos = p
        cur_frame = self.video_frames[self.vid_pos]
        frame_pix_map = QPixmap(self.convert_cv_qt(cur_frame)).scaledToWidth(400)
        self.video_widget.setPixmap(frame_pix_map)
        self.sc.axes.clear()
        self.sc.axes.set_xlim(self.vid_pos - 10, self.vid_pos + 10)
        self.sc.axes.plot(self.df["time_stamp"], self.df["encoder_value"])
        self.sc.draw()

    ## This method adapoted from this tutorial by github user docPhil99:
    ## https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)














def main():
    print("Hello world")

    capture = cv2.VideoCapture("videos/test_robot_video.mp4")
    chec, vid = capture.read()
    frame_list = []
    check = True
    frame_count = 0
    while(check == True):
        check, vid = capture.read()
        frame_list.append(vid)
        frame_count += 1
    capture.release()


    # release method of video
    # object clean the input video



    # last value in the frame_list is None
    # because when video reaches to the end
    # then false value store in check variable
    # and None value is store in vide variable.

    # removing the last value from the
    # frame_list by using pop method of List
    frame_list.pop()






    app = QApplication([])

    window = MainWindow(frame_list)
    window.show()

    app.exec()




if __name__ == "__main__":
    main()