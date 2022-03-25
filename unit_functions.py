import numpy as np

def quantization(bl):
    q=np.array([[16,11,10,16,24,40,51,61]
    ,[12,12,14,19,26,58,60,55],
    [14,13,16,24,40,57,69,56],
    [14,17,22,29,51,87,80,62],
    [18,22,37,56,68,109,103,77],
    [24,35,55,64,81,104,113,92],
    [49,64,78,87,103,121,120,101],
    [72,92,95,98,112,100,103,99]])
    return np.divide(bl,q).astype(int)

def reconstruct(m):
    q=np.array([[16,11,10,16,24,40,51,61]
    ,[12,12,14,19,26,58,60,55],
    [14,13,16,24,40,57,69,56],
    [14,17,22,29,51,87,80,62],
    [18,22,37,56,68,109,103,77],
    [24,35,55,64,81,104,113,92],
    [49,64,78,87,103,121,120,101],
    [72,92,95,98,112,100,103,99]])
    return np.multiply(q,m)

def derive_code_length(stats):    #returns dictionary of code lengths of each character
    #SORTING STATISTICS AND INITIALISING CANONICAL TABLES
    statsArray = []
    for key,value in stats.items():
        statsArray.append([value,[key]])
        stats[key] = 0
    statsArray.sort(reverse=True)
    #CALCULATING CANONICAL CODE LENGTHS
    while len(statsArray)!=1:
        #print(len(statsArray))
        x, y = statsArray[-1], statsArray[-2]
        z = [x[0]+y[0],x[1]+y[1]]
        for zs in z[1]:
            stats[zs] += 1
        statsArray = statsArray[:-2]
        statsArray.append(z)
        statsArray.sort(reverse=True)
        # BETTER SORTING
    return stats

def derive_huffmann_code(Stats):  #returns dictionary of canonical huffmann code using codelengths dictionary
    statsArray = []
    for key,value in Stats.items():
        statsArray.append([value,key])
    statsArray.sort()
    huffmannCode = {}
    code = bin(0)
    codeLength = 1
    for [length, character] in statsArray:
        while codeLength<length:
            codeLength+=1
            code += '0'
        huffmannCode[chr(character)] = code
        code = bin(int(code,2)+1)
    return huffmannCode

def bin_to_chr(b):
    result = 0
    for i in range(len(b)):
        result += (2**(i))*int(b[-i-1])
    return chr(result)

def convert_to_json(Data, huffmancode):
    r= len(Data)%7
    reminder= Data[-r:]
    output = ""
    for i in range(len(Data)//7):
        #print(bin_to_chr(Data[i*7:i*7+7]))
        output += bin_to_chr(Data[i*7:i*7+7])
    #print(output)
    return {'remainder':reminder, 'data':output, 'huffmancode':huffmancode}
