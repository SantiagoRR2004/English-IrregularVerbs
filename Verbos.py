from random import randint, sample, choices
import datetime
import pandas as pd
import os


def createExams(
    fileInName: str = "./ListaVerbos.txt",
    folderPath: str = "./",
    numOfVerbs: int = 30,
    numOfExams: int = 1,
    studentsFile: str = None,
) -> None:
    """
    Create multiple exams with irregular verbs.

    Args:
        - fileInName (str): The name of the file containing the list of irregular verbs
        - folderPath (str): The folder where the exams will be saved
        - numOfVerbs (int): The number of verbs to include in each exam
        - numOfExams (int): The number of exams to create
        - studentsFile (str): The name of the file containing the list of students
            This file should have two columns: surname and name.

    Returns:
        - None
    """
    df = pd.read_csv(studentsFile)

    width = len(str(numOfExams))

    for student in df.itertuples(index=False):
        fullName = student[1] + " " + student[0]

        for i in range(numOfExams):
            number = f"{i+1:0{width}d}" if numOfExams > 1 else ""
            finalPath = os.path.join(
                folderPath, f"ExamenVerbos_{fullName}_{number}.html"
            )
            createExam(
                fileInName, finalPath, numOfVerbs, name=student[0], surname=student[1]
            )


def createExam(
    fileInName: str = "./ListaVerbos.txt",
    fileOutName: str = "./ExamenVerbos.html",
    numOfVerbs: int = 30,
    name: str = "_____________",
    surname: str = "_____________",
) -> None:
    """
    Create an exam with irregular verbs.

    There will be 4 columns:
        - The infinitive
        - The simple past
        - The past participle
        - The translation

    Only one of the columns will contain the word, the other three will be empty.

    Args:
        - fileInName (str): The name of the file containing the list of irregular verbs
        - fileOutName (str): The name of the file to save the exam
        - numOfVerbs (int): The number of verbs to include in the exam
        - name (str): The name of the student
        - surname (str): The surname of the student

    Returns:
        - None
    """
    html_head = f"""
    <hmtl>
        <meta charset="UTF-8">
        <head>
            <style>
                table, th, td {{
                    border: 1px solid black;
                    border-collapse: collapse;
                }}
                th, td {{
                    padding: 5px;
                }}
                .header-line {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 20px;
                }}
                .title {{
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 40px;
                }}
                .name-surname {{
                    line-height: 0.1; /* Adjusts spacing between lines */
                    margin-left: 40px; /* Adds indentation */
                    margin-bottom: 40px; /* Adds space between the surname section and the table */
                }}
            </style>
        </head>
        <body>
            <div class="header-line">
                <span>English</span>
                <span>{datetime.datetime.now().strftime("%d/%m/%Y")}</span>
            </div>
            <h1 class="title">IRREGULAR VERB EXAM</h1>
            <div class="name-surname">
                <p>Name: {name}</p>
                <p>Surname: {surname}</p>
        </div>

            <table>
    """

    html_tail = """
            </table>
        </body>
    </hmtl>
    """

    with open(fileInName, encoding="utf-8-sig") as fileIn:
        content = fileIn.readlines()
    lineas = [x.strip() for x in content]
    print("The file contains: " + str(len(lineas) - 1) + " verbs")

    columns = lineas[0].split("\t")

    # Fill without repetition
    indexes = sample(range(1, len(lineas)), min(numOfVerbs, len(lineas) - 1))

    # If more verbs are needed than unique options, allow repeats
    if len(indexes) < numOfVerbs:
        remaining = numOfVerbs - len(indexes)
        indexes += choices(range(1, len(lineas)), k=remaining)

    fileOut = open(fileOutName, "w", encoding="utf-8")

    fileOut.write(html_head)

    fileOut.write(
        """
    <tr>
        <th><i>No.</i></th>
        <th width="300px"><i>{}</i></th>
        <th width="300px"><i>{}</i></th>
        <th width="300px"><i>{}</i></th>
        <th width="300px"><i>{}</i></th>
    </tr>
    """.format(
            columns[0], columns[1], columns[2], columns[3]
        )
    )

    numQuest = 1
    for index in indexes:
        fileOut.write("<tr>")
        fileOut.write("<th>{}</th>".format(numQuest))
        words = lineas[index].split("\t")
        given_word = randint(0, 3)
        for iw in range(4):
            if iw == given_word:
                fileOut.write('<th width="300px">{}</th>'.format(words[iw]))
            else:
                fileOut.write('<th width="300px"> </th>')
        fileOut.write("</tr>")

        numQuest += 1

    fileOut.write(html_tail)

    fileOut.close()

    print("An exam was generated containing " + str(len(indexes)) + " verbs")


if __name__ == "__main__":
    createExam()
