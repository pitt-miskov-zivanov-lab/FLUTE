import sys, os
import re
import numpy as np

    #pass all interactions and paper IDs
    #open OA file and read to array
    #find pmcid for all interactions and get associated year
    #pass interactions and values back to main

def main():

    paperInfo = np.genfromtxt("oa_file_list.txt", dtype=">U50",delimiter="\t",skip_header=1)

    data = paperInfo[:,1:4]

    for x in range(data.shape[0]):

        xtr = data[x,0]

        mtch = re.search(r'[18|19|20]+\d{2}',xtr)

        if(mtch):

            yr = int(mtch[0])

            print(yr)

            data[x,0] = yr

    np.save("pmcidYears.npy",data)

if __name__ == '__main__':
    main()
