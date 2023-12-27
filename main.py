import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import random
import time

class QuizApp:
    def __init__(self, root, quiz_data):
        # Initialize the QuizApp
        self.root = root
        self.root.title("WizQuiz")
        self.root.geometry("600x500")
        self.style = Style(theme="darkly")
        self.style.configure("TLabel", font=("Arial", 18), foreground="white")
        self.style.configure("TButton", font=("Arial", 14), foreground="white", background="#343a40", width=15)  # Button width set to 15

        # Shuffle the quiz data to randomize question order
        random.shuffle(quiz_data)
        self.quiz_data = quiz_data
        self.num_choices = len(quiz_data[0]["choices"])
        self.current_question = 0
        self.score = 0
        self.timer_start_time = 0

        # Create the GUI elements
        self.create_gui()
        self.show_question()

    def create_gui(self):
        # Create the title label
        self.create_title_label()
        # Create the question label
        self.create_question_label()
        # Create the choice buttons
        self.create_choice_buttons()
        # Create the feedback label
        self.create_feedback_label()
        # Create the score label
        self.create_score_label()
        # Create the next button
        self.create_next_button()
        # Create the timer label
        self.create_timer_label()

    def create_title_label(self):
        # Create and configure the title label
        title_label = ttk.Label(
            self.root,
            text="🌟 WizQuiz 🌟",
            font=("Helvetica", 24, "bold"),
            foreground="#FFD700"  # Gold color
        )
        title_label.pack(pady=10)

    def create_question_label(self):
        # Create and configure the question label
        self.qs_label = ttk.Label(
            self.root,
            anchor="center",
            wraplength=500,
            padding=10,
            background="#343a40",  # Dark background color
        )
        self.qs_label.pack(pady=10)

    def create_choice_buttons(self):
        # Create and configure the choice buttons
        self.choice_btns = []
        for i in range(self.num_choices):
            button = ttk.Button(
                self.root,
                command=lambda i=i: self.check_answer(i),
                style="TButton"  # Use the configured style for buttons
            )
            button.pack(pady=5, ipadx=10, ipady=5)
            self.choice_btns.append(button)

    def create_feedback_label(self):
        # Create and configure the feedback label
        self.feedback_label = ttk.Label(
            self.root,
            anchor="center",
            padding=10,
            foreground="green"  # Feedback label color
        )
        self.feedback_label.pack(pady=10)

    def create_score_label(self):
        # Create and configure the score label
        self.score_label = ttk.Label(
            self.root,
            text=f"Score: {self.score}/{len(self.quiz_data)}",
            anchor="center",
            padding=10,
            foreground="white"  # Score label color
        )
        self.score_label.pack(pady=10)

    def create_next_button(self):
        # Create and configure the next button
        self.next_btn = ttk.Button(
            self.root,
            text="Next",
            command=self.next_question,
            state="disabled",
            style="TButton.Next"  # Use the configured style for Next button
        )
        self.next_btn.pack(pady=10, ipadx=10, ipady=5)

    def create_timer_label(self):
        # Create and configure the timer label
        self.timer_label = ttk.Label(
            self.root,
            text="Time left: 15",
            anchor="center",
            padding=10,
            foreground="white"  # Timer label color
        )
        self.timer_label.pack(pady=10)

    def show_question(self):
        # Display the current question
        self.timer_start_time = time.time()
        question = self.quiz_data[self.current_question]
        self.qs_label.config(text=question["question"])

        # Display the choices on the buttons
        choices = question["choices"]
        for i in range(self.num_choices):
            self.choice_btns[i].config(text=choices[i], state="normal")

        # Clear the feedback label and disable the next button
        self.feedback_label.config(text="")
        self.next_btn.config(state="disabled")

        # Update the timer
        self.update_timer()

    def update_timer(self):
        # Update the timer label with remaining time
        remaining_time = max(0, 15 - (time.time() - self.timer_start_time))
        self.timer_label.config(text=f"Time left: {int(remaining_time)}")

        if remaining_time > 0:
            # Schedule the update_timer method to be called after 100 milliseconds
            self.root.after(100, self.update_timer)
        else:
            # If time runs out, call the timeout method
            self.timeout()

    def check_answer(self, choice):
        # Check the selected answer and provide feedback
        question = self.quiz_data[self.current_question]
        selected_choice = question["choices"][choice]

        elapsed_time = time.time() - self.timer_start_time

        if selected_choice == question["answer"]:
            # Update the score and display correct feedback
            self.score += 1
            self.feedback_label.config(
                text=f"Correct! Time taken: {elapsed_time:.2f} seconds",
                foreground="green"
            )
        else:
            # Display incorrect feedback with the correct answer
            self.feedback_label.config(
                text=f"Incorrect! Correct answer: {question['answer']} Time taken: {elapsed_time:.2f} seconds",
                foreground="red"
            )

        # Disable choice buttons and enable the next button
        for button in self.choice_btns:
            button.config(state="disabled")
        self.next_btn.config(state="normal")

        # Update the score label
        self.score_label.config(text=f"Score: {self.score}/{len(self.quiz_data)}")

    def next_question(self):
        # Move to the next question
        self.current_question += 1

        if self.current_question < len(self.quiz_data):
            # If there are more questions, show the next question
            self.show_question()
        else:
            # If all questions have been answered, display the final score
            self.show_final_score()

    def show_final_score(self):
        # Display the final score in a messagebox
        messagebox.showinfo(
            "Quiz Completed",
            f"Quiz Completed! Final score: {self.score}/{len(self.quiz_data)}"
        )
        # Close the application window
        self.root.destroy()

    def timeout(self):
        # Handle timeout by displaying the correct answer
        self.feedback_label.config(text="Time's up! Correct answer: {}".format(self.quiz_data[self.current_question]["answer"]))
        # Disable choice buttons and enable the next button
        for button in self.choice_btns:
            button.config(state="disabled")
        self.next_btn.config(state="normal")

if __name__ == "__main__":
    # Define custom quiz data for a Harry Potter quiz
    custom_quiz_data = [
    {
        "question": "Who is known as the Half-Blood Prince?",
        "choices": ["Sirius Black", "Remus Lupin", "Severus Snape", "Rubeus Hagrid"],
        "answer": "Severus Snape"
    },
    {
        "question": "Who is the headmaster of Hogwarts when Harry first arrives?",
        "choices": [ "Severus Snape","Albus Dumbledore", "Minerva McGonagall", "Gellert Grindelwald"],
        "answer": "Albus Dumbledore"
    },
    {
        "question": "What is the name of Harry's owl?",
        "choices": ["Hedwig", "Errol", "Crookshanks", "Fawkes"],
        "answer": "Hedwig"
    },
    {
        "question": "Which house does Harry belong to at Hogwarts?",
        "choices": [ "Slytherin", "Hufflepuff", "Ravenclaw", "Gryffindor" ],
        "answer": "Gryffindor"
    },
    {
        "question": "What is the primary mode of transportation for wizards and witches?",
        "choices": ["Broomsticks", "Thestrals", "Apparition", "Portkeys"],
        "answer": "Broomsticks"
    }
    ]

    # Create the main window and start the application
    root = tk.Tk()
    app = QuizApp(root, custom_quiz_data)
    # Define a new style for the Next button and set button width
    root.style = Style(theme="darkly")
    root.style.configure("TButton.Next", font=("Arial", 14), foreground="white", background="#007BFF", width=15)  # Blue background color
    root.mainloop()
