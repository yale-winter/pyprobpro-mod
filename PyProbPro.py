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

To load your live google sheet online:
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
        
    if len(fileList) == 6:
        
        last_time = int(fileList[5])
        end_time = int(((time.time() - float(fileList[1]))/60))
        print('minutes taken', end_time)
    
        result_string = ''
        if end_time < last_time:
            result_string = 'New fastest time: ' + str(end_time) + ' minutes. Congratulations, this was ' + str(last_time - end_time) + ' minutes faster'
        else: 
            result_string = 'New time: ' + str(end_time) + ' minutes. This was ' + str(end_time - last_time) + ' minutes slower than your best'
        print(result_string)
        with open(latest_file, "a") as file1:
            file1.write(result_string +'\n')
    else:
        print('most recent problem already marked complete')


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
    
    
def import_problems(file_name, online, read_rows):
    '''
    Import problem solving questions from .csv file
    '''
    loaded = False
    try:
        if online:
            df = pd.read_csv('https://docs.google.com/spreadsheets/d/' + 
                               '___online_url___' +
                               '/export?gid=0&format=csv',
                              )
        else:
            # file path (same directory as this file)
            __location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))
            sheet_url = os.path.join(__location__, file_name)
            df = pd.read_csv(sheet_url, nrows=read_rows, on_bad_lines='skip')
            df.dropna(how='all')
        df = pd.DataFrame(df, columns=['Problem Description', 'Test Cases', 'Time'])
    except:
        print('initial problem reading data')
    finally:
        loaded = True
    return df, loaded


def set_up(import_online):
    
    df, loaded = import_problems('Problems.csv', import_online, 1000)
    return df, loaded


def start():
    '''
    Use this function in console to start problem solving
    '''
    global startT
    global prob_choice
    global loaded
    global df
    if loaded:
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
    if loaded:
        startT = time.time()
        prob_choice = provide_problem(df, x)


import_online = False
startT = 0
prob_choice = -1
df, loaded = set_up(import_online)
if loaded:
    print('PyProbPro successfully loaded - Use start() or problem(x) for a new problem')
else:
    print('Problem loading problems')



