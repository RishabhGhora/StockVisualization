# Stock Visualization

# React + D3 + Flask Project

CSE 6242 project Stock price prediction tool

React + D3 + Flask project.
Note: you will need to download files from the provided links in order to make the code run.

![alt text](https://i.imgur.com/YuE6Vns.png)

## Description

This package contains all the code necessary to run our Stock Visualization UI. It contains a backend written in Python Flask that contains our machine learning models and weights. It also contains a frontend written in React that has our visualizations.

The backend contains our trained machine learning models which are LSTMs with different window sizes trained on financial and sentiment data for five stocks. We extract sentiment with the help of finBERT.

The frontend contains visualizations that will help someone analyze stock price versus sentiment, predict future stock prices by giving future predictions of sentiment, and help determine sentiment over the past week on Twitter for a certain stock.

## Installation

### Backend

1. Download the pytorch_model.bin file from here
   https://drive.google.com/file/d/1BZjW13BIMty_WhPx7uabzC7Kp6wPGtpK/view?usp=sharing

2. Place the downloaded file in the backend/finBert/model/ directory (relatively backend/finBert/model). This model is around 400 MB.
   This directory should now have 2 files config.json, pytorch_model.bin
3. Download the archive.zip file from here
   https://drive.google.com/file/d/1ApRVntmOTog9XyfVavP7SuaFFlGOMUul/view?usp=sharing

4. Unzip the archive folder and move the 3 directories twitter, reddit, stock_data
   into the backend directory. These 3 directories are around 1.3 GB total.

5. The backend server is run using pipenv please ensure you have
   python 3.7 and pipenv on your computer
   https://www.python.org/downloads/release/python-370/
   https://pypi.org/project/pipenv/

6. Rename .env.example to .env
7. CD into backend
8. Run `pipenv --python 3.7`
9. Run `pipenv install`
10. Run `pipenv run dev`
11. Now the backend server is running on http://localhost:5000

#### NOTE

This repo uses a .env file in the backend folder which contains my credentials in order to use the Twitter API.
These credentials will be valid until May 7, 2021. After this date you will need to apply for a twitter developer
account, create a project, and generate your own credentials to store in the .env file.
https://cran.r-project.org/web/packages/rtweet/vignettes/auth.html

### Frontend

Please make sure you have Node.js with npm and yarn installed and it is updated to the most
recent stable release.

CD into frontend in a new terminal window

#### With yarn

1. Run `yarn install`
2. Run `yarn start`
3. It might take a couple of min to start, if the window does not open automatically navigate to localhost:3000.

## Execution

The first graph is the Financial dashboard. Here the user can select a company and view detailed information about the stock price and sentiment on a particular day. They can see the breakdown of sentiments from tweets that day and can adjust the time period to get a detailed view.

The second graph is the Prediction graph. Here the user can experiment with different sentiment related settings to analyze predictions about the future price of a stock. The user can fine tune sentiment on a week by week basis for a certain company and see our predicted average price for that week given the user inputs. The user can see a graph that shows our prediction model for the past year to inspire confidence in the model and can then see the prediction. This graph simulates the current date as being the start of January 2020.

# Note to use the third graph please use UPPERCASE stock symbols with no special characters such as '$'

The third graph is the Recent Sentiment graph. This allows the user to enter any stock ticker and see how sentiment is about that ticker on Twitter over the past 7 days. This allows users to get an idea about how sentiment looks right now. This graph is limited because we are using the free version of twitter API which only returns 100 results per request and we are filtering by their definition of “popular” tweets which have a certain number of favorites. This is done to ensure we are not only analyzing 100 tweets from the current day with little to none activity. However, expanding this functionality with the correct Twitter API credentials (pro or educational account) would expand the number of results returned from these queries, but getting the sentiment using our model would take longer.
