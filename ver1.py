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
    print(cost[rows-1][cols-1])
    print(getAlignments(cost,s1,s2))

alignSequence(generateInput('ACGT', [3,6,1,1,5,6,7,8,9,20]),generateInput('TACG', [1,2,0,4,3,2,0,5,6,17]))
