import json
from PIL import Image
import numpy as np
import math

from unit_functions import ord_to_bin, reconstruct

class huffmanTree:
    def __init__(self):
        self.val = None
        self.left = None
        self.right = None
    def add(self,key, value):
        if len(key)>0:
            if key[0]=='0':
                if self.left == None:
                    self.left = huffmanTree()
                self.left.add(key[1:],value)
            elif key[0]=='1':
                if self.right == None:
                    self.right = huffmanTree()
                self.right.add(key[1:],value)
        else:
            self.val = value
    def decode(self, data):
        result=[]
        temp = self
        for c in data:
            if c=="0":
                temp = temp.left
            elif c=="1":
                temp = temp.right
            if temp.val != None:
                result.append(temp.val)
                temp=self
        return result

def retrieve(dict):
    output = ""
    for c in dict['data']:
        output += ord_to_bin(ord(c))
    output += dict['remainder']

    tree = huffmanTree()
    hc = dict['huffmancode']
    for k in hc.keys():
        tree.add(str(hc[k]),(k))
    return tree.decode(output)
    

def main():
    image_file_name = "DSC00121.tiff"
    with open(image_file_name.split('.')[0]+"_encoded.json", 'r') as openfile:
        mainDict = json.load(openfile)

    dc_output = retrieve(mainDict['DC'])
    ac_output = retrieve(mainDict['AC'])
    rows, columns = mainDict['shape']
    pixels = np.zeros((rows,columns,3), dtype=int)

    dc_index = 0
    ac_index = 0
    for i in range (len(pixels)):
        for j in range (len(pixels[0])):
            if i%8==0 and j%8==0:
                for k in range(3):
                    pixels[i][j][k] = ord(dc_output[dc_index])
                    dc_index += 1
            else:
                for k in range(3):
                    pixels[i][j][k] = ord(ac_output[ac_index])
                    ac_index += 1

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
                imgBlock1 = reconstruct(imgBlock)
                imgBlock2 = (np.dot(np.dot(dctBlock.T,imgBlock1),dctBlock).round()+128).astype(int)
                for x in range(8):
                    for y in range(8):
                        pixels[i*8+x][j*8+y][k]=int(imgBlock2[x][y])
    print(type(pixels[0][0][0]))
    print(pixels)
    img = Image.fromarray(pixels)
    img.show()
    



if __name__ == "__main__":
    main()