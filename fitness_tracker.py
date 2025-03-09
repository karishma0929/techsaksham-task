import customtkinter as ctk
import csv
import os
from datetime import datetime
from tkinter import messagebox

# Set theme and appearance
ctk.set_appearance_mode("Light")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Try: "green", "dark-blue", "blue"

class FitnessTracker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Personal Fitness Tracker")
        self.geometry("500x600")

        # Variables
        self.steps = ctk.IntVar()
        self.workout_minutes = ctk.IntVar()
        self.goal = ctk.IntVar(value=10000)

        # Title
        ctk.CTkLabel(self, text="Personal Fitness Tracker", font=("Arial", 22, "bold")).pack(pady=20)

        # Inputs
        self.create_input("Steps Walked Today:", self.steps)
        self.create_input("Workout Time (min):", self.workout_minutes)
        self.create_input("Daily Step Goal:", self.goal)

        # Buttons
        ctk.CTkButton(self, text="Calculate & Save", command=self.calculate_and_save).pack(pady=12)
        ctk.CTkButton(self, text="View History", command=self.view_history).pack(pady=5)

        # Result
        self.result_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.result_label.pack(pady=15)

        # History Text Box
        self.history_box = ctk.CTkTextbox(self, width=450, height=200, corner_radius=10)
        self.history_box.pack(pady=10)

    def create_input(self, label, variable):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=5)
        ctk.CTkLabel(frame, text=label, width=200, anchor="w").pack(side="left", padx=10)
        ctk.CTkEntry(frame, textvariable=variable, width=200).pack(side="right", padx=10)

    def calculate_and_save(self):
        steps = self.steps.get()
        workout = self.workout_minutes.get()
        goal = self.goal.get()

        if steps <= 0 or workout < 0 or goal <= 0:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return

        calories = steps * 0.04
        progress = (steps / goal) * 100

        result = f"Calories Burned: {calories:.2f} kcal\nWorkout: {workout} min\nProgress: {progress:.2f}%"
        self.result_label.configure(text=result)
        self.save_data(steps, workout, calories, progress)

    def save_data(self, steps, workout, calories, progress):
        file_exists = os.path.exists("progress_data.csv")
        with open("progress_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Steps", "Workout(min)", "Calories", "Progress(%)"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                steps, workout, f"{calories:.2f}", f"{progress:.2f}"
            ])
        messagebox.showinfo("Saved", "Progress saved successfully!")

    def view_history(self):
        self.history_box.delete("0.0", "end")
        if not os.path.exists("progress_data.csv"):
            self.history_box.insert("end", "No data found.")
            return

        with open("progress_data.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                self.history_box.insert("end", ", ".join(row) + "\n")

# Run app
if __name__ == "__main__":
    app = FitnessTracker()
    app.mainloop()
