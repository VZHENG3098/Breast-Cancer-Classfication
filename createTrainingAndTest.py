import csv
import random
def createnewData():
    newLines = []
    with open('Breast.csv', 'r') as input_file:
        lines = input_file.readlines()

        for line in lines:
            newLine = line.strip().split()
            newLines.append(newLine)

    testingData = []
    amountData = 0
    dataCheck = len(newLines) / 4
    #print(len(newLines))
    #print(newLines[0])
    while amountData < dataCheck:
        getRandomNumber = random.randint(1, len(newLines) - 1)
        testingData.append(newLines[getRandomNumber])
        newLines.pop(getRandomNumber)
        amountData += 1

    with open('TestingData.csv', 'w', newline="") as test_file:
        file_writer = csv.writer(test_file)
        labels = []
        for att in newLines[0][0].split(","):
            labels.append(str(att))
        file_writer.writerow(labels)
        for line in testingData:
            lineSplit = line[0].split(",")
            lineAdd = []
            for index in range(0, len(lineSplit)):
                lineAdd.append(lineSplit[index])
            file_writer.writerow(lineAdd)

    with open('TrainingData.csv', 'w', newline="") as test_file:
        file_writer = csv.writer(test_file)
        for line in newLines:
            lineSplit = line[0].split(",")
            lineAdd = []
            for index in range(0, len(lineSplit)):
                lineAdd.append(lineSplit[index])
            file_writer.writerow(lineAdd)

    #print(len(newLines))