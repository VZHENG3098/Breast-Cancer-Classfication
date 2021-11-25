
import breast_cancer_treeplot

def loadDataSet(filepath):
    '''
    Returns
    -----------------
    data: 2-D list
        each row is the feature and label of one instance
    featNames: 1-D list
        feature names
    '''
    data=[]
    featNames = None
    fr = open(filepath)
    for (i,line) in enumerate(fr.readlines()):
        array=line.strip().split(',')
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
        if instance[axis] == value:    # if contains the given feature value
            reducedVec = instance[:axis] + instance[axis+1:] # remove the given axis
            subset.append(reducedVec)
    return subset


def chooseBestFeature(dataSet):
    greatestIndex = 0
    greatGiniValue = 0
    for i in range(0,len(dataSet[0])-1):
        listOfAllFeature = dict()
        ValueOfLabel = dict()
        labelIndex = len(dataSet[i]) - 1
        for currentLabel in dataSet:
            Label = currentLabel[labelIndex]
            if currentLabel[i] in listOfAllFeature:
                listOfAllFeature[currentLabel[i]][1] += 1
                labelHolder = listOfAllFeature[currentLabel[i]][0]
                if Label in labelHolder:
                    labelHolder[Label] += 1
                else:
                    labelHolder[Label] = 1
                    listOfAllFeature[currentLabel[i]][0] = labelHolder
            else:
                labelHolder = dict()
                labelHolder[Label] = 1
                listOfAllFeature[currentLabel[i]] = [labelHolder, 1]
            if currentLabel[labelIndex] in ValueOfLabel:
                ValueOfLabel[currentLabel[labelIndex]] += 1
            else:
                ValueOfLabel[currentLabel[labelIndex]] = 1
        giniIndexParent = 1
        for key in ValueOfLabel:
            giniIndexParent -= pow((ValueOfLabel[key] / len(dataSet)), 2)
        GiniIndexForEachFeature = dict()
        for key in listOfAllFeature:
            featureGini = 1
            for key2 in listOfAllFeature[key][0]:
                featureGini -= pow((listOfAllFeature[key][0][key2] / listOfAllFeature[key][1]), 2)
            GiniIndexForEachFeature[key] = featureGini
        SubtractGiniBy = 0
        for key in listOfAllFeature:
            SubtractGiniBy += listOfAllFeature[key][1] / len(dataSet) * GiniIndexForEachFeature[key]
        featureGiniParent = giniIndexParent - SubtractGiniBy
        if i == 0:
            greatGiniValue = featureGiniParent
        elif greatGiniValue < featureGiniParent:
            greatestIndex = i
            greatGiniValue = featureGiniParent
    return greatestIndex


def stopCriteria(dataSet):
    '''
    Criteria to stop splitting:
    1) if all the classe labels are the same, then return the class label;
    2) if there are no more features to split, then return the majority label of the subset.

    Parameters
    -----------------
    dataSet: 2-D list
        [n_sampels, m_features + 1]
        the last column is class label

    Returns
    ------------------
    assignedLabel: string
        if satisfying stop criteria, assignedLabel is the assigned class label;
        else, assignedLabel is None
    '''
    # TODO
    assignedLabel = None
    returnBool = True
    MajorityTable = dict()
    labelIndex = len(dataSet[0])-1
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

    SortedDict = sorted(MajorityTable.items(), key = lambda kv: kv[1],reverse=True)
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

    myTree = {bestFeatName:{}}
    subFeatName = featNames[:]
    del(subFeatName[bestFeatId])
    featValues = [d[bestFeatId] for d in dataSet]
    uniqueVals = list(set(featValues))
    for value in uniqueVals:
        myTree[bestFeatName][value] = buildTree(splitData(dataSet, bestFeatId, value), subFeatName)

    return myTree



if __name__ == "__main__":
    data, featNames = loadDataSet('car.csv')
    dtTree = buildTree(data, featNames)
    # print (dtTree)
    treeplot.createPlot(dtTree)
