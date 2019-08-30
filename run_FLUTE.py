import sys, os
import csv
import time
import numpy as np
import mysql.connector
import datetime
import pandas as pd
import testString
import testFunc
from sklearn import metrics
from makeArrays_REACH import saveArrays
import argparse
#This script takes uniprot IDs and converts them to a list of string IDs
#REACH format, last updated for OUP databases, August 2019

def get_args():

        parser = argparse.ArgumentParser(description="Identify high-confidence interactions in machine reading output.")

        parser.add_argument('username', type=str,help="MySQL username")
        parser.add_argument('password', type=str,help="MySQL password")
        parser.add_argument('host', type=str,help="MySQL host")
        parser.add_argument('DB', type=str,help="MySQL database name")

        parser.add_argument('file_in', type=str,help="Input file")
        parser.add_argument('filtered_reading', type=str,help="Filtered reading output filename")
        parser.add_argument('scores', type=str,help="Database scores output filename")
        
        args = parser.parse_args()

        return(args)

def convID(db_user,db_pass,db_host,db_name,X):

    db_cnx  = mysql.connector.connect(user = db_user, password = db_pass, host = db_host, database = db_name, charset='utf8')
    cursor = db_cnx.cursor()

    for i in range(X.shape[0]):

        commonName = str(X[i,1])
        unip = str(X[i,0]).strip("\n")

        if(unip):

            int_query = ("SELECT stringID FROM unistringmapping WHERE uniID = %s OR uniID= %s OR ogs= %s") 

            cursor.execute(int_query,(unip,commonName,commonName))

            for s in cursor:

                X[i,2] = s[0]


    cursor.close()
    db_cnx.close()

    return(X)


def findInts(db_user,db_pass,db_host,db_name,ints,es,ts,ds):

    #Specify user, password, database, host, database
    db_cnx  = mysql.connector.connect(user = db_user, password = db_pass, host = db_host, database = db_name, charset='utf8')
    cursor = db_cnx.cursor(buffered=True)
    cursor2 = db_cnx.cursor(buffered=True)
    cursor3 = db_cnx.cursor(buffered=True)
    cursor4 = db_cnx.cursor(buffered=True)
    cursor5 = db_cnx.cursor(buffered=True)
    logs = []

    st = time.time()

    print(ints[:,10])

    for i in range(ints.shape[0]):
    
        #IC interaction ID's 
        id1 = str(ints[i,0]) #this is actually the name
        name1 = str(ints[i,1]) #this is actually the id
        uid1 = str(ints[i,2])
        sid1 = str(ints[i,3])
        chemid1 = str(ints[i,6])
        goid1 = str(ints[i,7])
        id2 = str(ints[i,8])
        name2 = str(ints[i,9])
        uid2 = str(ints[i,10])
        sid2 = str(ints[i,11])
        chemid2 = str(ints[i,14])
        goid2 = str(ints[i,15])

        #Query STRING DB
        if(sid1 and sid2):

            #Select all matching interactions from STRING DB
            int_query = ("SELECT protein1, protein2, escore,tscore,ascore,dscore FROM ppi_detail_v11 WHERE ((protein1 = %s AND protein2 = %s ) OR (protein1 = %s AND protein2 = %s)) AND (escore>=%s AND tscore>=%s AND dscore>=%s)") 
            cursor.execute(int_query, (sid1,sid2,sid2,sid1,es,ts,ds))


            for (protein1, protein2,escore,tscore,ascore,dscore) in cursor:

                logs.append([name1,name2,escore,tscore,dscore])

        if((uid1 and uid2) and (uid1!=uid2)):

            long_upid1 = "uniprotkb:" + uid1.upper()
            long_upid2 = "uniprotkb:" +uid2.upper()

            int_query_r = ("SELECT upid1,upid2 FROM reactome WHERE ((upid1=%s AND upid2=%s) or (upid1=%s AND upid2=%s))")
            cursor2.execute(int_query_r,(long_upid1,long_upid2,long_upid2,long_upid1))

            for (upid1, upid2) in cursor2:

                logs.append([uid1,uid2, "", "", ""])


        #Biogrid
        int_query3 = ("SELECT ogsA,ogsB FROM biogrid WHERE (ogsA = %s AND ogsB = %s) OR (ogsA = %s AND ogsB = %s)") 
        cursor3.execute(int_query3, (name1,name2,name1,name2))

        for (bi1,bi2) in cursor3:
            logs.append([ogsA,id1,ogsB,id2,"","",""])

        #Go terms
        int_q3 = ("SELECT goterm,id1,evidence FROM goterms WHERE ((goterm = %s AND id1 = %s) OR (goterm = %s AND id1 = %s))")
        cursor5.execute(int_q3, (goid1,uid2,goid2,uid1))

        for (goterm,id1,evidence) in cursor5:

            logs.append([name1,name2, evidence,"",""])

        #STITCH
        int_q2 = ("SELECT chem,prot,exp,text,data FROM pci_detail WHERE ((chem= %s AND prot = %s) OR (chem= %s AND prot = %s))") 
        cursor4.execute(int_q2, (chemid1,sid2,chemid2,sid1))

        for (chem, prot,exp,pred,data) in cursor4:

            if(chemid1):
                logs.append([name1,name2, exp, pred, data])


            else:
                logs.append([name1, name2,exp, pred, data])



    strLogs = np.array(logs)
    npLogs = strLogs.reshape((-1,5))

    cursor.close()
    cursor2.close()
    cursor3.close()
    cursor4.close()
    cursor5.close()
    db_cnx.close()

    return(npLogs)

