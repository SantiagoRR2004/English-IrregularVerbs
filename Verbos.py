from random import randint, sample, choices
import datetime
import pandas as pd
import unicodedata
import os


def processString(inputString: str) -> str:
    """
    Process a string to normalize it by removing accents and replacing spaces with underscores.

    Args:
        - inputString (str): The string to process

    Returns:
        - str: The processed string
    """
    # Normalize and remove accents
    no_accents = "".join(
        c
        for c in unicodedata.normalize("NFD", inputString)
        if unicodedata.category(c) != "Mn"
    )
    # Replace spaces with underscores
    result = no_accents.replace(" ", "_")
    return result


def getVerbs(filePath: str) -> pd.DataFrame:
    """
    Get the verb data from the file

    Args:
    - filePath (str): The path to the file containing the list of irregular verbs

    Returns:
        - pd.DataFrame: DataFrame containing the verbs
    """
    df = pd.read_csv(filePath, encoding="utf-8-sig", sep="\t")
    print("The file contains:", len(df), "verbs")

    return df


def createExams(
    fileInName: str = "./ListaVerbos.txt",
    numOfVerbs: int = 30,
    numOfExams: int = 1,
    saveHTML: bool = True,
    folderHTMLPath: str = "./",
    savePDF: False = bool,
    folderPDFPath: str = "./",
    studentsFile: str = None,
) -> None:
    """
    Create multiple exams with irregular verbs.

    Args:
        - fileInName (str): The name of the file containing the list of irregular verbs
        - numOfVerbs (int): The number of verbs to include in each exam
        - numOfExams (int): The number of exams to create
        - folderHTMLPath (str): The folder where the html exams will be saved
        - folderPDFPath (str): The folder where the pdf exams will be saved
        - studentsFile (str): The name of the file containing the list of students
            This file should have two columns: surname and name.

    Returns:
        - None
    """
    if not (saveHTML or savePDF):
        print("Warning: Nothing will be saved.")

    width = len(str(numOfExams))
    verbs = getVerbs(fileInName)

    if studentsFile:
        df = pd.read_csv(studentsFile)

        for student in df.itertuples(index=False):
            fullName = "_" + processString(
                student[1] + " " + student[0]
            )  # name + surname

            for i in range(numOfExams):
                number = f"_{i+1:0{width}d}" if numOfExams > 1 else ""
                finalPath = os.path.join(
                    folderHTMLPath, f"ExamenVerbos{fullName}{number}.html"
                )
                createExam(
                    verbs,
                    finalPath,
                    numOfVerbs,
                    name=student[0],
                    surname=student[1],
                )

    else:
        # No students file
        for i in range(numOfExams):
            number = f"_{i+1:0{width}d}" if numOfExams > 1 else ""
            finalPath = os.path.join(folderHTMLPath, f"ExamenVerbos{number}.html")
            createExam(verbs, finalPath, numOfVerbs)


def createExam(
    verbs: pd.DataFrame,
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
        - verbs (pd.DataFrame): The DataFrame containing the irregular verbs
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

    # Fill without repetition
    indexes = sample(range(1, len(verbs)), min(numOfVerbs, len(verbs) - 1))

    # If more verbs are needed than unique options, allow repeats
    if len(indexes) < numOfVerbs:
        remaining = numOfVerbs - len(indexes)
        indexes += choices(range(1, len(verbs)), k=remaining)

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
            verbs.columns[0], verbs.columns[1], verbs.columns[2], verbs.columns[3]
        )
    )

    numQuest = 1
    for index in indexes:
        fileOut.write("<tr>")
        fileOut.write("<th>{}</th>".format(numQuest))
        words = verbs.iloc[index]
        given_word = randint(0, 3)
        for iw in range(4):
            if iw == given_word:
                fileOut.write('<th width="300px">{}</th>'.format(words.iloc[iw]))
            else:
                fileOut.write('<th width="300px"> </th>')
        fileOut.write("</tr>")

        numQuest += 1

    fileOut.write(html_tail)

    fileOut.close()

    print("An exam was generated containing " + str(len(indexes)) + " verbs")
