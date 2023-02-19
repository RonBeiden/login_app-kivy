from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import ObjectProperty
import sqlite3



# Define our different screens
class WelcomeScreen(Screen):
    passw = ObjectProperty(None)
    def createBtn(self):
        self.reset()
        sm.current = "create"

    def togglevisibility(self):
        if self.passw.password:
            self.passw.password = False
        elif not self.passw.password:
            self.passw.password = True
class CreateWindow(Screen):
    pass


class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


sm = WindowManager()


class MainApp(MDApp):
    def build(self):
        self.password_visible = False
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        # Create Database Or Connect To One
        conn = sqlite3.connect('users.db')

        # Create A Cursor
        c = conn.cursor()

        # Create A Table
        c.execute("""CREATE TABLE if not exists users(
                     username text,
                     password text)
                 """)

        # Commit our changes
        conn.commit()

        # Close our connection
        conn.close()
        return Builder.load_file('login.kv')

    def logger(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        data = c.fetchone()
        if data:
            self.on_release()
        else:
            popup = Popup(title='Login Failed', content=Label(text='Invalid username or password'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
        conn.close()

    def create(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        data = c.fetchone()
        if len(password) == 0 or len(username) == 0:
            popup = Popup(title='Create Account Failed', content=Label(text='Invalid password or username'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
        elif data:
            popup = Popup(title='Create Account Failed', content=Label(text='Username already taken'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            self.clear()
            self.on_release()
        conn.close()

    def clear(self):
        self.root.children[0].ids.user.text = ""
        self.root.children[0].ids.password.text = ""
        self.root.children[0].ids.welcome_label.text = "WELCOME"

    def on_release(self):
        self.root.current = "second"

if __name__ == "__main__":
    MainApp().run()
