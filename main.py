import tkinter as tk
from tkinter import filedialog
import Verbos
import os


class ExamCreator:

    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    NUMBEROFVERBS = 30
    VERBSFOLDER = os.path.join(currentDirectory, "Verbs")
    NUMBEROFEXAMS = 1
    HTML = True
    HTMLFOLDER = currentDirectory
    PDF = False
    PDFFOLDER = currentDirectory
    STUDENTSFILE = ""

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
        self.createUseHTMLButton()
        self.createHTMLLocation()
        self.createUsePDFButton()
        self.createPDFLocation()
        self.createStudentLocation()
        self.createExamButton()
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

    def browse_file(self, fileToSet: tk.StringVar) -> None:
        """
        Necessary function to get the Browse button working.

        Args:
            - fileToSet: A StringVar to set the file path.

        Returns:
            - None
        """
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            fileToSet.set(file_path)

    def browse_folder(self, pathToSet: tk.StringVar) -> None:
        """
        Necessary function to get the Browse button working.

        Args:
            - pathToSet: A StringVar to set the folder path.

        Returns:
            - None
        """
        folder_path = filedialog.askdirectory(title="Select a folder")
        if folder_path:
            pathToSet.set(folder_path)

    def createVerbLocation(self) -> None:
        """
        Create the file selection entry and button to choose the verbs file.

        Args:
            - None

        Returns:
            - None
        """
        # Get the txt files
        txtFiles = [f for f in os.listdir(self.VERBSFOLDER) if f.endswith(".csv")]

        # File selection Entry and Button
        self.file_path_var = tk.StringVar(value=txtFiles[0])

        # Label
        fileLabel = tk.Label(self.window, text="Verb file:")
        fileLabel.grid(row=1, column=0, padx=5, pady=10, sticky="w")

        # Dropdown
        fileDropdown = tk.OptionMenu(self.window, self.file_path_var, *txtFiles)
        fileDropdown.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        # Button
        fileButton = tk.Button(
            self.window,
            text="Browse...",
            command=lambda: self.browse_file(self.file_path_var),
        )
        fileButton.grid(row=1, column=2, padx=5, pady=10, sticky="e")

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

    def createUseHTMLButton(self) -> None:
        """
        Create a checkbox to select whether to create HTML files or not.

        Args:
            - None

        Returns:
            - None
        """
        self.htmlVar = tk.BooleanVar(value=self.HTML)

        boolean_checkbox = tk.Checkbutton(
            self.window,
            text="Create HTML",
            command=self.updateHTMLLocation,
            variable=self.htmlVar,
        )
        boolean_checkbox.grid(row=5, column=0, padx=5, pady=10, sticky="w")

    def createHTMLLocation(self) -> None:
        """
        Create the folder selection entry and button to choose where
        the html exams will be created.

        Args:
            - None

        Returns:
            - None
        """
        # File selection Entry and Button
        self.html_folder_path_var = tk.StringVar(value=self.HTMLFOLDER)

        # Label
        folderLabel = tk.Label(self.window, text="HTML Destination:")
        folderLabel.grid(row=6, column=0, padx=5, pady=10, sticky="w")

        # Entry
        self.htmlFolderEntry = tk.Entry(
            self.window,
            textvariable=self.html_folder_path_var,
            width=40,
            state="readonly",
        )
        self.htmlFolderEntry.grid(row=6, column=1, padx=5, pady=10, sticky="w")

        # Button
        self.htmlFolderButton = tk.Button(
            self.window,
            text="Browse...",
            command=lambda: self.browse_folder(self.html_folder_path_var),
        )
        self.htmlFolderButton.grid(row=6, column=2, padx=5, pady=10, sticky="e")

        self.updateHTMLLocation()

    def updateHTMLLocation(self) -> None:
        """
        Update the state of the HTML folder entry and button based on the checkbox.

        Args:
            - None

        Returns:
            - None
        """
        if self.htmlVar.get():
            self.htmlFolderButton.config(state="normal")
            self.htmlFolderEntry.config(textvariable=self.html_folder_path_var)
        else:
            self.htmlFolderButton.config(state="disabled")
            self.htmlFolderEntry.config(textvariable=tk.StringVar(value=""))

    def createUsePDFButton(self) -> None:
        """
        Create a checkbox to select whether to create PDF files or not.

        Args:
            - None

        Returns:
            - None
        """
        self.pdfVar = tk.BooleanVar(value=self.PDF)

        boolean_checkbox = tk.Checkbutton(
            self.window,
            text="Create PDF",
            command=self.updatePDFLocation,
            variable=self.pdfVar,
        )
        boolean_checkbox.grid(row=7, column=0, padx=5, pady=10, sticky="w")

    def createPDFLocation(self) -> None:
        """
        Create the folder selection entry and button to choose where
        the pdf exams will be created.

        Args:
            - None

        Returns:
            - None
        """
        # File selection Entry and Button
        self.pdf_folder_path_var = tk.StringVar(value=self.PDFFOLDER)

        # Label
        folderLabel = tk.Label(self.window, text="PDF Destination:")
        folderLabel.grid(row=8, column=0, padx=5, pady=10, sticky="w")

        # Entry
        self.pdfFolderEntry = tk.Entry(
            self.window,
            textvariable=self.pdf_folder_path_var,
            width=40,
            state="readonly",
        )
        self.pdfFolderEntry.grid(row=8, column=1, padx=5, pady=10, sticky="w")

        # Button
        self.pdfFolderButton = tk.Button(
            self.window,
            text="Browse...",
            command=lambda: self.browse_folder(self.pdf_folder_path_var),
        )
        self.pdfFolderButton.grid(row=8, column=2, padx=5, pady=10, sticky="e")

        self.updatePDFLocation()

    def updatePDFLocation(self) -> None:
        """
        Update the state of the PDF folder entry and button based on the checkbox.

        Args:
            - None

        Returns:
            - None
        """
        if self.pdfVar.get():
            self.pdfFolderButton.config(state="normal")
            self.pdfFolderEntry.config(textvariable=self.pdf_folder_path_var)
        else:
            self.pdfFolderButton.config(state="disabled")
            self.pdfFolderEntry.config(textvariable=tk.StringVar(value=""))

    def createStudentLocation(self) -> None:
        """
        Create the file selection entry and button to choose the students file.

        Args:
            - None

        Returns:
            - None
        """
        # File selection Entry and Button
        self.students_file_path_var = tk.StringVar(value=self.STUDENTSFILE)

        # Label
        fileLabel = tk.Label(self.window, text="Students file (Optional):")
        fileLabel.grid(row=10, column=0, padx=5, pady=10, sticky="w")

        # Entry
        fileEntry = tk.Entry(
            self.window,
            textvariable=self.students_file_path_var,
            width=40,
            state="readonly",
        )
        fileEntry.grid(row=10, column=1, padx=5, pady=10, sticky="w")

        # Button
        fileButton = tk.Button(
            self.window,
            text="Browse...",
            command=lambda: self.browse_file(self.students_file_path_var),
        )
        fileButton.grid(row=10, column=2, padx=5, pady=10, sticky="e")

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

            verbFile = self.file_path_var.get()

            # One of the dropdown options
            if not os.path.exists(verbFile):
                verbFile = os.path.join(self.VERBSFOLDER, verbFile)

            Verbos.createExams(
                numOfVerbs=self.numOfVerbs,
                fileInName=verbFile,
                numOfExams=self.numOfExams,
                folderHTMLPath=self.html_folder_path_var.get(),
                saveHTML=self.htmlVar.get(),
                savePDF=self.pdfVar.get(),
                studentsFile=self.students_file_path_var.get(),
            )
            self.window.destroy()

        except Exception as e:
            print("An error occurred: ", e)


if __name__ == "__main__":
    ExamCreator()
