import tkinter as tk


numOfVerbs = 30


def save_number():
    global numOfVerbs
    try:
        numOfVerbs = int(spinbox.get())  # Convert input to an integer
    except ValueError:
        pass


root = tk.Tk()
root.title("Irregular Verb Exam Creator")
root.geometry("800x600")  # Set width to 800 and height to 600

# Label
label = tk.Label(root, text="Number of verbs:")
label.grid(row=0, column=0, padx=5, pady=10, sticky="w")

# Spinbox with arrows for increasing/decreasing the number
spinbox = tk.Spinbox(
    root, from_=1, to=float("inf"), width=5, textvariable=tk.StringVar(value=numOfVerbs)
)
spinbox.grid(row=0, column=1, padx=5, pady=10, sticky="w")


# Button to create the exams
button = tk.Button(root, text="Create exams", command=save_number)
button.place(
    relx=1.0, rely=1.0, anchor="se", x=-10, y=-10
)  # Places it in the bottom-right with some padding


root.mainloop()


print(numOfVerbs)
