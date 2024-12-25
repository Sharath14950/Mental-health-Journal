import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from modules import db  # Import db module
from datetime import datetime
import matplotlib.pyplot as plt

# Ensure the project directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

class QuestionScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Mental health questions
        self.questions = [
            "How are you feeling today? (0 = Terrible, 10 = Great)",
            "How would you rate your level of serenity today? (0 = Poorly, 10 = Very well)",
            "How well did you sleep last night? (0 = Poorly, 10 = Very well)",
            "How productive were you today? (0 = Not at all, 10 = Extremely productive)",
            "How much did you enjoy your day today? (0 = Not at all, 10 = Very much)"
        ]

        # Initialize state
        self.current_question_index = 0
        self.answers = []

        # Create UI components
        self.question_label = Label(
            text=self.questions[self.current_question_index],
            size_hint=(1, 0.3),
            font_size='20sp',
            halign='center',
            valign='middle'
        )
        self.question_label.bind(size=self.question_label.setter('text_size'))  # Ensure proper wrapping
        self.add_widget(self.question_label)

        # Slider and value display
        self.slider = Slider(min=0, max=10, value=5, size_hint=(1, 0.2), step=1)
        self.slider.bind(value=self.update_slider_value)

        self.slider_value_label = Label(
            text=f"Selected value: {int(self.slider.value)}",
            size_hint=(1, 0.1),
            font_size='16sp',
            halign='center',
            valign='middle'
        )
        self.slider_value_label.bind(size=self.slider_value_label.setter('text_size'))  # Ensure proper wrapping

        self.add_widget(self.slider)
        self.add_widget(self.slider_value_label)

        self.next_button = Button(text="Next", size_hint=(1, 0.2), font_size='18sp')
        self.next_button.bind(on_press=self.handle_next)
        self.add_widget(self.next_button)

    def update_slider_value(self, instance, value):
        """
        Update the slider value label dynamically as the user moves the slider.
        """
        self.slider_value_label.text = f"Selected value: {int(value)}"

    def handle_next(self, instance):
        """
        Handle clicking the Next button. Either navigate to the next question or finish the survey.
        """
        # Store the answer
        self.answers.append(self.slider.value)

        if self.current_question_index < len(self.questions) - 1:
            # Update to the next question
            self.current_question_index += 1
            self.question_label.text = self.questions[self.current_question_index]
            self.slider.value = 5  # Reset slider
        else:
            # End of questions: calculate average and save
            self.calculate_average()

    def calculate_average(self):
        """
        Calculate the average score and save the data to the database.
        """
        average_score = sum(self.answers) / len(self.answers)
        self.save_to_database(average_score)
        self.show_results_popup(average_score)
        self.show_graph()

    def save_to_database(self, average):
        """
        Save the user's responses to the database.
        """
        db.create_table()  # Ensure the table exists
        now = datetime.now()
        date_string = now.strftime('%Y-%m-%d')
        db.add_entry(
            date=date_string,
            feeling=self.answers[0],
            serenity=self.answers[1],
            sleep=self.answers[2],
            productivity=self.answers[3],
            enjoyment=self.answers[4],
            average=average
        )

    def show_results_popup(self, average):
        """
        Show a popup displaying the user's average score.
        """
        popup_content = Label(
            text=f"Your average mental health score is {average:.1f}",
            font_size='18sp',
            halign='center',
            valign='middle'
        )
        popup_content.bind(size=popup_content.setter('text_size'))  # Ensure proper wrapping

        popup = Popup(
            title="Results",
            content=popup_content,
            size_hint=(0.8, 0.5)
        )
        popup.open()

    def show_graph(self):
        """
        Generate and display a graph based on the user's responses.
        """
        categories = [
            "Feeling",
            "Serenity",
            "Sleep",
            "Productivity",
            "Enjoyment"
        ]

        plt.figure(figsize=(10, 5))
        plt.bar(categories, self.answers, color='skyblue')
        plt.ylim(0, 10)
        plt.title("Mental Health Responses")
        plt.xlabel("Categories")
        plt.ylabel("Scores (0-10)")
        plt.tight_layout()
        plt.show()


class MentalHealthApp(App):
    def build(self):
        """
        Build the Kivy app's root widget.
        """
        return QuestionScreen()


if __name__ == '__main__':
    MentalHealthApp().run()
