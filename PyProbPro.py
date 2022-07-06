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
Saves receipts of your times and questions asked. Displays your top slowest
problems and gives options to randomly or purposefully choose them.

To load your offline .csv:
Download your Problems as .csv (only downloading selected collumns and rows)
And name the document 'Problems.csv' and place in the same folder

See the example .csv file (Problems.csv) attached in this repository

> To Start: Use start() to pick randomly from all,
> hard() to randomly choose from problems that are above median time
> Or use problem(x) where x is the problem you want
> Use done() when done or show() to show the problem again
> Look at saved .txt receipts for a seperate record 

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
        file1.write(result_string +'\n')
        file1.write(str(end_time) +'\n')


def provide_problem(df, x, hard=False):
    '''
    displays the problem information
    '''
    global prob_choice
    global startT
    prob_choice = rnd.randint(0,len(df)-1)
    
    the_mean = df['Time'].mean()
    speed_desc = ''
    if hard == True:
        while int(df.loc[prob_choice]['Time']) < the_mean:
            prob_choice = rnd.randint(0,len(df)-1)

    # if using problem(x) set problem manually
    if x -1 >= 0 and x -1 <= len(df) -1:
        prob_choice = x - 1
        
    try:
        
        print('\nProblem', prob_choice+1)
        print('\n- - - - - - - - - - - - - - - - - -\n')
        print(df.loc[prob_choice]['Problem Description'])
        print('\n',df.loc[prob_choice]['Test Cases'])
        speed_desc = '\nBest time for this problem: ' + str(df.loc[prob_choice]['Time']) + ' min\n\nAverage best time for all problems: ' + str(the_mean) +' min\n'
        print(speed_desc)
        print("Run done() when finished to compare times, Show() to show problem again")
        print('\nDate stamp', datetime.now())
        print('\n- - - - - - - - - - - - - - - - - -\n')
    except:
        print('Problem reading problem data')
        return 'none'
        
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
        writefile.write(speed_desc)
        writefile.write(str(df.loc[prob_choice]['Time']) + '\n')

    return prob_choice
    
    
def import_data_table(file_name, read_rows, col_names):
    '''
    Import timeline from .csv file

    '''
    try:
        print('* * * * * * * * * * Python Problem Provider * * * * * * *\n')
        df = pd.read_csv(file_name,nrows=read_rows, on_bad_lines='skip')
        df.dropna()
       
        df2 = df.sort_values(by=['Time', 'Problem Description'], ascending = False)
        df2 = df2.loc[df2['Time'] > 0, ['Problem Description', 'Time']]
        print(df2.head())
        print('\nloaded table data from local .csv')
    except:
        print('error loading data from local .csv')

    return df


def set_up():
    col_names = ['Problem Description', 'Test Cases', 'Time']
    df = import_data_table('Problems.csv', 1000, col_names)
    return df

def hard():
    start(True)

def start(hard= False):
    '''
    Use this function in console to start problem solving
    '''
    global startT
    global prob_choice
    global loaded
    global df
    if type(df) == pd.DataFrame:
        startT = time.time()
        prob_choice = provide_problem(df, -1, hard)


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

def show():
    list_of_files = glob.glob('*.txt')
    latest_file = max(list_of_files, key=os.path.getctime)
    
    with open(latest_file, "r") as file1:
        fileList = file1.readlines()
        for i in range(len(fileList)):
            print(fileList[i])
            

startT = 0
prob_choice = -1
df = set_up()
if type(df) == pd.DataFrame:
    print('PyProbPro successfully loaded - Use start(), hard(), or problem(x) for a new problem')
else:
    print('error loading problems')
    



