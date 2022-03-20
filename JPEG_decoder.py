import json

from JPEG_Encoder import reconstruct

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


def ord_to_bin(n):
    result = ""
    while n!=0:
        result = chr(n%2) + result
        n//=2
    while len(result)<7:
        result = '0'+result
    return result

def main():
    image_file_name = "DSC00121.tiff"
    with open(image_file_name.split('.')[0]+"_encoded.json", 'r') as openfile:
        mainDict = json.load(openfile)
    output = ""
    #print(mainDict['DC']['data'][0])
    for c in mainDict['DC']['data']:
        output += ord_to_bin(ord(c))
    
    tree = huffmanTree()
    hc = mainDict['DC']['huffmancode']
    for k in hc.keys():
        tree.add(str(hc[k])[2:],ord(k))
    
    


if __name__ == "__main__":
    main()