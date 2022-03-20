from googledrivedownloader import GoogleDriveDownloader as gdd

gdd.download_file_from_google_drive(file_id='https://drive.google.com/file/d/13Kro0PwDfvHPoxPz1jNnJSZVoaSduVFd/view?usp=sharing',
                                    dest_path='./image.zip',
                                    unzip=True)

# BETTER SORTING
#print(len(huffmannTableAc))
"""
for i in range(len(huffmannTableAc)-1,0,-1):
    if z[0]<=huffmannTableAc[i][0]:
        huffmannTableAc = huffmannTableAc[:i+1] + [z] + huffmannTableAc[i+1:]
        break
#if len(huffmannTableAc)<9:
    #print(huffmannTableAc)
    #print(z)
    #print()
if z[0]>huffmannTableAc[0][0]:
    huffmannTableAc = [z] + huffmannTableAc
"""
