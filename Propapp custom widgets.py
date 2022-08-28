from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

Builder.load_file(r'C:\Users\Rotimi Olasehinde\Documents\Kv lang\propcustomwid.kv')

class Wid_grid_container(GridLayout):
    pass

class PressableLabel(Label, ButtonBehavior):
    pass

class PlayGround():
    pass

class AMPressableLbl(PressableLabel):
    pass

class FMPressableLbl(PressableLabel):
    pass

class GMTPressableLbl(PressableLabel):
    pass

class TestwidApp(App):
    def build(self):
        return PlayGround()


if __name__ == '__main__':
    TestwidApp().run()