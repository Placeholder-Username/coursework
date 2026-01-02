import tkinter as tk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class Timer:
    # this makes the timer part of the app
    def __init__(self, window):
        self.window = window
        self.time_left = 0
        self.is_running = False
        self.end_time = None

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

    def start_timer(self):
        # this takes the user’s input, then converts it into an integer as entry.get() returns strings
        user_input = self.time_entry.get()
        self.time_left = int(user_input) * 60  # converts minutes into seconds
        self.is_running = True

        # datetime library gives a more accurate countdown
        self.end_time = datetime.now() + timedelta(seconds=self.time_left)
        self.count_down()

    def stop_timer(self):
        self.is_running = False
        self.timer_label.config(text="Stopped")

    def count_down(self):
        # checks if the timer is running
        if self.is_running:
            remaining = self.end_time - datetime.now()
            total_seconds = int(remaining.total_seconds())

            if total_seconds <= 0:
                self.timer_label.config(text="00:00")
                self.is_running = False
                print("Time’s up!")  # placeholder for alarm feature
            else:
                mins, secs = divmod(total_seconds, 60)
                self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
                self.window.after(1000, self.count_down)  # updates every second


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

        # creates the timer object
        self.timer = Timer(self.window)

        # creates the graph page
        self.graph = Graph_Display(self.window)

        # starts the GUI
        self.window.mainloop()


MyGUI()