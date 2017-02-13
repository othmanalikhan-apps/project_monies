Project Monies--Where Have You Gone?
------------------------------------

The aim of the project is to visualise expenditure to encourage better
management of money. The code parses bank statements supplied as text files
from Santander (international bank), and outputs some graphs (see below).


Prerequisites
-------------
- Python 3+ (see requirements.txt file)


How to Use
----------
1. Download or clone the repository
2. Edit the main method in project_monies > monies > monies > visualise.py to
 specify which keywords to search in the bank statement and hence plot.
3. Run 'visualise.py' using a python interpreter 


Key Features
------------
- Convert a Santander bank statement .txt files into .csv format
- Search the .txt files for transactions based on a keyword

- Create two types of visualisation:
    - Graph: Bar plot of the total expense per month for a category, for multiple categories.
    - Uses: Find the month with the cheapest food ordering scheme.
    ![alt text][logo]
    <br> <br><br>
    - Graph: Total expense vs time, for multiple categories.
    - Uses: Predict how many years needed to wait before buying some item, and highlight the category with the highest expense so savings can be considered.
    ![alt text][logo2]

[logo]: res/samples/bar_sample.gif
[logo2]: res/samples/line_sample.gif

Authors
-------
Othman Alikhan, oz.alikhan@gmail.com
