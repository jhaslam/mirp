import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

kivy.require('2.1.0')


class MainScreen(BoxLayout):
    button_press_count = 0
    label_text = StringProperty("Number of Presses: 0")

    def increment_button_count(self, widget):
        self.button_press_count += 1
        self.label_text = f"Number of Presses: {self.button_press_count}"


class MirpApp(App):

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MirpApp().run()
