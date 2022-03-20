from PIL import Image,ImageOps
import numpy as np

import math

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

def dctTransform():
    dct=np.zeros((8,8),dtype=float)
    for i in range(8):
        for j in range(8):
            if(i==0):
                dct[i][j]=1/math.sqrt(8)
            else:
                dct[i][j]=math.sqrt(2/8)*math.cos((2*j+1)*i*math.pi/16)
    return dct

def inversedct(r,t):
    return (np.dot(np.dot(t.T,r),t).round()+128).astype(int)

img=Image.open(r"rgbImage.jpg")
img=img.resize((256,256))
grayimg=ImageOps.grayscale(img)
pixel=np.array(grayimg.getdata())
pixel=pixel.reshape((256,256))
grayimg.show()
i=0
j=0
newpixel=np.zeros((256,256))
while(i<256):
  j=0
  while(j<256):
    bl=(pixel[i:i+8,j:j+8]).reshape((8,8)).copy()
    Tm=dctTransform()
    for k1 in range(8):
        for k2 in range(8):
            bl[k1][k2]=bl[k1][k2]-128
    D=np.dot(np.dot(Tm,bl),Tm.T)
    Ans=quantization(D)
    bl2=inversedct(reconstruct(Ans),Tm)
    for ii in range(8):
      for jj in range(8):
        newpixel[i+ii][j+jj]=bl2[ii][jj]
    j+=8
  i+=8

#print(newpixel.shape)
invd=Image.fromarray(newpixel)
#print(newpixel,pixel)
invd.show()