import json
from turtle import shape

from unit_functions import ord_to_bin

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



def main():
    image_file_name = "DSC00121.tiff"
    with open(image_file_name.split('.')[0]+"_encoded.json", 'r') as openfile:
        mainDict = json.load(openfile)

    print(len(mainDict['DC']['data']))
    output = ""
    #print(mainDict['DC']['data'][0])
    for c in mainDict['DC']['data']:
        output += ord_to_bin(ord(c))
    
    tree = huffmanTree()
    hc = mainDict['DC']['huffmancode']
    for k in hc.keys():
        tree.add(str(hc[k])[2:],(k))
    
    dc_output = tree.decode(output)
    print(mainDict["shape"], len(dc_output))
if __name__ == "__main__":
    main()