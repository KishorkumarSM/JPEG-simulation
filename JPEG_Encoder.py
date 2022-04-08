from collections import defaultdict
import math
import numpy as np
from PIL import Image
import json
#from scipy.fftpack import dct, idct

from unit_functions import quantization, derive_code_length, derive_huffmann_code, convert_to_json

def main():
    #GETTING IMAGE
    image_file_name = "DSC00121.tiff"
    img = Image.open("../"+image_file_name)
    #RESIZING IMAGE AND CONVERTING IT INTO ARRAY
    resize_ratio = 25
    rows, columns = img.size
    print("Original image dimensions: ",img.size)
    rows = int(rows*(resize_ratio/100))
    columns = int(columns*(resize_ratio/100))
    rows = 360
    columns = 480
    img = img.resize((columns,rows))
    print("New image dimensions: ",img.size)
    #img.show()
    pixels=np.asarray(img)

    #INITIALIZING DCT BLOCK
    dctBlock=np.zeros((8,8),dtype=float)
    for i in range(8):
        for j in range(8):
            if(i==0):
                dctBlock[i][j]=1/math.sqrt(8)
            else:
                dctBlock[i][j]=math.sqrt(2/8)*math.cos((2*j+1)*i*math.pi/16)

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

    acStats = derive_code_length(acStats)
    huffmannCodeAc = derive_huffmann_code(acStats)

    DataAc = ""
    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
            for k in range(3):
                if i%8!=0 or j%8!=0:
                    #print(huffmannCodeAc[chr(pixels[i][j][k])][2:])
                    DataAc += huffmannCodeAc[chr(pixels[i][j][k])][2:]
    #print(DataAc)
    dcStats = derive_code_length(dcStats)
    huffmannCodeDc = derive_huffmann_code(dcStats)

    DataDc = ""
    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
            for k in range(3):
                if i%8==0 and j%8==0:
                    #print(huffmannCodeDc[chr(pixels[i][j][k])][2:])
                    DataDc += huffmannCodeDc[chr(pixels[i][j][k])][2:]
    
    mainDict = {}

    mainDict['shape'] = (rows, columns)
    mainDict['DC'] = convert_to_json(DataDc, huffmannCodeDc)
    mainDict['AC'] = convert_to_json(DataAc, huffmannCodeAc)

    #print(huffmannCodeAc)

    with open(image_file_name.split('.')[0]+"_encoded.json", "w") as outfile:
        json.dump(mainDict, outfile)
    
    print(len(DataDc))

if __name__ == '__main__':
    main()
