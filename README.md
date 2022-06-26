# PyProbPro
PyProbPro - Python Problem Provider

![PyToDoT](https://user-images.githubusercontent.com/5803874/175763591-e8261c2d-d28c-4527-a3d6-aa3672ad4171.jpg)
- - - - - - - - - - - - - - - - - - - - - - - - -
**PyToDoT: Python To-Do Tracker**
- - - - - - - - - - - - - - - - - - - - - - - - -
Create a google sheet online or use with .csv offline with the following schema:

| Problem Description | Test Cases | Time | 
| --- | --- | --- |
| Problem 1 | Test case 1 | 20 |
| Problem 2 | Test case 2 | 15 | 


**To load your live google sheet online:**<br/>
Change import_online to True, and replace ___online_url___ with that part of your url<br/><br/>
**To load your offline .csv:**<br/>
Download your Problems as .csv (only downloading selected collumns and rows)<br/>
And name the document 'Problems.csv' and place in the same folder<br/><br/>
**How to Use:**
- Run in Jupyter Notebook etc parallel alongside another or an IDE used to solve the problem
- Use the command done() to see how your time compared to your best
- See the example .csv file (Problems.csv) attached in this repository
