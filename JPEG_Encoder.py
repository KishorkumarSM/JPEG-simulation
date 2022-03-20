import math
import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

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
    return statsArray, stats

def deriveHuffmannCode(Stats):
    statsArray = []
    for key,value in acStats.items():
        statsArray.append([value,key])
    statsArray.sort()
    huffmannCode = {}
    code = bin(0)
    codeLength = 1
    for [length, character] in statsArray:
        while codeLength<length:
            codeLength+=1
            code += '0'
        huffmannCode[character] = code
        code = bin(int(code,2)+1)
    return huffmannCode

dctBlock=np.zeros((8,8),dtype=float)
for i in range(8):
    for j in range(8):
        if(i==0):
            dctBlock[i][j]=1/math.sqrt(8)
        else:
            dctBlock[i][j]=math.sqrt(2/8)*math.cos((2*j+1)*i*math.pi/16)

#GETTING IMAGE
img = Image.open('../DSC00121.tiff')

#RESIZING IMAGE AND CONVERTING IT INTO ARRAY
resize_ratio = 25
rows, columns = img.size
rows = int(rows*(resize_ratio/100))
columns = int(columns*(resize_ratio/100))
rows = 360
columns = 480
img = img.resize((columns,rows))
#print(img.size)
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
acStats = {}
dcStats = {}

for i in range(len(pixels)):
    for j in range(len(pixels[0])):
        for k in range(3):
            if i%8==0 and j%8==0:
                if pixels[i][j][k] in dcStats.keys():
                    dcStats[pixels[i][j][k]] += 1
                else:
                    dcStats[pixels[i][j][k]] = 1
            else:
                if pixels[i][j][k] in acStats.keys():
                    acStats[pixels[i][j][k]] += 1
                else:
                    acStats[pixels[i][j][k]] = 1

#for temp in statsArrayAc:
#    print(temp[0],end=", ")
#for key,value in acStats.items():
#    print(key,value)

#

statsArrayAc, acStats = deriveCodeLength(acStats)
huffmannCodeAc = deriveHuffmannCode(acStats)

DataAc = bin(0)
for i in range(len(pixels)):
    for j in range(len(pixels[0])):
        for k in range(3):
            if i%8 or j%8:
                DataAc += huffmannCodeAc[pixels[i][j][k]]

"""
deriveCodeLength(statsArrayDc,dcStats)
huffmannCodeDc = deriveHuffmannCode(dcStats)

DataDc = bin(0)
for i in range(len(pixels)):
    for j in range(len(pixels[0])):
        for k in range(3):
            if i%8==0 and j%8==0:
                DataDc += huffmannCodeDc[pixels[i][j][k]]
"""

print(huffmannCodeAc)
print(pixels[0][1])
#print(DataAc)
