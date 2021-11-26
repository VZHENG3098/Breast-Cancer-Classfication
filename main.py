import csv

with open('breast-cancer.data', 'r') as input_file:
    lines = input_file.readlines()
    newLines = []
    for line in lines:
        newLine = line.strip().split()
        newLines.append(newLine)

labels = ["Class", "age", "menopause", "tumor-size", "inv-nodes", "node-caps", "deg-malig", "breast", "breast-quad",
          "irradiat"]
with open('Breast.csv', 'w', newline="") as test_file:
    file_writer = csv.writer(test_file)
    file_writer.writerow(labels)
    for line in newLines:
        lineSplit = line[0].split(",")
        lineAdd = []
        for index in range(0, len(lineSplit) - 1):
            lineAdd.append(lineSplit[index].replace("-", "--"))
        file_writer.writerow(lineAdd)