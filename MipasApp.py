from os import path
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.settings import Settings
from kivy.uix.image import Image
from kivy.core.window import Window
import threading
from kivy.uix.screenmanager import ScreenManager, Screen

from gui import CrawlerController
from gui.settingsmenu import settings_json


kivy.require('1.11.0')

Builder.load_file('kv_files/home.kv')
Builder.load_file('kv_files/runtime.kv')
Builder.load_file('kv_files/tabs.kv')
Builder.load_file('kv_files/switchingScreen.kv')

app = None


class ImageButton(ButtonBehavior, Image):
    # might need to do init... and add 's' to settings panel.

    def on_release(self):
        print('pressed')


class Menu(FloatLayout):
    pass


class MipasApp(App):
    counter = NumericProperty(0)
    started = False

    def build(self):
        global app
        Window.size = (1000, 600)
        self.settings_cls = Settings
        self.use_kivy_settings = False
        self.root = Menu()
        app = self
        return self.root

    def build_config(self, config):
        config.setdefaults('preferences', {
            'platform': 'Etsy',
            'stores_name': 'AWESOME-STORE,COOL-STORE',
            'dataset_path': path.expanduser('~'),
            'main_category': 'jewelry',
            'sub_categories': 'necklaces,earrings,bracelets,rings',
            'crawler_option': 'Update Found Stores',
        })

    @staticmethod
    def get_search_option():
        return app.config.get('preferences', 'crawler_option')

    def build_settings(self, settings):
        settings.add_json_panel('Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section, key, value):
        print(config, section, key, value)


class RuntimeScreen(Screen):
    pass


class Home(Screen):
    pass


class MainScreenManager(ScreenManager):

    def __init__(self,**kwargs):
        super(MainScreenManager, self).__init__(**kwargs)
        self.add_widget(Home(name="_home_screen_"))
        self.add_widget(RuntimeScreen(name="_runtime_screen_"))
        self.current = '_home_screen_'

    def switch_to_menu(self):
        self.current = '_home_screen_'
        threading.Thread(target=self.stop_program()).start()

    def switch_to_runtime(self):
        self.current = '_runtime_screen_'
        threading.Thread(target=self.start_program()).start()

    def start_program(self):
        CrawlerController.crawl_by_option(MipasApp.get_search_option())
        print('START')

    def stop_program(self):
        print('STOP')


if __name__ == '__main__':
    MipasApp().run()

