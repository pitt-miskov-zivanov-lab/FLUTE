#  -*- coding: utf-8 -*-
#
#  This file is a part of FLUTE tool, developed by MeLoDy Lab at Univ of Pitt.
#  Compares list of interactions against local copy of FLUTE database
#
#  __author__ = "Emilee Holtzapple"
#  __reviewer__ = "Gaoxiang Zhou"
#  __time__ = "March 2021"

import argparse
import re
import time

import mysql.connector
import numpy as np
import pandas as pd


def filter_protein_ints(all_ints_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function returns interactions that involves protein either in regulator or regulated element

    Parameters
    ----------
    all_ints_df: pd.DataFrame
        All interactions from the input file, in DataFrame format, has to include the following columns:
        'Regulated Name', 'Regulated ID', 'Regulated Type', 'Regulator Name', 'Regulator ID', 'Regulator Type'

    Returns
    -------
    pt_only_ints: pd.DataFrame
        Interactions that involves protein either in regulator or regulated element. Formatted with only
        name (lowercase) and ID columns.
    """

    rel_ints = []

    for i, row in all_ints_df.iterrows():
        nm1 = row['Regulated Name']
        nm2 = row['Regulator Name']
        type1 = row['Regulated Type'].lower()
        type2 = row['Regulator Type'].lower()
        up_id1 = str(row['Regulated ID'])
        up_id2 = str(row['Regulator ID'])

        if type1 == 'protein' or type2 == 'protein':
            rel_ints.append([nm1.lower(), up_id1, nm2.lower(), up_id2])

    pt_only_ints = pd.DataFrame(rel_ints, columns=['Regulated Name', 'Regulated ID', 'Regulator Name', 'Regulator ID'])
    return pt_only_ints


def get_chem_id(pt_only_ints: pd.DataFrame) -> pd.DataFrame:
    """
    This function adds CIDm information to protein-chemical interactions

    Parameters
    ----------
    pt_only_ints: pd.DataFrame
        Interaction dataframe to be populated with CIDm information

    Returns
    -------
    pt_only_ints: pd.DataFrame
        Interaction dataframe with CIDm information filled out
    """
    for z in range(pt_only_ints.shape[0]):
        id1 = pt_only_ints.at[z, 'Regulated ID']
        id2 = pt_only_ints.at[z, 'Regulator ID']

        if id1.isdigit():
            pt_only_ints.at[z, 'Regulated CIDm'] = "CIDm" + '0' * (8 - len(id1)) + id1
        if id2.isdigit():
            pt_only_ints.at[z, 'Regulator CIDm'] = "CIDm" + '0' * (8 - len(id2)) + id2

    return pt_only_ints


def get_go_id(pt_only_ints: pd.DataFrame) -> pd.DataFrame:
    """
    This function adds go information to protein-biological process interactions

    Parameters
    ----------
    pt_only_ints: pd.DataFrame
        Interaction dataframe to be populated with GO information

    Returns
    -------
    pt_only_ints: pd.DataFrame
        Interaction dataframe with GO information filled out
    """

    mask1 = pt_only_ints["Regulated ID"].str.upper().str.contains("GO:", na=False)
    pt_only_ints.loc[mask1, "Regulated GoID"] = pt_only_ints.loc[mask1, "Regulated ID"].str.upper()

    mask2 = pt_only_ints["Regulator ID"].str.upper().str.contains("GO:", na=False)
    pt_only_ints.loc[mask2, "Regulator GoID"] = pt_only_ints.loc[mask2, "Regulator ID"].str.upper()

    return pt_only_ints


def get_string_id(pt_only_ints: pd.DataFrame, id_stringid_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function adds string_id information to regulated element and regulator in interactions

    Parameters
    ----------
    pt_only_ints: pd.DataFrame
        Interaction dataframe to be populated with string_id information
    id_stringid_df: pd.DataFrame
        Species dataframe that links id and string_id information

    Returns
    -------
    pt_only_ints: pd.DataFrame
        Interaction dataframe with string_id information filled out
    """

    id_stringid_dict = dict(zip(id_stringid_df['ID'], id_stringid_df['stringID']))

    pt_only_ints['Regulated stringID'] = pt_only_ints['Regulated ID'].apply(lambda x: id_stringid_dict[x[0:50]])
    pt_only_ints['Regulator stringID'] = pt_only_ints['Regulator ID'].apply(lambda x: id_stringid_dict[x[0:50]])

    return pt_only_ints


def get_uid(pt_only_ints: pd.DataFrame) -> pd.DataFrame:
    """
    This function adds uid information to regulated element and regulator in interactions:
    it is the same as ID if its corresponding stringID exists

    Parameters
    ----------
    pt_only_ints: pd.DataFrame
        Interaction dataframe to be populated with uid information

    Returns
    -------
    pt_only_ints: pd.DataFrame
        Interaction dataframe with uid information filled out
    """

    pt_only_ints['Regulated UID'] = \
        pt_only_ints[pt_only_ints['Regulated stringID'] == pt_only_ints['Regulated stringID']]['Regulated ID']
    pt_only_ints['Regulator UID'] = \
        pt_only_ints[pt_only_ints['Regulator stringID'] == pt_only_ints['Regulator stringID']]['Regulator ID']

    return pt_only_ints


def extract_year(input_path):
    """
    Load the input OA_file into a pd.DataFrame with Year, PMC, PMID columns

    Parameters
    ----------
    input_path: str
        Path to input OA_file

    Return
    ------
    year_df: pd.DataFrame
        A dataframe with Year, PMCID, PMID columns
    """

    year_df = pd.read_csv(input_path, sep='\t')
    year_df['Year'] = year_df['Publ'].apply(
        lambda x: re.search(r'\b(18|19|20)\d{2}\b', x)[0]
        if re.search(r'\b(18|19|20)\d{2}\b', x) else np.nan)
    year_df = year_df[['Year', 'PMCID', 'PMID']].dropna()

    return year_df


def filter_recent_ints(f_in, year_df, x=5):
    """
    This function should search input interaction file and find all interactions occurring in
    papers less than X years old

    Parameters
    ----------
    f_in: str
        Input filename that contains list of interactions, it shall include a column "Paper IDs"
    year_df: pd.DataFrame
        A dataframe with Year, PMCID, PMID columns
    x : int
        Integer specifying # of years, default is 5

    Return
    ------
    df: pd.DataFrame
        A dataframe containing all filtered interactions occurring in papers less than X years old
    """

    df = pd.read_excel(f_in)
    df = df.merge(year_df, left_on='Paper IDs', right_on='PMCID')

    df['Year'] = df['Year'].astype('int64')
    df = df[df['Year'] >= time.localtime().tm_year - x].drop(columns=year_df.columns)
    return df


def get_duplicates_ints(f_in):
    """
    This function calculates the number of duplicated occurrences of an interaction in a reading set.
    Interactions with same regulated ID, Regulator ID, and Paper ID are considered as duplicates.

    Parameters
    ----------
    f_in: str
        Input filename that contains list of interactions, it shall include columns 'Regulated ID',
        'Regulator ID', 'Paper IDs'

    Return
    ------
    duplicate_counts: pd.DataFrame
        a dataframe to indicate the number of occurrences of duplicated interaction in a reading set

    """

    df = pd.read_excel(f_in)

    columns_to_check = ['Regulated ID', 'Regulator ID', 'Paper IDs']
    duplicates = df[df.duplicated(subset=columns_to_check, keep=False)]
    duplicate_counts = duplicates.groupby(columns_to_check).size().reset_index(name='Occurrence')

    return duplicate_counts.sort_values(by='Occurrence', ascending=False)


class Query(object):

    def __init__(self, user, password, host, database):

        """
        Initialize query with credentials and configuration settings.

        Parameters
        ----------
        user : str
            Name of the MySQL user where the FLUTE DB is stored, usually 'root'
        password : str
            Password for the MySQL user where the FLUTE DB is stored.
        host : str
            Host name for the local machine where the coopy of the FLUTE DB is stored, usually 'localhost'
        database : str
            Name of the local copy of the FLUTE DB, usually 'flute'
        """

        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.db_cnx = mysql.connector.connect(user=self.user,
                                              password=self.password,
                                              host=self.host,
                                              database=self.database,
                                              charset='utf8')

    def ground_string_id(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        This function uses the flute database to ground species name and ID to identify stringID.

        Parameters
        ----------
        df: pd.DataFrame
            containing the columns of 'Name' and 'ID' of all studied species

        Returns
        -------
        df: pd.DataFrame
            New column 'stringID' added for all studied species
        """

        cursor = self.db_cnx.cursor()

        for i, row in df.iterrows():
            common_name = str(row['Name'])
            common_id = str(row['ID']).strip("\n")

            if common_id:
                int_query = "SELECT stringID FROM unistringmapping WHERE uniID = %s OR uniID= %s OR ogs= %s"
                cursor.execute(int_query, (common_id.upper(), common_name.upper(), common_name.upper()))
                for s in cursor.fetchall():
                    df.at[i, 'stringID'] = s[0]
        cursor.close()

        return df

    def get_related_papers(self, year_df, prot=None):
        """
        This function retrieves related papers based on a protein ID and saves a file of related paper IDs.

        Parameters
        ----------
        year_df : pd.DataFrame
            A DataFrame with Year, PMCID, PMID information
        prot : str
            Input protein ID to retrieve related papers. ',' can be used to split multiple IDs

        Return
        ------
        fp_list : list
            the list of paper PMCIDs that are related to inquired protein IDs
        """

        if prot is None:
            fp_list = []
            return fp_list

        all_prot = [p.strip() for p in prot.split(",")] if "," in prot else [prot.strip()]

        ref_logs = []
        cursor = self.db_cnx.cursor()
        for id in all_prot:
            # Query for ogs values
            ogs_query = "SELECT ogs FROM unistringmapping WHERE uniID = %s OR uniID = %s"
            cursor.execute(ogs_query, (id, "uniprotkb:" + id))
            id_ogs = [result[0] for result in cursor.fetchall()]

            # Query for PubID values
            pub_query = "SELECT PubID FROM biogrid WHERE ogsA = %s OR ogsB = %s"
            for og_id in id_ogs:
                cursor.execute(pub_query, (og_id, og_id))
                ref_logs.extend(str(result[0]) for result in cursor.fetchall())

            # Query inside Reactome
            react_query = "SELECT ref FROM reactome WHERE upID1 = %s OR upID2 = %s"
            cursor.execute(react_query, ("uniprotkb:" + id, "uniprotkb:" + id))
            ref_logs.extend([ind_ref for r in cursor.fetchall() for ind_ref in r[0].split("|")])
        cursor.close()

        fp_list = year_df[year_df['PMID'].isin(["PMID:" + i for i in set(ref_logs)])]['PMCID'].tolist()
        return fp_list

    def get_same_papers_ints(self, file_in, year_df):
        """
        This function retrieves interactions from the same papers as input spreadsheet

        Parameters
        ----------
        file_in: str
            File name of a spreadsheet (.xlsx) containing a column name "Paper IDs"
        year_df: pd.DataFrame
            A DataFrame with Year, PMCID, PMID information

        Return
        ------
        ints_same_pp: np.array
            Array of interactions that are occurred in the same papers as input file, each interaction is in the
            format of (protein1's external ID, protein2's external ID, mode, source in PMID)
        """

        df = pd.read_excel(file_in)
        pmid_list = list(set(
            year_df[year_df['PMCID'].isin(df['Paper IDs'].tolist())]['PMID'].str.replace('PMID:', 'PMID0').tolist()))

        cursor = self.db_cnx.cursor()

        placeholders = ', '.join(['%s'] * len(pmid_list))
        paper_query = f"SELECT protein1, protein2, mode, sources FROM actions_source WHERE sources IN ({placeholders})"
        cursor.execute(paper_query, pmid_list)
        ints_same_pp = np.array(cursor.fetchall(), dtype="U50")

        if len(ints_same_pp) == 0:
            return ints_same_pp

        info_query = "SELECT external_id FROM protein_info WHERE internal_id=%(internal_id)s"
        external_ids = [cursor.execute(info_query, {'internal_id': ele}) or cursor.fetchone()[0] for ele in
                        ints_same_pp[:, [0, 1]].ravel()]
        cursor.close()

        ints_same_pp[:, [0, 1]] = np.array(external_ids).reshape(ints_same_pp[:, [0, 1]].shape)
        return ints_same_pp

    def filter_pt_ints_by_scoring(self, pt_only_ints: pd.DataFrame, score_tuple: tuple) -> pd.DataFrame:
        """
        This function further filters protein-only interactions via multiple tables in database, subject to score tuple.
        It would return a DataFrame with scored protein-only interactions

        Parameters
        ----------
        pt_only_ints: pd.DataFrame
            protein-only interactions with name/id/uid/stringID/GoID/CIDm etc. information filled out
        score_tuple: tuple
            a tuple of three numbers, denoting thresholds of escore, tscore, dscore

        Return
        ------
        pt_scored_ints: pd.DataFrame
            interactions further filtered by database entries and score thresholds
        """

        cursor = self.db_cnx.cursor(buffered=True)

        df_qry1 = \
            pt_only_ints[(pt_only_ints['Regulated stringID'].notna()) & (pt_only_ints['Regulator stringID'].notna())][
                ['Regulated stringID', 'Regulator stringID']]
        df_qry1['copy_r_str'] = df_qry1['Regulator stringID']
        df_qry1['copy_d_str'] = df_qry1['Regulated stringID']
        df_qry1['es'] = score_tuple[0]
        df_qry1['ts'] = score_tuple[1]
        df_qry1['ds'] = score_tuple[2]

        query1 = "SELECT protein1,protein2,escore,tscore,dscore FROM ppi_detail_v11 WHERE " + " OR ".join([
               "(((protein1 = %s AND protein2 = %s) OR (protein1 = %s AND protein2 = %s)) AND "
               "(escore>=%s AND tscore>=%s AND dscore>=%s))"] * len(df_qry1))
        params1 = df_qry1.to_numpy().flatten().tolist()

        cursor.execute(query1, params1)
        obtained_rows1 = cursor.fetchall()

        qry_result1a = pd.DataFrame(obtained_rows1,
                                    columns=['Regulated stringID', 'Regulator stringID', 'escore', 'tscore', 'dscore'])
        qry_merged1a = \
            pd.merge(qry_result1a, pt_only_ints, on=['Regulated stringID', 'Regulator stringID'], how='left')[
                ['Regulated ID', 'Regulator ID', 'escore', 'tscore', 'dscore']]
        qry_merged1a = qry_merged1a[(qry_merged1a['Regulated ID'].notna()) & (qry_merged1a['Regulator ID'].notna())]

        qry_result1b = pd.DataFrame(obtained_rows1,
                                    columns=['Regulator stringID', 'Regulated stringID', 'escore', 'tscore', 'dscore'])
        qry_merged1b = \
            pd.merge(qry_result1b, pt_only_ints, on=['Regulator stringID', 'Regulated stringID'], how='left')[
                ['Regulated ID', 'Regulator ID', 'escore', 'tscore', 'dscore']]
        qry_merged1b = qry_merged1b[(qry_merged1b['Regulated ID'].notna()) & (qry_merged1b['Regulator ID'].notna())]

        df_qry2 = pt_only_ints[(pt_only_ints['Regulated UID'].notna()) & (pt_only_ints['Regulator UID'].notna()) & (
                pt_only_ints['Regulated UID'] != pt_only_ints['Regulator UID'])][['Regulated UID', 'Regulator UID']]
        df_qry2['Regulated UID'] = 'uniprotkb:' + df_qry2['Regulated UID'].astype(str).str.upper()
        df_qry2['Regulator UID'] = 'uniprotkb:' + df_qry2['Regulator UID'].astype(str).str.upper()
        df_qry2['copy_r_uid'] = df_qry2['Regulator UID']
        df_qry2['copy_d_uid'] = df_qry2['Regulated UID']

        query2 = "SELECT upid1,upid2 FROM reactome WHERE " + " OR ".join(
            ["((upid1=%s AND upid2=%s) OR (upid1=%s AND upid2=%s))"] * len(df_qry2))
        params2 = df_qry2.to_numpy().flatten().tolist()

        cursor.execute(query2, params2)
        obtained_rows2 = cursor.fetchall()

        qry_result2a = pd.DataFrame(obtained_rows2, columns=['Regulated UID', 'Regulator UID'])
        qry_result2a['Regulated UID'] = qry_result2a['Regulated UID'].astype(str).str.replace('uniprotkb:', '')
        qry_result2a['Regulator UID'] = qry_result2a['Regulator UID'].astype(str).str.replace('uniprotkb:', '')
        qry_result2a['escore'] = np.nan
        qry_result2a['tscore'] = np.nan
        qry_result2a['dscore'] = np.nan
        qry_merged2a = pd.merge(qry_result2a, pt_only_ints, on=['Regulated UID', 'Regulator UID'], how='left')[
            ['Regulated UID', 'Regulator UID', 'escore', 'tscore', 'dscore']]
        qry_merged2a = qry_merged2a[(qry_merged2a['Regulated UID'].notna()) & (qry_merged2a['Regulator UID'].notna())]

        qry_result2b = pd.DataFrame(obtained_rows2, columns=['Regulator UID', 'Regulated UID'])
        qry_result2b['Regulated UID'] = qry_result2b['Regulated UID'].astype(str).str.replace('uniprotkb:', '')
        qry_result2b['Regulator UID'] = qry_result2b['Regulator UID'].astype(str).str.replace('uniprotkb:', '')
        qry_result2b['escore'] = np.nan
        qry_result2b['tscore'] = np.nan
        qry_result2b['dscore'] = np.nan
        qry_merged2b = pd.merge(qry_result2b, pt_only_ints, on=['Regulated UID', 'Regulator UID'], how='left')[
            ['Regulated UID', 'Regulator UID', 'escore', 'tscore', 'dscore']]
        qry_merged2b = qry_merged2b[(qry_merged2b['Regulated UID'].notna()) & (qry_merged2b['Regulator UID'].notna())]

        # FIXME: qry3 seems to be extra or in wrong format
        # df_qry3 = pt_only_ints[['Regulated ID', 'Regulator ID']]
        # df_qry3['copy_d_id'] = df_qry3['Regulated ID']
        # df_qry3['copy_r_id'] = df_qry3['Regulator ID']

        # query3 = "SELECT ogsA,ogsB FROM biogrid WHERE " + " OR ".join(
        #     ["( (ogsA = %s AND ogsB = %s) OR (ogsB = %s AND ogsA = %s) )"] * len(df_qry3))
        # params3 = df_qry3.to_numpy().flatten().tolist()

        # cursor.execute(query3, params3)
        # obtained_rows3 = cursor.fetchall()
        # qry_result3 = pd.DataFrame(obtained_rows3, columns=['ogsA', 'ogsB'])

        df_qry4 = pt_only_ints[(pt_only_ints["Regulated GoID"].notna()) & (pt_only_ints["Regulator UID"].notna()) | (
            pt_only_ints["Regulator GoID"].notna()) & (pt_only_ints["Regulated UID"].notna())][
            ["Regulated GoID", "Regulator UID", "Regulator GoID", "Regulated UID"]].astype(str)

        query4 = "SELECT goterm,id1,evidence FROM goterms WHERE " + " OR ".join(
            ["( (goterm = %s AND id1 = %s) OR (goterm = %s AND id1 = %s) )"] * len(df_qry4))
        params4 = df_qry4.to_numpy().flatten().tolist()

        cursor.execute(query4, params4)
        obtained_rows4 = cursor.fetchall()

        qry_result4a = pd.DataFrame(obtained_rows4, columns=['Regulated GoID', 'Regulator UID', 'evidence'])
        qry_result4a['ts'] = np.nan
        qry_result4a['ds'] = np.nan
        qry_merged4a = pd.merge(qry_result4a, pt_only_ints, on=['Regulated GoID', 'Regulator UID'], how='left')[
            ['Regulated ID', 'Regulator ID', 'evidence', 'ts', 'ds']]
        qry_merged4a = qry_merged4a[(qry_merged4a['Regulated ID'].notna()) & (qry_merged4a['Regulator ID'].notna())]

        qry_result4b = pd.DataFrame(obtained_rows4, columns=['Regulator GoID', 'Regulated UID', 'evidence'])
        qry_result4b['ts'] = np.nan
        qry_result4b['ds'] = np.nan
        qry_merged4b = pd.merge(qry_result4b, pt_only_ints, on=['Regulator GoID', 'Regulated UID'], how='left')[
            ['Regulated ID', 'Regulator ID', 'evidence', 'ts', 'ds']]
        qry_merged4b = qry_merged4b[(qry_merged4b['Regulated ID'].notna()) & (qry_merged4b['Regulator ID'].notna())]

        df_qry5 = \
            pt_only_ints[(pt_only_ints["Regulated CIDm"].notna()) & (pt_only_ints["Regulator stringID"].notna()) | (
                pt_only_ints["Regulator CIDm"].notna()) & (pt_only_ints["Regulated stringID"].notna())][
                ["Regulated CIDm", "Regulator stringID", "Regulator CIDm", "Regulated stringID"]].astype(str)

        # FIXME: if chem: logs.append([name1, name2, exp, pred, data]) else: ??
        query5 = "SELECT chem,prot,exp,text,data FROM pci_detail WHERE " + " OR ".join(
            ["( (chem= %s AND prot = %s) OR (chem= %s AND prot = %s) )"] * len(df_qry5))
        params5 = df_qry5.to_numpy().flatten().tolist()

        cursor.execute(query5, params5)
        obtained_rows5 = cursor.fetchall()
        cursor.close()

        qry_result5a = pd.DataFrame(obtained_rows5,
                                    columns=['Regulated CIDm', 'Regulator stringID', 'exp', 'text', 'data'])
        qry_merged5a = pd.merge(qry_result5a, pt_only_ints, on=['Regulated CIDm', 'Regulator stringID'], how='left')[
            ['Regulated ID', 'Regulator ID', 'exp', 'text', 'data']]
        qry_merged5a = qry_merged5a[(qry_merged5a['Regulated ID'].notna()) & (qry_merged5a['Regulator ID'].notna())]

        qry_result5b = pd.DataFrame(obtained_rows5,
                                    columns=['Regulator CIDm', 'Regulated stringID', 'exp', 'text', 'data'])
        qry_merged5b = pd.merge(qry_result5b, pt_only_ints, on=['Regulator CIDm', 'Regulated stringID'], how='left')[
            ['Regulated ID', 'Regulator ID', 'exp', 'text', 'data']]
        qry_merged5b = qry_merged5b[(qry_merged5b['Regulated ID'].notna()) & (qry_merged5b['Regulator ID'].notna())]

        # Concatenate arrays
        concatenated_array = np.vstack((qry_merged1a.fillna('').to_numpy(dtype='U50'),
                                        qry_merged1b.fillna('').to_numpy(dtype='U50'),
                                        qry_merged2a.fillna('').to_numpy(dtype='U50'),
                                        qry_merged2b.fillna('').to_numpy(dtype='U50'),
                                        qry_merged4a.fillna('').to_numpy(dtype='U50'),
                                        qry_merged4b.fillna('').to_numpy(dtype='U50'),
                                        qry_merged5a.fillna('').to_numpy(dtype='U50'),
                                        qry_merged5b.fillna('').to_numpy(dtype='U50')))

        pt_scored_ints = pd.DataFrame(np.unique(concatenated_array, axis=0),
                                      columns=["Element 1 ID", "Element 2 ID", "STRING escore", "STRING tscore",
                                               "STRING dscore"])

        return pt_scored_ints

    def filtered_input_ints(self, f_in, score_tuple, output_path):
        """
        This function uses the input interaction file and tuple of score threshold to generate all scored
        protein-related interactions and filtered scored interactions from the input file

        Parameters
        ----------
        f_in: str
            The path of input interaction file (.xlsx), best in BioRECIPE format. Minimum required column names include
            ['Regulated Name', 'Regulated ID', 'Regulated Type',
            'Regulator Name', 'Regulator ID', 'Regulator Type', 'Paper IDs']
        score_tuple: tuple
            a tuple of three numbers, denoting thresholds of escore, tscore, dscore
        output_path: str
            specify output path to store the final output:
            1) <output_path>_grd_ints_scores.xlsx : contains all scored protein-related interactions
            2) <output_path>_filtered.xlsx : contains filtered interactions from the input file

        Returns
        -------
        """

        start = time.time()

        df = pd.read_excel(f_in)
        df = df.fillna('').astype(str)

        # please make sure input file at least has the following headers
        interaction_df = df[['Regulated Name', 'Regulated ID', 'Regulated Type',
                             'Regulator Name', 'Regulator ID', 'Regulator Type', 'Paper IDs']]

        # Make a dataframe with id-name of all species
        id_name1 = df[['Regulated ID', 'Regulated Name']].rename(
            columns={'Regulated ID': 'ID', 'Regulated Name': 'Name'})
        id_name2 = df[['Regulator ID', 'Regulator Name']].rename(
            columns={'Regulator ID': 'ID', 'Regulator Name': 'Name'})
        id_name_df = pd.concat([id_name1, id_name2], ignore_index=True)
        id_name_df['ID'] = id_name_df['ID'].astype(str).str.slice(0, 50)
        id_name_df['Name'] = id_name_df['Name'].astype(str).str.slice(0, 50)
        id_name_df = id_name_df.drop_duplicates(subset='ID')

        # Ground the dataframe to fill out stringID information
        id_name_df = self.ground_string_id(id_name_df)

        pt_only_ints = filter_protein_ints(interaction_df)  # returns lower-case interactions:ppis/pcis/pbpis
        pt_only_ints = get_chem_id(pt_only_ints)
        pt_only_ints = get_go_id(pt_only_ints)
        pt_only_ints = get_string_id(pt_only_ints, id_name_df)
        pt_only_ints = get_uid(pt_only_ints)

        pt_scored_ints = self.filter_pt_ints_by_scoring(pt_only_ints, score_tuple)
        pt_scored_ints.to_excel(output_path + "_grd_ints_scores.xlsx", index=False)

        pt_scored_ints['set_12'] = pt_scored_ints.apply(
            lambda row: frozenset([row['Element 1 ID'].lower(), row['Element 2 ID'].lower()]),
            axis=1)
        df['set_dr'] = df.apply(lambda row: frozenset([row['Regulated ID'].lower(), row['Regulator ID'].lower()]),
                                axis=1)

        # Merge the DataFrames based on the sets and drop the helper columns
        output_df = df.merge(pt_scored_ints, left_on='set_dr', right_on='set_12')
        output_df = output_df.drop(columns=pt_scored_ints.columns.tolist() + ['set_dr', ])
        output_df = output_df.drop_duplicates()
        output_df.to_excel(output_path + "_filtered.xlsx", index=False)

        end = time.time() - start
        print("File filtered: " + str(f_in) + " Time: " + str(end) + " seconds")


def get_args():
    parser = argparse.ArgumentParser(description="Identify high-confidence interactions in machine reading output.")

    parser.add_argument('username', type=str, help="MySQL username")
    parser.add_argument('password', type=str, help="MySQL password")
    parser.add_argument('host', type=str, help="MySQL host")
    parser.add_argument('db_name', type=str, help="MySQL database name")

    parser.add_argument('input_file', type=str, help="Input file")
    parser.add_argument('output_path', type=str, help="Filtered reading output path")

    parser.add_argument('-g', '--drop_duplicates', action="store_true", default=False,
                        help="Whether to output duplicate interactions")
    parser.add_argument('-p', '--keep_recent_pps', action="store_true", default=False,
                        help="If true, show interactions in recent papers")
    parser.add_argument('-q', '--prot_query', nargs='?', const=None, default=None,
                        help="If exists, finds interactions related to protein ID")
    parser.add_argument('-r', '--add_related_ints', action="store_true", default=False,
                        help="If true, finds additional interactions related to input that are in the same paper set")

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    user = args.username
    password = args.password
    name = args.db_name
    host = args.host

    f_in = args.input_file
    out_path = args.output_path

    # User need to unzip supplementary/oa_file_list.txt.zip and put it to input/
    # From src/ directory, you can:
    # unzip ../supplementary/oa_file_list.txt.zip -d "../examples/input/"
    year_df = extract_year("../examples/input/oa_file_list.txt")

    # If user wants to choose a different tuple of scores threshold from 0,0,0
    score_tuple = (0, 0, 0)
    # If user wants to choose a different number of years for "recent years", from x=5
    x = 5

    query = Query(user, password, host, name)
    if args.keep_recent_pps:
        optional_output = filter_recent_ints(f_in=f_in, year_df=year_df, x=x)
        optional_output.to_excel(args.output_path + '_optional_recent_ints.xlsx', index=False)

    if args.drop_duplicates:
        optional_output = get_duplicates_ints(f_in)
        optional_output.to_excel(args.output_path + '_optional_duplicated_ints.xlsx', index=False)

    if args.prot_query:
        fq_list = query.get_related_papers(year_df, args.prot_query)
        pd.DataFrame(fq_list, columns=['Paper IDs']).to_excel(args.output_path + '_query_' + args.prot_query + '.xlsx',
                                                              index=False)
        optional_output = query.get_same_papers_ints(args.output_path + '_query_' + args.prot_query + '.xlsx', year_df)
        pd.DataFrame(optional_output, columns=['Regulated ID', 'Regulator ID', 'Mechanism', 'Paper IDs']).to_excel(
            args.output_path + '_optional_ints_related_to_' + args.prot_query + '.xlsx', index=False)

    if args.add_related_ints:
        optional_output = query.get_same_papers_ints(f_in, year_df)
        pd.DataFrame(optional_output, columns=['Regulated ID', 'Regulator ID', 'Mechanism', 'Paper IDs']).to_excel(
            args.output_path + '_optional_ints_in_same_pps.xlsx', index=False)

    query.filtered_input_ints(f_in, score_tuple, out_path)


if __name__ == '__main__':
    main()
