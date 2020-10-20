import sys, os
import csv
import time
import numpy as np
import mysql.connector
import datetime
import pandas as pd
from sklearn import metrics
import argparse
import re
#This script takes uniprot IDs and converts them to a list of string IDs
#REACH format, last updated for OUP databases, August 2019

def getRelatedPapers(db_user,db_pass,db_host,db_name,prot):

    tmp1 = float(time.time())

    all_prot=[]

    if (prot.find(",")!=-1):

        all_prot = prot.split(",")

    else:

        all_prot.append(prot)

    refLogs = []
    
    db_cnx  = mysql.connector.connect(user = db_user, password = db_pass, host = db_host, database = db_name, charset='utf8')
    cursorGetProts = db_cnx.cursor()
    cursorOGS = db_cnx.cursor()
    cursorBG = db_cnx.cursor()

    for a in all_prot:

        uniName = "uniprotkb:" + a

        ogs = ""

        ogsQuery = ("SELECT ogs FROM unistringmapping WHERE uniID = %s or uniID= %s")
        cursorOGS.execute(ogsQuery, (a, uniName))

        for nm in cursorOGS:
            ogs = nm[0]

        cursorOGS.close()


        bgQuery = ("SELECT PubID from biogrid WHERE ogsA = %s or ogsB = %s")
        cursorBG.execute(bgQuery,(ogs,ogs))


        for bg in cursorBG:

            refLogs.append(str(bg[0]))


        fQuery = ("SELECT ref from reactome where upID1 = %s or upID2 = %s")
        cursorGetProts.execute(fQuery, (uniName,uniName))


        for (r) in cursorGetProts:

            allRefs = r[0].split("|")

            for indRef in allRefs:
                refLogs.append(indRef)


<<<<<<< HEAD
=======

>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
    idConv = np.load("pmcidYears.npy")
    final_papers = []

    refLogsUniq = list(set(refLogs))

    for ref in refLogsUniq:

        r = "PMID:"+ref


        for i in range(idConv.shape[0]):

            if(idConv[i,2]==r):

                final_papers.append(idConv[i,1])


    fp = np.array(final_papers).reshape(-1,)
    np.savetxt("PMCPapers.txt", fp, fmt="%s")


def getRelatedInts(db_user,db_pass,db_host,db_name,f):

    d = pd.read_excel(f)

    data = d.values

    ppr = list(set(data[:,11]))

    idConv = np.load("pmcidYears.npy")

    pmids = []

    for p in ppr:

        for i in range(idConv.shape[0]):

            if(idConv[i,1]==p):

                pmids.append(idConv[i,2].strip("PMID:"))


    db_cnx  = mysql.connector.connect(user = db_user, password = db_pass, host = db_host, database = db_name, charset='utf8')
    cursorGetProts = db_cnx.cursor()

    log = []

    for pmid in pmids:

        pmidLong = "PMID0" + pmid

        paperQuery = "SELECT protein1,protein2,mode,sources from actions_source WHERE sources=%(sources)s"
        cursorGetProts.execute(paperQuery,{'sources':pmidLong})

        for (p1,p2,m,s) in cursorGetProts:

            log.append([p1,p2,m,s])

    cursorGetProts.close()

    cursorGetProtInfo = db_cnx.cursor(buffered=True)

    data = np.empty((len(log),3))

    for directedInt in log:

        infoQuery = "SELECT external_id from protein_info where internal_id=%(internal_id)s"

        cursorGetProtInfo.execute(infoQuery,{'internal_id':directedInt[0]})

<<<<<<< HEAD

        cursorGetProtInfo.execute(infoQuery,{'internal_id':directedInt[1]})


    ll = np.array(log)

    paperNum = list(set(log[:,3]))

    
=======
        print(cursorGetProtInfo.fetchone())

        cursorGetProtInfo.execute(infoQuery,{'internal_id':directedInt[1]})

        print(cursorGetProtInfo.fetchall())



    ll = np.array(log)

    print(log)

    paperNum = list(set(log[:,3]))

    

    print(paperNum)


    
>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
def getRecentPapers(f):

    #this function should search the OA file and find all interactions occuring in papers less than X years old

<<<<<<< HEAD
    d = pd.read_excel(f)
    data = d.values
    ppr = data[:,11]
=======

    tmp1 = float(time.time())

    d = pd.read_excel(f)

    data = d.values

    ppr = data[:,11]

>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
    yrs = np.load("pmcidYears.npy")

    s = []

    with open("years.txt", 'w+') as outf:

        for p in ppr:
<<<<<<< HEAD
            for y in yrs:
=======

            for y in yrs:

>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
                if(y[1]==p):

                    outf.write(y[0])
            

            outf.write("\n")

