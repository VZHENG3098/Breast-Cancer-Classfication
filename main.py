import csv
import pandas



with open('breast-cancer.data', 'r') as input_file:
    lines = input_file.readlines()
    newLines = []
    for line in lines:
        newLine = line.strip().split()
        newLines.append(newLine)
print(newLines)
labels = ["Class", "age", "menopause", "tumor-size", "inv-nodes", "node-caps", "deg-malig", "breast", "breast-quad",
          "irradiat"]
with open('Breast.csv', 'w', newline="") as test_file:
    file_writer = csv.writer(test_file)
    file_writer.writerow(labels)
    for line in newLines:
        lineSplit = line[0].split(",")
        lineAdd = []
        for index in range(0, len(lineSplit)):
            lineAdd.append(lineSplit[index].replace("-", "--"))
        file_writer.writerow(lineAdd)

# Convert CSV File and replacing first column to last
df = pandas.read_csv('Breast.csv')
print(df.keys())

df = df[["age", "menopause", "tumor-size", "inv-nodes", "node-caps", "deg-malig", "breast", "breast-quad","irradiat","Class"]]
df.to_csv('Breast.csv',index=False)