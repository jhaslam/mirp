import threading

from kivy.clock import mainthread
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from mserial.errors import MSerialError
from mserial.serial import Serial
from kivymd.uix.button import MDRoundFlatButton

class SerialDevice(BoxLayout):
    def __init__(self, device_name: str, serial_driver: Serial, **kwargs):
        super(SerialDevice, self).__init__(**kwargs)

        self.orientation = "vertical"
        self.device_name: str = device_name
        self.serial_driver: Serial = serial_driver

        device_name_label = Label(text=device_name)
        self.add_widget(device_name_label)

        ident_box: BoxLayout = BoxLayout()
        ident_box.orientation = "horizontal"
        self.ident_button: MDRoundFlatButton = MDRoundFlatButton(text='Identify')
        self.ident_button.bind(on_release=self.on_btn_ident_release)
        ident_box.add_widget(self.ident_button)
        self.ident_label: Label = Label()
        ident_box.add_widget(self.ident_label)

        self.add_widget(ident_box)

    def on_btn_ident_release(self, btn):
        self.ident_button.text = "Working"
        self.ident_button.disabled = True
        self.ident_label.text = ""

        threading.Thread(target=self.ident_device_threaded).start()

    def ident_device_threaded(self):
        try:
            ident: str = self.serial_driver.ident_device(self.device_name)
        except MSerialError as err:
            ident: str = err.__class__.__name__
        self.update_ident_label(ident)

    @mainthread
    def update_ident_label(self, text: str):
        self.ident_label.text = text
        self.ident_button.text = "Identify"
        self.ident_button.disabled = False