<<<<<<< HEAD
    outf.close()

=======

    outf.close()

    tmp2 =float(time.time()) - tmp1

>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3

def getDups(f):


    df = pd.read_excel(f)
    data = df.values
    vals = np.empty((data.shape[0],4),dtype=">U50")

    vals[:,0] = data[:,3]
    vals[:,1] = data[:,7]
    vals[:,2] = data[:,11]
    vals[:,3].fill(1)

    for i in range(vals.shape[0]):

        for j in range(vals.shape[0]):

            if(vals[i,0]==vals[j,0] and vals[i,1]==vals[j,1] and vals[i,2]!=vals[j,2]):

<<<<<<< HEAD
=======
                print("Duplicated interaction")

>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
                vals[i,3] = int(vals[i,3]) + 1

    with open("duplicateNum.txt", "w+") as outf:

        for i in range(vals.shape[0]):

            outf.write(vals[i,3])
            outf.write("\n")


    outf.close()

    tmp = np.delete(vals,[2],axis=1)

    dupVals = np.unique(tmp, axis=0)

def get_args():

        parser = argparse.ArgumentParser(description="Identify high-confidence interactions in machine reading output.")

        parser.add_argument('username', type=str,help="MySQL username")
        parser.add_argument('password', type=str,help="MySQL password")
        parser.add_argument('host', type=str,help="MySQL host")
        parser.add_argument('DB', type=str,help="MySQL database name")

        parser.add_argument('file_in', type=str,help="Input file")
        parser.add_argument('filtered_reading', type=str,help="Filtered reading output filename")
        parser.add_argument('scores', type=str,help="Database scores output filename")
<<<<<<< HEAD
        parser.add_argument('-g','--get_duplicates',action="store_true",default=False,help="Whether to output duplicate interactions")
        parser.add_argument('-p','--recentPapers',action="store_true",default=False,help="If true, exempts recent papers from filtering")
        parser.add_argument('-q','--protQuery',help="If true, finds interactions for protein ID") 
        parser.add_argument('-r','--relatedInts',action="store_true",default=False,help="If true, adds additional interactions related to input.")      
=======
>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
        
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
<<<<<<< HEAD
        nm2 = allInts[i,3]
        type1 = allInts[i,2].lower()
        type2 = allInts[i,5].lower()
        up_id1 = str(allInts[i,1])
        up_id2 = str(allInts[i,4])
=======
        nm2 = allInts[i,4]
        type1 = allInts[i,1].lower()
        type2 = allInts[i,5].lower()
        up_id1 = str(allInts[i,3])
        up_id2 = str(allInts[i,7])
>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3

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
    f_in = args.file_in
<<<<<<< HEAD
    recentPapers = args.recentPapers
    get_duplicates = args.get_duplicates
    protQuery = args.protQuery
    relatedInts = args.protQuery
=======

>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3

    escores=[0]
    tscores=[0]
    dscores= [0]

<<<<<<< HEAD
    if(recentPapers):
        getRecentPapers(f_in)

    if(get_duplicates):
        getDups(f_in)

    if (protQuery):

        getRelatedPapers(db_user,db_pass,db_host,db_name,protQuery)

    if(relatedInts):

        getRelatedInts(db_user,db_pass,db_host,db_name,f_in)
=======
    getRecentPapers(f_in)

    getDups(f_in)

    protQuery = "P35606" 

    getRelatedPapers(db_user,db_pass,db_host,db_name,protQuery)

    getRelatedInts(db_user,db_pass,db_host,db_name,f_in)
>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3

    for es in escores:

        for ts in tscores:

            for ds in dscores:

                start = time.time()
<<<<<<< HEAD
                df= pd.read_excel(f_in)


                #please double-check header ids
                a = df[['RegulatedName','RegulatedID','RegulatedType','RegulatorName','RegulatorID','RegulatorType','PaperID']]

                allInts= a.values
                
                getID = np.append(allInts[:,1],allInts[:,4]).astype(">U50")
=======

                #fix this!!
                a= pd.read_excel(f_in)

                allInts= a.values

                getID = np.append(allInts[:,3],allInts[:,7]).astype(">U50")

                #print(getID)

>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
                uniqID = np.unique(getID)

                blankDict = np.zeros((uniqID.shape[0],3),dtype=">U50")
                blankDict[:,0] = uniqID

                for i in range(blankDict.shape[0]):
                    for j in range(allInts.shape[0]):
<<<<<<< HEAD
                        if(allInts[j,1]==blankDict[i,0]):
                           blankDict[i,1] =allInts[j,0]

                        elif(allInts[j,4]==blankDict[i,0]):
                            blankDict[i,1] = allInts[j,3]

                nameDict = convID(db_user,db_pass,db_host,db_name,blankDict)

                all_ids = uni_only(allInts) #returns lower-case interactions:ppis/pcis/pbpis
                npIDs = np.array(all_ids).reshape(-1,4).astype(">U750")

