### the purpose of this script is to pull data from reddit/wallstreetbets and visualize the most commonly posted stock tickers
### at any given time, using pushshift API

##### I AM NOT A FINANCIAL ADVISOR AND THIS SCRIPT AND ITS CONTENT AND/OR OUTPUTS ARE NOT FINANCIAL OR INVESTMENT ADVICE #####


# if you don't have psaw library installed, type pip install psaw into your terminal line first before running the rest of this code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
import psaw
import datetime as dt
from psaw import PushshiftAPI

api = PushshiftAPI()

#importing in csv file of all stock tickers from nasdaq website directory, then converting the symbols into a list

nasdaq_df = pd.read_csv('/Users/mason/Desktop/Python_Practice/nasdaq_tickers.csv')
symbols_list = nasdaq_df['Symbol'].to_list()


#creating time stamp with which to check WSB

start_time = int(dt.datetime(2021, 3, 12).timestamp())


#getting submissions onto WSB and adding it into a list as type string so we can split it up into an array

submissions = str(list(
    api.search_submissions(after=start_time, subreddit='wallstreetbets', filter=['url', 'author', 'title', 'subreddit'], limit=100)
    ))

#splitting submission entries up into an array

word_list = submissions.split()
print(word_list)

#searching word list for entries that start with $ or are in all caps (looking for stock tickers)

ticker_list = []
for entry in word_list:
    
    if entry.startswith('$'):
        ticker_list.append(entry)
    if entry.isupper():
        ticker_list.append(entry)
print(ticker_list)

#filtering out irrelevant entries from ticker list

for ticker in ticker_list:
    ticker.replace("'", "")
    ticker.replace('.', "")
    ticker.replace('"', "")
    ticker.replace('*', "")
    ticker.replace("'", "")
    ticker.replace('!', "")
    ticker.replace('$', "")
    ticker.replace('?', "")
    if ticker.startswith(" "):
        ticker.replace(" ", "")
    if ticker.startswith('$'):
        ticker.replace('$', "")
    if ticker.endswith(','):
        ticker_list.remove(ticker)
    if ticker.startswith("'"):
        ticker.replace("'", "")
    if ticker.startswith('"'):
        ticker.replace('"', "")
    if ticker.endswith('?'):
        ticker_list.remove(ticker)

#creating a final list and using our symbol list with all the stock tickers to determine which WSB entries are actually stock references

WSB_list = []
for ticker in ticker_list:
    if ticker in symbols_list:
        WSB_list.append(ticker)
        
print(WSB_list)

#creating a new dataframe of 1 column named Symbol for all the stock ticker symbols found in the WSB list

WSB_df = pd.DataFrame(WSB_list, columns=['Symbol'])
display(WSB_df.head())

#creating variable X to represent the value counts for each stock ticker

X = WSB_df['Symbol'].value_counts()

#creating bar graph for top 30 stock tickers by value count

plt.figure(figsize=(10, 7))
(X[0:30]).plot(kind='bar', color='r')
plt.title('WSB Stock Ticker Frequency Plot')
plt.xlabel('Stock Ticker')
plt.ylabel('Number of Mentions')  
plt.show()
plt.close()
print(X[0:30])

### you can change the output of this script by changing the limit number in submissions, and also by changing the date in the
### timestamp, and the number of stock tickers you want displayed in the graph.
