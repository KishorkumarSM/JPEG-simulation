from collections import defaultdict
import math
import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct
import json

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

def deriveCodeLength(stats):
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

def deriveHuffmannCode(Stats):
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

dctBlock=np.zeros((8,8),dtype=float)
for i in range(8):
    for j in range(8):
        if(i==0):
            dctBlock[i][j]=1/math.sqrt(8)
        else:
            dctBlock[i][j]=math.sqrt(2/8)*math.cos((2*j+1)*i*math.pi/16)

def bin_to_chr(b):
    result = 0
    for i in range(len(b)):
        result += (2**(i))*int(b[-i-1])
    return chr(result)

def jsonConvert(Data, huffmancode):
    r= len(Data)%7
    reminder= Data[-r:]
    output = ""
    for i in range(len(Data)//7):
        #print(bin_to_chr(Data[i*7:i*7+7]))
        output += bin_to_chr(Data[i*7:i*7+7])
    #print(output)
    return {'remainder':reminder, 'data':output, 'huffmancode':huffmancode}


def main():
    #GETTING IMAGE
    image_file_name = "DSC00121.tiff"
    img = Image.open("../"+image_file_name)
    #RESIZING IMAGE AND CONVERTING IT INTO ARRAY
    resize_ratio = 25
    rows, columns = img.size
    print(img.size)
    rows = int(rows*(resize_ratio/100))
    columns = int(columns*(resize_ratio/100))
    rows = 360
    columns = 480
    img = img.resize((columns,rows))
    print(img.size)

    #img.show()
    pixels=np.asarray(img)

    #APPLYING DCT AND QAUNTIZATION
    for i in range(len(pixels)//8):
        for j in range(len(pixels[0])//8):
            for k in range(3):
                #print(i,j,k)
                imgBlock = pixels[i*8:(i+1)*8,j*8:(j+1)*8,k].reshape((8,8)).copy()
                for x in range(8):
                    for y in range(8):
                        imgBlock[x][y]-=128
                #imgBlock1=dct(dct(imgblock,axis=0),axis=1)
                #imgBlock2=reconstruct(quantization(imgblock1))
                #imgBlock3=idct(idct(imgblock,axis=0),axis=1)
                imgBlock1 = np.dot(np.dot(dctBlock,imgBlock),dctBlock.T)
                imgBlock2 = quantization(imgBlock1)
                #imgBlock3 = (np.dot(np.dot(dctBlock.T,imgBlock2),dctBlock).round()+128).astype(int)
                for x in range(8):
                    for y in range(8):
                        pixels[i*8+x][j*8+y][k]=int(imgBlock2[x][y])

    #GETTING STATISTICS OF AC AND DC VALUES
    acStats = defaultdict(lambda: int(0))
    dcStats = defaultdict(lambda: int(0))

    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
            for k in range(3):
                if i%8==0 and j%8==0:
                    dcStats[pixels[i][j][k]] += 1
                else:
                    acStats[pixels[i][j][k]] += 1

    acStats = deriveCodeLength(acStats)
    huffmannCodeAc = deriveHuffmannCode(acStats)

    DataAc = ""
    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
            for k in range(3):
                if i%8!=0 or j%8!=0:
                    #print(huffmannCodeAc[chr(pixels[i][j][k])][2:])
                    DataAc += huffmannCodeAc[chr(pixels[i][j][k])][2:]
    #print(DataAc)
    dcStats = deriveCodeLength(dcStats)
    huffmannCodeDc = deriveHuffmannCode(dcStats)

    DataDc = ""
    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
            for k in range(3):
                if i%8==0 and j%8==0:
                    #print(huffmannCodeDc[chr(pixels[i][j][k])][2:])
                    DataDc += huffmannCodeDc[chr(pixels[i][j][k])][2:]
    
    mainDict = {}

    mainDict['shape'] = (rows, columns)
    mainDict['DC'] = jsonConvert(DataDc, huffmannCodeDc)
    mainDict['AC'] = jsonConvert(DataAc, huffmannCodeAc)

    #print(huffmannCodeAc)

    with open(image_file_name.split('.')[0]+"_encoded.json", "w") as outfile:
        json.dump(mainDict, outfile)

if __name__ == '__main__':
    main()