=======
                        if(allInts[j,3]==blankDict[i,0]):
                           blankDict[i,1] =allInts[j,0]

                        elif(allInts[j,6]==blankDict[i,0]):
                            blankDict[i,1] = allInts[j,4]

                nameDict = convID(db_user,db_pass,db_host,db_name,blankDict)
                all_ids = uni_only(allInts) #returns lower-case interactions:pis/pcis/pgis

                npIDs = np.array(all_ids).reshape(-1,4).astype(">U750")

                #print(npIDs)

>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
                intComp = np.empty((npIDs.shape[0],17),dtype=">U750")
                intComp[:,0] = npIDs[:,0] #element1 name
                intComp[:,1] = np.char.upper(npIDs[:,1]) # element 1 id
                intComp[:,8] = npIDs[:,2]        
                intComp[:,9] = np.char.upper(npIDs[:,3])

<<<<<<< HEAD
=======

>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
                intComp_c = getChem(intComp) #get cidm ids
                intComp = getGo(intComp_c)

                for i in range(intComp.shape[0]):
                    id1 = intComp[i,1].upper()
                    id2 = intComp[i,9].upper()

                    for j in range(nameDict.shape[0]):

<<<<<<< HEAD
                        if(id1==nameDict[j,0].upper()):
=======
                        if(id1==nameDict[j,0]):
>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
                            intComp[i,3] = str(nameDict[j,2])

                            if(nameDict[j,2]):
                                intComp[i,2] = str(nameDict[j,0])

<<<<<<< HEAD
                        if(id2==nameDict[j,0].upper()):
=======
                        if(id2==nameDict[j,0]):
>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
                            intComp[i,11] = str(nameDict[j,2])

                            if(nameDict[j,2]):
                                intComp[i,10] = str(nameDict[j,0])

                outp = args.scores
                outp2 = args.filtered_reading

                fInts = findInts(db_user,db_pass,db_host,db_name,intComp,es,ts,ds) 
<<<<<<< HEAD
=======

                #print(fInts)
>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3
                np.savetxt(outp2,fInts, delimiter=",",fmt='%s %s %s %s %s',encoding="utf-8")

                xl = f_in

                IC_df = pd.read_excel(xl)
                IC = IC_df.values

                fUniq = np.unique(fInts, axis=0)
<<<<<<< HEAD
                fInts = fUniq

                rowDf = IC_df[['RegulatedID','RegulatorID']]
                rowIDs  = rowDf.values

                with open(outp, 'w+', encoding="utf-8") as outfile:

                    for n in range(fInts.shape[0]): #go through all original ints and find evidence

                        for k in range(IC.shape[0]): 

                            ic1 = str(rowIDs[k,0]).lower()
                            ic2 = str(rowIDs[k,1]).lower()

                            #Write to file:check both directions

                            if((fInts[n,0].lower()==ic1 and fInts[n,1].lower()==ic2) or (fInts[n,0].lower()==ic2 and fInts[n,1].lower()==ic1)):

                                for m in range(IC.shape[1]):

                                    outfile.write(str(IC[k,m]))
                                    outfile.write("\t")

                                outfile.write("\n")
=======

                fInts = fUniq

                rc = fInts.shape[0]
                rc2 = IC.shape[0]

                with open(outp, 'w+', encoding="utf-8") as outfile:

                    for n in range(rc2): #go through all original ints and find evidence

                        found = False
                        ind = -1

                        for k in range(rc): 

                            ic1 = str(IC[n,3])
                            ic2 = str(IC[n,7])

                            #Write to file:check both directions

                            if((fInts[k,0]==ic1 and fInts[k,1]==ic2) or (fInts[k,0]==ic2 and fInts[k,1]==ic1)):

                                found = True
                                ind=k

                        if(found==False):

                            for m in range(IC.shape[1]):

                                outfile.write(str(IC[n,m]))
                                outfile.write("\t")

                            outfile.write("\n")

                        else:


                            for m in range(IC.shape[1]):

                                outfile.write(str(IC[n,m]))
                                outfile.write("\t")

                            outfile.write(fInts[ind,2])
                            outfile.write("\t")
                            outfile.write(str(fInts[ind,3])) 
                            outfile.write("\t")
                            outfile.write(str(fInts[ind,4]))

                            outfile.write("\n") 

>>>>>>> bbf80e6015219c595960550fd1f025492cf265a3


                outfile.close()
                end = time.time() - start
                print("File filtered: " + str(f_in) + " Time: " + str(end) + " seconds")

if __name__ == '__main__':
    main()
