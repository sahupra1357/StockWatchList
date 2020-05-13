Python Project - Stock Watch List 

Setting up development environment, using

1. virtualenv
2. pip
3. git

Project Explanation:

Start the project (python stockwatchlist.py) , open the browser to open the Index page of local environment (http://localhost:5000/).

This page contains 2 input fields.

Stock Code -- Valid stock code
Buying Price -- Your stock buying price or expected price to buy or can be blank

One Button -- Add Stock

Click on "Add Stock" button below steps will execute,

1) Go to Yahoo Finance page for that Stock 
2) Scrap "Stock Name", "52 Week High", "52 Week Low", "Current Market Price".
3) Depending on the Buying Price, program will calculate the profit loss.
4) If there is no "Buying Price" provided then the "Buying Price" & "Profit/Loss" would be 0.
5) Store all these details in Sqlite database

Exception:	
    If Stock code is not correct then program will not add or update anything. 

There are 2 actions.
1) Update - Update the current market price of the Stock.
2) Delete - Delete the Stock from the list.
