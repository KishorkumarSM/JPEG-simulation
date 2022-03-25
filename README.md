# JPEG-simulation
## About
A lossy JPEG compression program in python using PIL library. The program uses Discrete cosine transform, quantisation and entropy coding(Huffman) to perform a complete simulation of the JPEG compression technique. This compressed text data is then reverse processed to obtain the original high quality image.
- JPEG_Encoder - Compressess and writes the image file into a json file.
- JPEG_Decoder - Read the json file , decompressess and displays the image without the need for actual image file.
- Input - We use .tiff (Tagged Image File Format) as input images, as they are the closest to bitmapped image formats that are easily available. This is needed in order to understand the compressing capacity of the JPEG algorithm.

## Sample input image file
Since, tiff files are too large to store in github repo. Here's the link to a sample image:
https://drive.google.com/file/d/13Kro0PwDfvHPoxPz1jNnJSZVoaSduVFd/view?usp=sharing
