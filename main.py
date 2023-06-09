import numpy
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
import cv2
from kivy.uix.image import Image
from kivy.graphics.texture import Texture, platform
from kivy.clock import Clock
import easyocr
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.CAMERA,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE])



class MainApp(MDApp):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical')
        self.layout = MDBoxLayout(orientation='vertical')
        self.layout1 = StackLayout(size_hint_y=None)
        scrollView = ScrollView(size_hint=(1, None),
         size=(75, 250), do_scroll_y= True,do_scroll_x=True)
        self.start_button = MDRaisedButton(
            text="Start again",
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(.5, .1))
        self.capture_button = MDRaisedButton(
            text="Image cropping",
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint = (.5, .1))
        self.get_text_button = MDRaisedButton(
            text="Extract text",
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint = (.5, .1)
        )
        self.start_button.bind(on_press=self.start_again)
        self.capture_button.bind(on_press=self.get_images)
        self.get_text_button.bind(on_press=self.get_text)

        self.image = Image()
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)
        scrollView.add_widget(self.layout1)
        self.layout.add_widget(self.image)
        self.main_layout.add_widget(self.layout)
        self.main_layout.add_widget(scrollView)
        self.main_layout.add_widget(self.capture_button)
        self.main_layout.add_widget(self.get_text_button)
        return self.main_layout

    def load_video(self, *args):
        ret, frame = self.capture.read()
        # frame
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1],
                                       frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture
    def start_again(self, *args):
        self.layout1.clear_widgets()
        self.main_layout.remove_widget(self.start_button)
        self.main_layout.add_widget(self.capture_button)
        self.main_layout.add_widget(self.get_text_button)
    def get_text(self, *args):
        if self.layout:
            self.layout1.clear_widgets()
        self.main_layout.remove_widget(self.capture_button)
        self.main_layout.remove_widget(self.get_text_button)

        reader = easyocr.Reader(['no','en'], gpu=False)
        result = reader.readtext(self.image_frame, detail=0,
                                 ycenter_ths=0.2, paragraph=False, width_ths=0.1)
        if not result:
            self.layout1.add_widget(MDLabel(text='Finner ikke tekst på bildet!'))
        text_res= ' '.join([str(elem) for elem in result])
        res1= MDLabel(text=f'{text_res}',size_hint_y= None, padding= (10, 10))
        self.layout1.add_widget(res1)
        self.main_layout.add_widget(self.start_button)
    def get_images (self, *args):
        if self.layout:
            self.layout1.clear_widgets()
        #self.layout.clear_widgets()
        self.main_layout.remove_widget(self.capture_button)
        self.main_layout.remove_widget(self.get_text_button)
        # bedre om du har gpu og raaskere
        reader = easyocr.Reader(['no','en'], gpu=False)
        result = reader.readtext(self.image_frame,
                                 detail=1, ycenter_ths=0.2,
                                 paragraph=False, width_ths=0.1) # Matrise
        if not result:
            self.layout1.add_widget(MDLabel
                                    (text='Finner ikke tekst på bildet!'))

        for text in result:
            p1 = text[0][0]
            p3 = text[0][2]
            y1 = p1[1]
            y2 = p3[1]
            x1 = p1[0]
            x2 = p3[0]
            if type(y1) !=numpy.int64:
                self.layout1.add_widget(MDLabel
                            (text='teksten er veldig skeiv!!'))
                break
            else:
                croppeed = self.image_frame[(y1):(y2),(x1):(x2)]
                buffer = cv2.flip(croppeed, 0).tobytes()
                texture = Texture.create(size=(croppeed.shape[1],croppeed.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                imT = Image(size_hint_y=None, size_hint_x=None)
                imT.texture = texture
                self.layout1.add_widget(imT)
        self.main_layout.add_widget(self.start_button)


if __name__ == '__main__':
    MainApp().run()