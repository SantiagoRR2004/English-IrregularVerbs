from random import randint
import datetime


def createExams(
    fileInName: str = "./ListaVerbos.txt",
    fileOutName: str = "./ExamenVerbos.html",
    numOfVerbs: int = 30,
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
            </style>
        </head>
        <body>
            <div class="header-line">
                <span>English</span>
                <span>{datetime.datetime.now().strftime("%d/%m/%Y")}</span>
            </div>
            <h1 class="title">IRREGULAR VERB EXAM</h1>
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

    indexes = []
    while len(indexes) < numOfVerbs:
        random_verb = randint(1, len(lineas) - 1)
        if random_verb not in indexes:
            indexes.append(random_verb)

    fileOut = open(fileOutName, "w")

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
    createExams()
