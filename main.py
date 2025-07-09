import tkinter as tk
from tkinter import filedialog
import Verbos
import os


class ExamCreator:

    NUMBEROFVERBS = 30
    VERBSFILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "ListaVerbos.txt"
    )
    NUMBEROFEXAMS = 1
    EXAMFOLDER = os.path.dirname(os.path.abspath(__file__))

    def __init__(self) -> None:
        self.createWindow()
        self.window.mainloop()

    def reset(self):
        self.numOfVerbs = self.NUMBEROFVERBS
        self.numOfExams = self.NUMBEROFEXAMS
        for widget in self.window.winfo_children():
            widget.destroy()
        self.createWidgets()

    def createWindow(self):
        self.window = tk.Tk()
        self.window.title("Irregular Verb Exam Creator")
        self.window.geometry("800x600")
        self.reset()

    def createWidgets(self):
        self.createNumberOfVerbs()
        self.createVerbLocation()
        self.createNumberOfExams()
        self.createExamButton()
        self.createExamLocation()
        self.createResetButton()

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

    def browse_folder(self) -> None:
        """
        Necessary function to get the Browse button working.

        Args:
            - None

        Returns:
            - None
        """
        folder_path = filedialog.askdirectory(title="Select a folder")
        if folder_path:
            self.exam_folder_path_var.set(folder_path)

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
        self.file_label = tk.Label(self.window, text="Verb file:")
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

    def createNumberOfExams(self) -> None:
        """
        Create a spinbox to select the number of exams to create.
        """
        label = tk.Label(self.window, text="Number of exams:")
        label.grid(row=2, column=0, padx=5, pady=10, sticky="w")
        self.spinboxNExams = tk.Spinbox(
            self.window,
            from_=1,
            to=float("inf"),
            width=5,
            textvariable=tk.IntVar(value=self.numOfExams),
        )
        self.spinboxNExams.grid(row=2, column=1, padx=5, pady=10, sticky="w")

    def createExamLocation(self) -> None:
        """
        Create the folder selection entry and button to choose where
        the exams will be created.

        Args:
            - None

        Returns:
            - None
        """
        # File selection Entry and Button
        self.exam_folder_path_var = tk.StringVar(value=self.EXAMFOLDER)

        # Label
        self.file_label = tk.Label(self.window, text="Exam Destination:")
        self.file_label.grid(row=4, column=0, padx=5, pady=10, sticky="w")

        # Entry
        self.file_entry = tk.Entry(
            self.window,
            textvariable=self.exam_folder_path_var,
            width=40,
            state="readonly",
        )
        self.file_entry.grid(row=4, column=1, padx=5, pady=10, sticky="w")

        # Button
        self.file_button = tk.Button(
            self.window, text="Browse...", command=self.browse_folder
        )
        self.file_button.grid(row=4, column=2, padx=5, pady=10, sticky="e")

    def createExamButton(self):
        button = tk.Button(self.window, text="Create exams", command=self.save_number)
        button.place(
            relx=1.0, rely=1.0, anchor="se", x=-10, y=-10
        )  # Places it in the bottom-right with some padding

    def createResetButton(self):
        button = tk.Button(self.window, text="Reset", command=self.reset)
        button.place(
            relx=0.0, rely=1.0, anchor="sw", x=10, y=-10
        )  # Bottom-left with padding

    def save_number(self):
        try:
            self.numOfVerbs = int(
                self.spinboxNVerbs.get()
            )  # Convert input to an integer
            self.numOfExams = int(self.spinboxNExams.get())
            Verbos.createExams(
                numOfVerbs=self.numOfVerbs,
                fileInName=self.file_path_var.get(),
                numOfExams=self.numOfExams,
            )
            self.window.destroy()

        except Exception as e:
            print("An error occurred: ", e)


if __name__ == "__main__":
    ExamCreator()
