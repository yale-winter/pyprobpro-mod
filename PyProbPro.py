# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 02:19:15 2022

@author: yale-winter
yalewinter.com

- - - - - - - - - - - - - - - - - - - - - - - - -

PyProbPro - Python Problem Provider

- - - - - - - - - - - - - - - - - - - - - - - - -

Create a google sheet online or use with .csv offline 
The document needs the following schema:

Collumns: (A)Problem Description  (B)Test Cases   (C)Time
Data:             Problem 1       x = [1,2,3]       20
Data:             Problem 2       x = "bob"         15
etc ...

Run the script to test your Problem Solving and try to get a better time,
Saves receipts of your times and questions asked.

To load your live google sheet online (set so anyone with the link can view):
Change import_online to True, and replace ___online_url___ with that part of your url

To load your offline .csv:
Download your Problems as .csv (only downloading selected collumns and rows)
And name the document 'Problems.csv' and place in the same folder

See the example .csv file (Problems.csv) attached in this repository

>>> Use function start() to start OR use problem(x) where x is the problem you want
>>> Use function done() when done

"""
import pandas as pd
import os
import random as rnd
import time
from datetime import datetime
import glob

def done():
    '''
    Use this function in console when done
    '''

    list_of_files = glob.glob('*.txt')
    latest_file = max(list_of_files, key=os.path.getctime)
    
    with open(latest_file, "r") as file1:
        fileList = file1.readlines()
        
    last_time = int(fileList[-1])
    end_time = int(((time.time() - float(fileList[1]))/60))
    print('minutes taken', end_time)
    
    result_string = ''
    if end_time < last_time:
        result_string = 'New fastest time: ' + str(end_time) + ' minutes. Congratulations, this was ' + str(last_time - end_time) + ' minutes faster'
    else: 
        result_string = 'New time: ' + str(end_time) + ' minutes. This was ' + str(end_time - last_time) + ' minutes slower than your best'
    print(result_string)
    with open(latest_file, "a") as file1:
        file1.write(str(end_time) +'\n')


def provide_problem(df, x):
    '''
    displays the problem information
    '''
    global prob_choice
    global startT
    prob_choice = rnd.randint(0,len(df)-1)
    
    # if using problem(x) set problem manually
    if x -1 >= 0 and x -1 <= len(df) -1:
        prob_choice = x - 1
    
    try:
        print('Problem', prob_choice+1)
        print('\n- - - - - - - - - - - - - - - - - -\n')
        print(df.loc[prob_choice]['Problem Description'])
        print('\n')
        print(df.loc[prob_choice]['Test Cases'])
        print("\nRun done() when finished to compare times")
    except:
        print('problem reading problem data')
        
    print('date time', datetime.now())
    # Write line to file
    fName = str(datetime.now()) + '-Problem-' + str(prob_choice + 1) 
    fName = fName.replace('.', '_')
    fName = fName.replace(' ', '_')
    fName = fName.replace(':', '_')
    fName += '.txt'

    with open(fName, 'w') as writefile:
        writefile.write('Problem ' + str(prob_choice+1)+'\n')
        writefile.write(str(startT) + '\n')
        writefile.write(str(datetime.now()) + '\n')
        writefile.write(str(df.loc[prob_choice]['Problem Description']) + '\n')
        writefile.write(str(df.loc[prob_choice]['Test Cases']) + '\n')
        writefile.write(str(df.loc[prob_choice]['Time']) + '\n')

    return prob_choice
    
    
def import_data_table(file_name, online, gsheet_mid_link, read_rows, col_names):
    '''
    Import timeline from .csv file
    
    Parameters
    ----------
    file_name : string
        File name including file extension
    online : bool
        Read online or local
    read_rows : number
        number of rows to read
    col_names : array of strings
        names of columns

    Returns
    -------
    DataFrame of the content or error string

    '''
    df = 'error importing data'
    if online:
        try:
            df = pd.read_csv('https://docs.google.com/spreadsheets/d/' + 
            gsheet_mid_link +
            '/export?gid=0&format=csv',nrows=read_rows, on_bad_lines='skip')
            print('loaded table data from google sheet online')
        except:
            print('error loading table data from google sheet online')
            online = False
            
    if online == False:
        try:
            df = pd.read_csv(file_name,nrows=read_rows, on_bad_lines='skip')
            print('loaded table data from local .csv')
        except:
            print('error loading data from local .csv')
    
    # drop rows where at least 1 element is missing
    if type(df) == pd.DataFrame:
        df.dropna()

    return df


def set_up(import_online,gsheet_mid_link):
    col_names = ['Problem Description', 'Test Cases', 'Time']
    df = import_data_table('Problems.csv', import_online, gsheet_mid_link, 1000, col_names)
    return df


def start():
    '''
    Use this function in console to start problem solving
    '''
    global startT
    global prob_choice
    global loaded
    global df
    if type(df) == pd.DataFrame:
        startT = time.time()
        prob_choice = provide_problem(df, -1)


def problem(x):
    '''
    Use this function to answer a specific ID question
    '''
    global startT
    global prob_choice
    global loaded
    global df
    if type(df) == pd.DataFrame:
        startT = time.time()
        prob_choice = provide_problem(df, x)


import_online = False
gsheet_mid_link = 'your_url_here'
startT = 0
prob_choice = -1
df = set_up(import_online,gsheet_mid_link)
if type(df) == pd.DataFrame:
    print('PyProbPro successfully loaded - Use start() or problem(x) for a new problem')
else:
    print('Problem loading problems')



