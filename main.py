from ast import Invert
from asyncio import run
import code
from codecs import Codec
import copy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from kivy.clock import Clock

# Database setup
def setup_database():
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry TEXT NOT NULL,
            sentiment_score REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

setup_database()
sia = SentimentIntensityAnalyzer()

# Splash Screen
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source="MentalHealthJournalsplash.png"))

class JournalAppScreen(Screen):
    def __init__(self, **kwargs):
        super(JournalAppScreen, self).__init__(**kwargs)
        self.root = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.add_widget(self.root)
        
        # Entry Text Input
        self.entry_input = TextInput(hint_text="Write your journal entry here...", multiline=True, size_hint_y=0.3)
        self.root.add_widget(self.entry_input)
        
        # Add Entry Button
        self.add_button = Button(text="Add Entry", size_hint_y=0.1, on_press=self.add_entry)
        self.root.add_widget(self.add_button)
        
        # Mood Trends Button
        self.trends_button = Button(text="View Mood Trends", size_hint_y=0.1, on_press=self.view_trends)
        self.root.add_widget(self.trends_button)
        
        # Journal Entries Section
        self.entries_label = Label(text="Journal Entries", size_hint_y=0.1)
        self.root.add_widget(self.entries_label)

        self.entries_list = JournalRecycleView(size_hint_y=0.5)
        self.root.add_widget(self.entries_list)
        
        # Refresh Button
        self.refresh_button = Button(text="Refresh Entries", size_hint_y=0.1, on_press=self.refresh_entries)
        self.root.add_widget(self.refresh_button)
        
        self.refresh_entries()  # Initial load of entries

    def add_entry(self, instance):
        text = self.entry_input.text.strip()
        if not text:
            self.show_popup("Input Error", "Please write something before adding!")
            return

        # Analyze sentiment
        score = sia.polarity_scores(text)["compound"]
        if score > 0.05:
            mood = "Positive"
        elif score < -0.05:
            mood = "Negative"
        else:
            mood = "Neutral"

        # Store in database
        conn = sqlite3.connect("journal.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO journal (entry, sentiment_score) VALUES (?, ?)", (text, score))
        conn.commit()
        conn.close()

        # Show feedback
        self.show_popup("Success", f"Entry added with mood: {mood} (Score: {score:.2f})")
        self.entry_input.text = ""  # Clear the input
        self.refresh_entries()

    def refresh_entries(self, instance=None):
        conn = sqlite3.connect("journal.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, entry , sentiment_score FROM journal")
        data = cursor.fetchall()
        conn.close()

        self.entries_list.data = [
            {
                "text": f"[ID: {id_}] {entry} - Mood: {'Positive' if score > 0.05 else 'Negative' if score < -0.05 else 'Neutral'} (Score: {score:.2f})"
            }
            for id_, entry, score in data
        ]

    def view_trends(self, instance):
        # Logic to view mood trends goes here
        print("Viewing mood trends...")  # Placeholder for actual implementation

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()  # Corrected indentation here

class JournalRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self .data = []

class JournalApp(App):
    def build(self):
        self.icon = "MentalHealthJournal.png"  # Set the app icon

        # Screen Manager
        self.sm = ScreenManager()
        self.sm.add_widget(SplashScreen(name="splash"))
        self.sm.add_widget(JournalAppScreen(name="main"))

        # Schedule transition from splash to main
        Clock.schedule_once(self.switch_to_main, 3)  # 3-second delay
        return self.sm

    def switch_to_main(self, dt):
        self.sm.current = "main"

# Run the Kivy app
if __name__ == "__main__":
    JournalApp().run()