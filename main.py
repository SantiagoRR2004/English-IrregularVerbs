import tkinter as tk
import Verbos


class ExamCreator:

    NUMBEROFVERBS = 30

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
        self.createLabel()
        self.createSpinbox()
        self.createButton()

    def createLabel(self):
        label = tk.Label(self.window, text="Number of verbs:")
        label.grid(row=0, column=0, padx=5, pady=10, sticky="w")

    def createSpinbox(self):
        self.spinbox = tk.Spinbox(
            self.window,
            from_=1,
            to=float("inf"),
            width=5,
            textvariable=tk.StringVar(value=self.numOfVerbs),
        )
        self.spinbox.grid(row=0, column=1, padx=5, pady=10, sticky="w")

    def createButton(self):
        button = tk.Button(self.window, text="Create exams", command=self.save_number)
        button.place(
            relx=1.0, rely=1.0, anchor="se", x=-10, y=-10
        )  # Places it in the bottom-right with some padding

    def save_number(self):

        try:
            self.numOfVerbs = int(self.spinbox.get())  # Convert input to an integer
            self.window.destroy()
            Verbos.createExams(numOfVerbs=self.numOfVerbs)

        except Exception as e:
            print("An error occurred: ", e)


if __name__ == "__main__":
    ExamCreator()
