'''
    Question specifically mentions that we hard code the alpha  & delta values
'''

delta = 30
alphas = [[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]

def convertChar(c):
    if c=='A':
        return 0
    if c=='C':
        return 1
    if c=='G':
        return 2
    if c=='T':
        return 3

def validateStringLength(originalLength, newLineCnt, newLength):
    return (2**newLineCnt)*originalLength == newLength

def transformString(currentStr, id):
    return currentStr[0:id+1]+currentStr+currentStr[id+1:len(currentStr)]
    
def generateInput(inputStr, ids):
    oldLength = len(inputStr)
    for id in ids:
        inputStr = transformString(inputStr,id)
    opCnt = len(ids)
    newLength = len(inputStr)
    print('Performing string length validation')
    if validateStringLength(oldLength, opCnt, newLength):
        print('Validation checks passed')
    else:
        print('Validation checks failed')
    return inputStr

def getAlignments(cost,s1,s2):
    i = len(s2)
    j = len(s1)
    s1aligned = ''
    s2aligned = ''
    while i>0 and j>0:
        if alphas[convertChar(s1[j-1])][convertChar(s2[i-1])]+cost[i-1][j-1] == cost[i][j]:
            s1aligned = s1[j-1] + s1aligned
            s2aligned = s2[i-1] + s2aligned
            i-=1
            j-=1
        elif delta+cost[i-1][j] == cost[i][j]:
            s1aligned = '_' + s1aligned
            s2aligned  = s2[i-1] + s2aligned
            i-=1
        else:
            s2aligned = '_' + s2aligned
            s1aligned = s1[j-1] + s1aligned
            j-=1
    while i>0:
        s1aligned  = '_' + s1aligned
        s2aligned  = s2[i-1] + s2aligned
        i-=1
    while j>0:
        s2aligned = '_' + s2aligned
        s1aligned = s1[j-1] + s1aligned
        j-=1
    return [s1aligned,s2aligned]

def alignSequence(s1, s2):
    rows = len(s2)+1
    cols = len(s1)+1
    cost = [[0 for i in range(cols)] for j in range(rows)]

    # base case
    for i in range(len(s1)+1):
        cost[0][i] = i*delta
    for i in range(len(s2)+1):
        cost[i][0] = i*delta
    
    # iterative bottom-up table filling
    for i in range(1,rows):
        for j in range(1,cols):
            id1 = convertChar(s1[j-1])
            id2 = convertChar(s2[i-1])
            cost[i][j] = min(cost[i-1][j-1]+alphas[id1][id2], cost[i-1][j]+delta, cost[i][j-1]+delta)
    # print(cost[rows-1][cols-1])
    # print(getAlignments(cost,s1,s2))
    return cost

def alignSequenceDivideAndConquer(s1,s2):
    rows = len(s2)+1
    cols = len(s1)+1
    cost = [[0 for i in range(2)] for j in range(rows)]

    # base case
    for i in range(len(s2)+1):
        cost[i][0] = i*delta
    
    # iterative bottom-up table filling
    for i in range(1,cols):
        cost[0][i%2] = delta*i
        for j in range(1,rows):
            id1 = convertChar(s1[i-1])
            id2 = convertChar(s2[j-1])
            cost[j][i%2] = min(cost[j-1][(i-1)%2]+alphas[id1][id2], cost[j-1][i%2]+delta, cost[j][(i-1)%2]+delta)
    lastCostColumn = [i[(cols-1)%2] for i in cost]
    # print(lastCostColumn)
    return lastCostColumn

def getAlignments2(s1,s2):
    if len(s1) <= 2 or len(s2) <= 2:
        return getAlignments(alignSequence(s1,s2), s1, s2)
    l1 = len(s1)
    l2 = len(s2)
    forwardCost = alignSequenceDivideAndConquer(s1[0:l1//2+1], s2)
    backwardCost = alignSequenceDivideAndConquer(s1[l1//2+1:][::-1], s2[::-1])
    minVal = 10000000
    for i in range(l2 + 1):
        if (forwardCost[i] + backwardCost[l2 - i]) < minVal:
            minVal = forwardCost[i] + backwardCost[l2 - i]
            dividePoint = i
    
    left = getAlignments2(s1[0:l1//2+1], s2[0:dividePoint])
    right = getAlignments2(s1[l1//2+1:], s2[dividePoint:])
    return [left[0] + right[0], left[1] + right[1]]

# alignSequence(generateInput('ACTG', [3,6,1,1]),generateInput('TACG', [1,2,9,2]))
# alignSequenceDivideAndConquer(generateInput('ACTG', [3,6,1,1]),generateInput('TACG', [1,2,9,2]))
# print(getAlignments2(generateInput('ACTG', [3,6,1,1]),generateInput('TACG', [1,2,9,2])))

# alignSequenceDivideAndConquer(generateInput('ACTG', [3,6,1,1]),generateInput('TACG', [1,2,0]))
# alignSequence(generateInput('ACTG', [3,6,1,1]),generateInput('TACG', [1,2,0]))
# print(getAlignments2(generateInput('ACTG', [3,6,1,1]),generateInput('TACG', [1,2,0])))

# alignSequenceDivideAndConquer(generateInput('AGTC', [0,0,0,0,0]),generateInput('TACG', [1,1,1,1,1]))
# alignSequence(generateInput('AGTC', [0,0,0,0,0]),generateInput('TACG', [1,1,1,1,1]))
# print(getAlignments2(generateInput('AGTC', [0,0,0,0,0]),generateInput('TACG', [1,1,1,1,1])))

# alignSequenceDivideAndConquer(generateInput('TCGA', [3,7,15,31,62]),generateInput('TCGA', [3,7,15,31,63]))
# alignSequence(generateInput('TCGA', [3,7,15,31,62]),generateInput('TCGA', [3,7,15,31,63]))
# print(getAlignments2(generateInput('TCGA', [3,7,15,31,62]),generateInput('TCGA', [3,7,15,31,63])))

# alignSequenceDivideAndConquer(generateInput('ACGT', [3,6,1,1,5,6,7,8,9,20]),generateInput('TACG', [1,2,0,4,3,2,0,5,6,17]))
# alignSequence(generateInput('ACGT', [3,6,1,1,5,6,7,8,9,20]),generateInput('TACG', [1,2,0,4,3,2,0,5,6,17]))
print(getAlignments2(generateInput('ACGT', [3,6,1,1,5,6,7,8,9,20]),generateInput('TACG', [1,2,0,4,3,2,0,5,6,17])))

# getAlignments2('ACTG', 'TACG')
