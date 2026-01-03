import tkinter as tk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import winsound


class Timer:
    # this makes the timer part of the app
    def __init__(self, window, projector):
        self.window = window
        self.projector = projector  # this allows the timer to talk to the study projector
        self.time_left = 0
        self.is_running = False
        self.end_time = None

        # this loads the total time studied today from a file so progress is not lost
        file = open("study_time.txt", "r")
        self.today_seconds = int(file.read())
        file.close()

        self.session_seconds = 0

        # display for the timer
        self.timer_label = tk.Label(self.window, text="00:00", font=("Arial", 30))
        self.timer_label.pack(pady=10)

        # this is where the user inputs their time
        self.time_entry = tk.Entry(self.window, font=("Arial", 18))
        self.time_entry.pack(pady=10)

        # frame for start and stop buttons so they’re side by side
        self.button_frame = tk.Frame(self.window, bg="white")
        self.button_frame.pack(pady=10)

        # start button
        self.start_button = tk.Button(self.button_frame, text="Start", font=("Arial", 18), command=self.start_timer)
        self.start_button.pack(side="left", padx=10)

        # stop button
        self.stop_button = tk.Button(self.button_frame, text="Stop", font=("Arial", 18), command=self.stop_timer)
        self.stop_button.pack(side="left", padx=10)

    # T is is the function that starts the timer and checs if its running
    def start_timer(self):
        user_input = self.time_entry.get()
        self.session_seconds = int(user_input) * 60
        self.time_left = self.session_seconds
        self.is_running = True
        self.end_time = datetime.now() + timedelta(seconds=self.time_left)
        self.count_down()

        # datetime library gives a more accurate countdown
        self.end_time = datetime.now() + timedelta(seconds=self.time_left)
        self.count_down()

    def stop_timer(self): #
        self.is_running = False
        self.timer_label.config(text="Stopped")

    def play_alarm(self): #  Alarm that actually plays
        winsound.Beep(6000, 10000)

    def count_down(self):
        # checks if the timer is running
        if self.is_running:
            remaining = self.end_time - datetime.now()
            total_seconds = int(remaining.total_seconds())
            if total_seconds <= 0:
                self.timer_label.config(text="00:00")
                self.is_running = False

                # adds the completed session time to today's total
                self.today_seconds += self.session_seconds

                # this saves todays total study time to a file so it can be used later
                file = open("study_time.txt", "w")
                file.write(str(self.today_seconds))
                file.close()

                # this sends the real study time to the study projector for feedback
                self.projector.feedback(self.today_seconds, 0)

                print("Time’s up!")  # Now a new thing
                self.play_alarm()  # alarm now plays its horror to listen to
            else:
                mins, secs = divmod(total_seconds, 60)
                self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
                self.window.after(1000, self.count_down)  # updates every second


# This class is responcible for motivatint the user to work harder
class Study_projector:
    def __init__(self, window):
        self.window = window
        self.tomorrows_challenge = 0  # stored in seconds

    def feedback(self, today_minutes, yesterday_minutes):
        daily_target = 3 * 60 * 60  # 3 hours in seconds
        if today_minutes < yesterday_minutes:
            message = ("You studied less than yesterday. That’s okay — refocus and try to beat it tomorrow.")
            self.tomorrows_challenge = yesterday_minutes
        elif today_minutes < 30 * 60:
            message = ("You got started, which matters. Try to reach 30 minutes tomorrow.")
            self.tomorrows_challenge = 30 * 60
        elif today_minutes < 60 * 60:
            message = ("Good start. Aim for a full hour next time.")
            self.tomorrows_challenge = 60 * 60
        elif today_minutes == 60 * 60:
            message = ("One hour completed. Tomorrow, push for an hour and a half.")
            self.tomorrows_challenge = 90 * 60
        elif today_minutes < 90 * 60:
            message = ("You’re building momentum. Keep pushing towards 90 minutes.")
            self.tomorrows_challenge = 90 * 60
        elif today_minutes == 90 * 60:
            message = ("Great session. Aim for two hours next.")
            self.tomorrows_challenge = 120 * 60
        elif today_minutes < 120 * 60:
            message = ("Strong effort. Two hours is within reach.")
            self.tomorrows_challenge = 120 * 60
        elif today_minutes == 120 * 60:
            message = ("Two hours completed. Try to reach two and a half hours tomorrow.")
            self.tomorrows_challenge = 150 * 60
        elif today_minutes < 150 * 60:
            message = ("You’re pushing into high focus levels. Keep going.")
            self.tomorrows_challenge = 150 * 60
        elif today_minutes == 150 * 60:
            message = ("Outstanding work. Aim for the full 3 hours next.")
            self.tomorrows_challenge = daily_target
        else:
            message = ("Excellent discipline. Maintain this pace tomorrow.")
            self.tomorrows_challenge = daily_target

        feedback_label = tk.Label(self.window, text=message, font=("Arial", 14), wraplength=700); feedback_label.pack(pady=10)


class Graph_Display:
    def __init__(self, window):
        self.window = window

        # graph button (bottom-left corner)
        self.graph_button = tk.Button(self.window, text="Graph", font=("Arial", 18), command=self.show_graph)
        self.graph_button.place(x=20, y=550)  # positioned bottom-left

    def show_graph(self):
        #this shows a fraph however i have ran into  a problem which is that this is shown using pycharm ask hamfflet on how to male it tkinter
        days = ["Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"] # temp values
        minutes_studied = [0, 30, 45, 60, 90, 99] # more temp values

        # this for loop controls the colour of the bad depending on how much work the user has doen
        colours = []
        for minutes in minutes_studied:
            if minutes == 0:
                colours.append("red")
            elif minutes < 30:
                colours.append("orange")
            else:
                colours.append("green")

        # this just dispalays the grph
        plt.bar(days, minutes_studied, color=colours)
        plt.title("Graph of Sessions")
        plt.xlabel("Days")
        plt.ylabel("Study Time")
        plt.show()


class MyGUI:
    # this is the main window of the app
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PomoFocus")
        self.window.geometry("800x600")
        self.window.configure(bg="white")

        # main title for the page
        self.label = tk.Label(self.window, text="PomoFocus", font=("Arial", 18))
        self.label.pack(pady=20)

        # creates the study projector
        self.projector = Study_projector(self.window)

        # creates the timer object and links it to the study projector
        self.timer = Timer(self.window, self.projector)

        # creates the graph page
        self.graph = Graph_Display(self.window)

        # starts the GUI
        self.window.mainloop()


MyGUI()
