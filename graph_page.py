import tkinter as tk
class MyGUI:
    # this is the main window of the app
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PomoFocus")
        self.window.geometry("800x600")
        self.window.configure(bg="white")

        # main title for the page
        self.label = tk.Label(self.window, text="Graph page", font=("Arial", 18))
        self.label.pack(pady=20)

        # starts the GUI
        self.window.mainloop()

MyGUI()