def uni_only(allInts):

    rel_ints = []
    nm = []

    for i in range(0,allInts.shape[0]):
        nm1 = allInts[i,0]
        nm2 = allInts[i,4]
        type1 = allInts[i,1].lower()
        type2 = allInts[i,5].lower()
        up_id1 = str(allInts[i,3])
        up_id2 = str(allInts[i,7])

        if(type1=='protein' or type2=='protein'):

            rel_ints.append(str(nm1).lower())
            rel_ints.append(up_id1.lower())
            rel_ints.append(str(nm2).lower())
            rel_ints.append(up_id2.lower())

    return(rel_ints)

def getChem(X):

    for z in range(X.shape[0]):

        id1 = X[z,1] #chem or prot
        id2 = X[z,9]

        if(id1.isdigit()):
            num_z =  8 - len(id1) 
            trailing_z = ''

            for j in range(num_z):

                trailing_z = trailing_z + "0"

            cidm_id = "CIDm" + trailing_z + id1

            X[z,6] = cidm_id


        if(id2.isdigit()):
            num_z =  8 - len(id2) 
            trailing_z = ''

            for j in range(num_z):

                trailing_z = trailing_z + "0"

            cidm_id = "CIDm" + trailing_z + id2

            X[z,14] = cidm_id


    return(X)

def getGo(a):

    for i in range(a.shape[0]):

        if(a[i,1].find("GO:")!=-1):
            a[i,7] = a[i,1].upper()
        if(a[i,9].find("GO:")!=-1):
            a[i,15] = a[i,9].upper()

    return(a)
    
    
def main():

    args = get_args()


    db_user = args.username
    db_pass = args.password
    db_name = args.DB
    db_host = args.host

    f_in=args.file_in


    escores=[0]
    tscores=[0]
    dscores= [0]


    for es in escores:

        for ts in tscores:

            for ds in dscores:

                start = time.time()

                allInts= saveArrays(f_in)

                getID = np.append(allInts[:,3],allInts[:,7])

                uniqID = np.unique(getID)

                blankDict = np.zeros((uniqID.shape[0],3),dtype=">U50")
                blankDict[:,0] = uniqID

                for i in range(blankDict.shape[0]):
                    for j in range(allInts.shape[0]):
                        if(allInts[j,3]==blankDict[i,0]):
                           blankDict[i,1] =allInts[j,0]

                        elif(allInts[j,6]==blankDict[i,0]):
                            blankDict[i,1] = allInts[j,4]

                nameDict = convID(db_user,db_pass,db_host,db_name,blankDict)
                all_ids = uni_only(allInts) #returns lower-case interactions:pis/pcis/pgis

                npIDs = np.array(all_ids).reshape(-1,4).astype(">U750")

                #print(npIDs)

                intComp = np.empty((npIDs.shape[0],17),dtype=">U750")
                intComp[:,0] = npIDs[:,0] #element1 name
                intComp[:,1] = np.char.upper(npIDs[:,1]) # element 1 id
                intComp[:,8] = npIDs[:,2]        
                intComp[:,9] = np.char.upper(npIDs[:,3])


                intComp_c = getChem(intComp) #get cidm ids
                intComp = getGo(intComp_c)

                for i in range(intComp.shape[0]):
                    id1 = intComp[i,1].upper()
                    id2 = intComp[i,9].upper()

                    for j in range(nameDict.shape[0]):

                        if(id1==nameDict[j,0]):
                            intComp[i,3] = str(nameDict[j,2])

                            if(nameDict[j,2]):
                                intComp[i,2] = str(nameDict[j,0])

                        if(id2==nameDict[j,0]):
                            intComp[i,11] = str(nameDict[j,2])

                            if(nameDict[j,2]):
                                intComp[i,10] = str(nameDict[j,0])

                outp = args.scores
                outp2 = args.filtered_reading

                fInts = findInts(db_user,db_pass,db_host,db_name,intComp,es,ts,ds) 
                np.savetxt(outp2,fInts, delimiter=",",fmt='%s %s %s %s %s',encoding="utf-8")

                xl = f_in

                IC_df = pd.read_excel(xl)
                IC = IC_df.as_matrix()

                rc = fInts.shape[0]
                rc2 = IC.shape[0]

                with open(outp, 'w+', encoding="utf-8") as outfile:

                    for n in range(fInts.shape[0]):

                        for k in range(rc2):

                            ic1 = str(IC[k,3])
                            ic2 = str(IC[k,7])
                            ic3 = str(IC[k,12])

                            if((fInts[n,0]==ic1 and fInts[n,1]==ic2) or (fInts[n,0]==ic1 and fInts[n,1]==ic3)):

                                for m in range(IC.shape[1]):

                                    outfile.write(str(IC[k,m]))
                                    outfile.write("\t")

                                outfile.write(fInts[n,2])
                                outfile.write("\t")
                                outfile.write(str(fInts[n,3])) 
                                outfile.write("\t")
                                outfile.write(str(fInts[n,4]))

                                outfile.write("\n") 

                outfile.close()
                end = time.time() - start
                print("File filtered: " + str(f_in) + " Time: " + str(end) + " seconds")

if __name__ == '__main__':
    main()