import kivy
import threading

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager, Screen

import mserial.serial
import ui.widgets

kivy.require('2.1.0')


class MainScreen(Screen):
    pass


class SerialConfigScreen(Screen):
    def __init__(self, **kwargs):
        self.read_thread = None
        self.port_thread_lock = threading.Lock()
        super(SerialConfigScreen, self).__init__(**kwargs)

    def on_btn_list_devices_release(self):
        device_list: BoxLayout = self.ids.device_list
        device_list.clear_widgets()

        serial: mserial.serial.Serial = MDApp.get_running_app().serial_driver
        device_name_list = serial.device_names()

        for device_name in device_name_list:
            serial_device_widget = ui.widgets.SerialDevice(
                device_name=device_name,
                serial_driver=serial_driver,
                size_hint_y=None, height='100dp')
            device_list.add_widget(serial_device_widget)


class WindowManager(ScreenManager):
    pass


class MirpApp(MDApp):
    def __init__(self, serial_driver, **kwargs):
        super().__init__(**kwargs)
        self.serial_driver = serial_driver

    def build(self):
        return Builder.load_file("ui/mainlayout.kv")


def position_window():
    # 9 x 16 Aspect ratio for phones
    if platform != 'android':
        Window.size = (dp(450), dp(800))
        Window.top = dp(50)


if __name__ == '__main__':
    position_window()

    if platform == 'android':
        serial_driver = mserial.serial.AndroidSerial()
    else:
        serial_driver = mserial.serial.DesktopSerial()

    MirpApp(serial_driver).run()
