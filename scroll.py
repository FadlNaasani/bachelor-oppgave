import kivy
from easyocr import easyocr
from kivy import app
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.app import App
from tkinter import Image
from kivy.uix.image import Image
from kivy.clock import Clock
import cv2
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton





KV = '''

#: import Window kivy.core.window.Window

ScrollView:
    size_hint: (1,None)
    size: (Window.width, Window.height)
    size_hint_y :None
    MyLayout:

'''


class MyLayout(StackLayout):

    def __init__(self,**kwargs):
        super(MyLayout,self).__init__(**kwargs)

        self.width= self.minimum_width

        self.bind(minimum_height=self.setter('height'))
        self.save_img_button = Button(
            text="Trkk Her!",
            size_hint=(None, None)
        )
        self.save_img_button.bind(on_press=self.imageToText)

        self.add_widget(self.save_img_button)

        self.image = Image()
        self.add_widget(self.image)

        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)

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
        self.remove_widget(self.save_img_button)
        self.remove_widget(self.image)
        self.size_hint_y = (None)
        img= self.image_frame
        reader = easyocr.Reader(['en'], gpu=False)  # bedre om du har gpu og raaskere
        result = reader.readtext(img, detail=1, ycenter_ths=0.2, paragraph=False, width_ths=0.1)  # Matrise
        i = 0
        for text in result:
            i = 1 + i
            p1 = text[0][0]
            p2 = text[0][2]
            y1 = p1[1]
            y2 = p2[1]
            x1 = p1[0]
            x2 = p2[0]
            # cpx = text[0][2]
            detectedText = text[1]
            croppeed = img[y1:y2, x1:x2]
            cv2.imwrite("IMG_{}.png".format(i), croppeed)
            #self.pixels = croppeed.pixels
            btn = Image(source="IMG_{}.png".format(i), size_hint_y=None, size_hint_x=None)
            self.add_widget(btn)



class MyApp(App):

    def build(self):
        return Builder.load_string(KV)


MyApp().run()