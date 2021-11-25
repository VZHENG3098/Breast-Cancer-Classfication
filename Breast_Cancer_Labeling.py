import collections

import treeplot


def loadDataSet(filepath):
    '''
    Returns
    -----------------
    data: 2-D list
        each row is the feature and label of one instance
    featNames: 1-D list
        feature names
    '''
    data = []
    featNames = None
    fr = open(filepath)
    for (i, line) in enumerate(fr.readlines()):
        array = line.strip().split(',')
        if i == 0:
            featNames = array[:-1]
        else:
            data.append(array)
    return data, featNames


def splitData(dataSet, axis, value):
    '''
    Split the dataset based on the given axis and feature value

    Parameters
    -----------------
    dataSet: 2-D list
        [n_sampels, m_features + 1]
        the last column is class label
    axis: int
        index of which feature to split on
    value: string
        the feature value to split on

    Returns
    ------------------
    subset: 2-D list
        the subset of data by selecting the instances that have the given feature value
        and removing the given feature columns
    '''
    subset = []
    for instance in dataSet:
        if instance[axis] == value:  # if contains the given feature value
            reducedVec = instance[:axis] + instance[axis + 1:]  # remove the given axis
            subset.append(reducedVec)
    return subset


def parentGini(TdataSet, parent, dataSetSize):
    labels = collections.Counter(TdataSet[len(TdataSet) - 1])
    for label in labels.values():
        parent -= (label / dataSetSize) ** 2
    return parent


def uniqueFeature(TdataSet):
    featureKeys = []
    TdataSetSize = len(TdataSet)
    for i in range(TdataSetSize - 1):
        featureKeys.append(sorted(list(set(TdataSet[i]))))
    return featureKeys


def uniqueLabel(TdataSet):
    TdataSetSize = len(TdataSet)
    label = sorted(list(set(TdataSet[TdataSetSize - 1])))
    return label


def fillList(length):
    filled = []
    for i in range(length):
        filled.append(0)
    return filled


def chooseBestFeature(dataSet):
    dataSetSize = len(dataSet)
    TdataSet = list(map(list, zip(*dataSet)))
    parent = parentGini(TdataSet, 1, dataSetSize)
    featureKeys = uniqueFeature(TdataSet)
    labels = uniqueLabel(TdataSet)
    Gain = []  # index of list corresponds to feature in the TdataSet
    for featuresIndex in range(len(featureKeys)):
        subfeatures = []
        for feature in featureKeys[featuresIndex]:
            totalLabeled = fillList(len(labels))
            total = 1
            for entry in dataSet:
                if entry[featuresIndex] == feature:
                    for labelIndex in range(len(labels)):
                        if entry[len(entry) - 1] == labels[labelIndex]:
                            totalLabeled[labelIndex] += 1
            for labeled in totalLabeled:
                total -= (labeled / sum(totalLabeled)) ** 2
            subfeatures.append(total * (sum(totalLabeled) / dataSetSize))
        Gain.append(parent - (sum(subfeatures)))
    return Gain.index(max(Gain))


def sameLabel(dataSet):
    assignedLabel = dataSet[0][len(dataSet[0]) - 1]
    for i in range(len(dataSet)):
        if assignedLabel != dataSet[i][len(dataSet[i]) - 1]:
            return False
    return True


def stopCriteria(dataSet):
    assignedLabel = None
    returnBool = True
    MajorityTable = dict()
    labelIndex = len(dataSet[0]) - 1
    for currentLabel in dataSet:
        if currentLabel[labelIndex] in MajorityTable:
            MajorityTable[currentLabel[labelIndex]] += 1
        else:
            MajorityTable[currentLabel[labelIndex]] = 1
        if assignedLabel == None:
            assignedLabel = currentLabel[labelIndex]
        else:
            if assignedLabel != currentLabel[labelIndex]:
                returnBool = False

    if returnBool:
        return assignedLabel

    SortedDict = sorted(MajorityTable.items(), key=lambda kv: kv[1], reverse=True)
    if len(dataSet[0]) <= 1:
        return SortedDict[0][0]
    return None


def buildTree(dataSet, featNames):
    '''
    Build the decision tree

    Parameters
    -----------------
    dataSet: 2-D list
        [n'_sampels, m'_features + 1]
        the last column is class label

    Returns
    ------------------
        myTree: nested dictionary
    '''
    assignedLabel = stopCriteria(dataSet)
    if assignedLabel:
        return assignedLabel

    bestFeatId = chooseBestFeature(dataSet)
    bestFeatName = featNames[bestFeatId]

    myTree = {bestFeatName: {}}
    subFeatName = featNames[:]
    del (subFeatName[bestFeatId])
    featValues = [d[bestFeatId] for d in dataSet]
    uniqueVals = list(set(featValues))
    for value in uniqueVals:
        myTree[bestFeatName][value] = buildTree(splitData(dataSet, bestFeatId, value), subFeatName)

    return myTree


if __name__ == "__main__":
    data, featNames = loadDataSet('Breast.csv')
    dtTree = buildTree(data, featNames)
    # print (dtTree)
    print(dtTree)
    treeplot.createPlot(dtTree)
