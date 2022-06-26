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

To load your live google sheet online:
Change import_online to True, and replace ___online_url___ with that part of your url

To load your offline .csv:
Download your Problems as .csv (only downloading selected collumns and rows)
And name the document 'Problems.csv' and place in the same folder
Run the script to test your Problem Solving and try to get a better time

>> See the example .csv file (Problems.csv) attached in this repository

>> Run in Jupyter Notebook etc parallel alongside another or an IDE etc to solve the problem

Use the command done() to see how your time compared to your best

*** or enable read/write file to manually call problems ***

"""
import pandas as pd
import os
import random as rnd
import time

def done():
    last_time = df.loc[i]['Time']
    print(last_time)
    end = time.time()
    end_time = int((end - start)/60)
    print(end_time)
    if end_time < last_time:
        print('New fastest time:', end_time, 'minutes. Congratulations, this was', last_time - end_time, 'minutes faster')
    else: 
        print('New time:', end_time, 'minutes. This was', end_time - last_time, 'minutes slower than your best')

def provide_problem(df):
    i = rnd.randint(0,len(df)-1)
    try:
        print('Problem', i+1)
        print('\n- - - - - - - - - - - - - - - - - -\n')
        print(df.loc[i]['Problem Description'])
        print('\n')
        print(df.loc[i]['Test Cases'])
        print("\nRun done() when finished to compare times")
    except:
        print('problem reading problem data')
    return i
    
    
def import_problems(file_name, online, read_rows):
    '''
    Import to-dos from .csv file
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

def start():
    '''
    Start up
    '''
    import_online = True
    df, loaded = import_problems('Problems.csv', import_online, 1000)
    if loaded:
        start = time.time()
        i = provide_problem(df)
    return df, start, i

df, start, i = start()



