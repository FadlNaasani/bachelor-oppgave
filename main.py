from kivy import app
from kivy.uix import layout
from kivy.uix.stacklayout import StackLayout
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
import cv2
from kivy.uix.button import Button

from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import easyocr
from tkinter import Image

import cv2
from easyocr import easyocr
# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)
from kivy.uix.image import Image

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.uix.stacklayout import StackLayout

import numpy as np
KV = '''

#: import Window kivy.core.window.Window

ScrollView:
    size_hint: (1,None)
    size: (Window.width, Window.height)
    MyLayout:

'''

class MainApp(MDApp):

    def build(self):
        layout = ScrollView()

        self.image = Image()
        layout.add_widget(self.image)




        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)
        return layout

    def load_video(self, *args):
        ret, frame = self.capture.read()
        # frame
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture


    def imageToText(self, *args):

        print("hei")





if __name__ == '__main__':
    MainApp().run()