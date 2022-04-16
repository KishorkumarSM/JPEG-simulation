from unit_functions import ord_to_bin, bin_to_chr

print(ord('a'))

print(bin_to_chr(ord_to_bin(ord('a'))))

print([1,2]+[3,4])

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

#print(int("100"))