import tkinter as tk
from tkinter import filedialog
import Verbos
import os


class ExamCreator:

    NUMBEROFVERBS = 30
    VERBSFILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "ListaVerbos.txt"
    )

    def __init__(self) -> None:
        self.reset()
        self.window.mainloop()

    def reset(self):
        self.numOfVerbs = self.NUMBEROFVERBS
        self.createWindow()

    def createWindow(self):
        self.window = tk.Tk()
        self.window.title("Irregular Verb Exam Creator")
        self.window.geometry("800x600")
        self.createWidgets()

    def createWidgets(self):
        self.createNumberOfVerbs()
        self.createVerbLocation()
        self.createButton()

    def createNumberOfVerbs(self) -> None:
        """
        Create a spinbox to select the number of verbs for the exam.
        """
        label = tk.Label(self.window, text="Number of verbs:")
        label.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.spinboxNVerbs = tk.Spinbox(
            self.window,
            from_=1,
            to=float("inf"),
            width=5,
            textvariable=tk.IntVar(value=self.numOfVerbs),
        )
        self.spinboxNVerbs.grid(row=0, column=1, padx=5, pady=10, sticky="w")

    def browse_file(self) -> None:
        """
        Necessary function to get the Browse button working.

        Args:
            - None

        Returns:
            - None
        """
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            self.file_path_var.set(file_path)

    def createVerbLocation(self) -> None:
        """
        Create the file selection entry and button to choose the verbs file.

        Args:
            - None

        Returns:
            - None
        """

        # File selection Entry and Button
        self.file_path_var = tk.StringVar(value=self.VERBSFILE)

        # Label
        self.file_label = tk.Label(self.window, text="Fichero con verbos:")
        self.file_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")

        # Entry
        self.file_entry = tk.Entry(
            self.window, textvariable=self.file_path_var, width=40, state="readonly"
        )
        self.file_entry.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        # Button
        self.file_button = tk.Button(
            self.window, text="Browse...", command=self.browse_file
        )
        self.file_button.grid(row=1, column=2, padx=5, pady=10, sticky="e")

    def createButton(self):
        button = tk.Button(self.window, text="Create exams", command=self.save_number)
        button.place(
            relx=1.0, rely=1.0, anchor="se", x=-10, y=-10
        )  # Places it in the bottom-right with some padding

    def save_number(self):
        try:
            self.numOfVerbs = int(
                self.spinboxNVerbs.get()
            )  # Convert input to an integer
            Verbos.createExams(
                numOfVerbs=self.numOfVerbs, fileInName=self.file_path_var.get()
            )
            self.window.destroy()

        except Exception as e:
            print("An error occurred: ", e)


if __name__ == "__main__":
    ExamCreator()
