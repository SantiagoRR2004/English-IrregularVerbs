from random import randint

fileInName = "./ListaVerbos.txt"
fileOutName = "./ExamenVerbos.html"

numOfVerbs = 30

html_head = '''
<hmtl>
	<head>
		<style>
		table, th, td {
			border: 1px solid black;
			border-collapse: collapse;
		}
		th, td {
			padding: 5px;
		}
		</style>
	</head>
	<body>
		<table>
'''

html_tail='''
		</table>
	</body>
</hmtl>
'''




with open(fileInName, encoding='utf-8-sig') as fileIn:
    content = fileIn.readlines()
lineas = [x.strip() for x in content]
print("The file contains: "+str(len(lineas)-1)+" verbs")

columns = lineas[0].split("\t")

indexes = []
while (len(indexes)<numOfVerbs):
    random_verb = randint(1,len(lineas)-1)
    if random_verb not in indexes:
        indexes.append(random_verb)

# print(indexes)
print("An exam was generated containing "+str(len(indexes))+" verbs")



fileOut = open(fileOutName, 'w')

fileOut.write(html_head)



fileOut.write('''
<tr>
    <th><i>No.</i></th>
    <th width="300px"><i>{}</i></th>
    <th width="300px"><i>{}</i></th>
    <th width="300px"><i>{}</i></th>
    <th width="300px"><i>{}</i></th>
</tr>
'''.format(columns[0],columns[1],columns[2],columns[3]))

numQuest = 1
for index in indexes:
    fileOut.write("<tr>")
    fileOut.write("<th>{}</th>".format(numQuest))
    words = lineas[index].split("\t")
    given_word = randint(0,3)
    for iw in range(4):
        if iw == given_word:
            fileOut.write('<th width="300px">{}</th>'.format(words[iw]))
        else:
            fileOut.write('<th width="300px"> </th>')
    fileOut.write("</tr>")


    numQuest += 1

fileOut.write(html_tail)

fileOut.close()