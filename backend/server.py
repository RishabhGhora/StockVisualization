# Imports 
import os
import tweepy as tw
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
from dotenv import load_dotenv
from finBert.sentiment import get_prediction

# Load env variables
load_dotenv()

# Flask configuration
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# API for getting sentiment of popular tweets 
# in the last 7 days with finBert
@app.route('/get_sentiment', methods=['POST'])
@cross_origin()
def get_sentiment():
    date_since = str(datetime.now() - timedelta(days=7)).split(' ')[0]
    curr_date = str(datetime.now()).split(' ')[0]
    search_words = request.json['query'] + ' -filter:retweets until:'+curr_date

    # Initialize tweepy isntance
    auth = tw.OAuthHandler(os.getenv('consumer_key'), os.getenv('consumer_secret'))
    auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))
    api = tw.API(auth, wait_on_rate_limit=True)

    # Get tweets
    tweets = tw.Cursor(api.search,
                    q=search_words,
                    lang="en",
                    since=date_since,
                    result_type="popular").items(100)

    tweet_list = [tweet for tweet in tweets]
    data = {'created_at': [], 'text': [], 'favorite_count': [], 'sentiment': []}
    created_at, text, favorite_count = [], [], []
    for tweet in tweet_list:
        data['created_at'].append(str(tweet.created_at).split(' ')[0])
        data['text'].append(tweet.text)
        data['favorite_count'].append(tweet.favorite_count)

    sentiment_list = get_prediction(data['text'])
    for sentiment in sentiment_list:
        data['sentiment'].append(sentiment)

    # Create dataframe
    df = pd.DataFrame(data)

    # Get data for graphs 
    positive_df = df[df['sentiment']=='positive']
    negative_df = df[df['sentiment']=='negative']
    neutral_df = df[df['sentiment']=='neutral']
    cols = ['count', 'negative_count', 'neutral_count', 'positive_count']
    grouped_df = pd.DataFrame([], columns=cols)
    grouped_df['count'] = df['sentiment'].groupby(df['created_at']).count()
    grouped_df[['negative_count','neutral_count','positive_count']] = \
                df.groupby(['created_at','sentiment'], as_index=False)\
                .size()\
                .pivot(index='created_at', columns='sentiment', values='size')\
                    [['negative','neutral','positive']]\
                .fillna(0)
    idx_negative = negative_df.groupby(['created_at'])['favorite_count'].transform(max) == negative_df['favorite_count']
    top_negative = negative_df[idx_negative]
    idx_positive = positive_df.groupby(['created_at'])['favorite_count'].transform(max) == positive_df['favorite_count']
    top_positive = positive_df[idx_positive]
    idx_neutral = neutral_df.groupby(['created_at'])['favorite_count'].transform(max) == neutral_df['favorite_count']
    top_neutral = neutral_df[idx_neutral]
    x = pd.merge(grouped_df, top_negative, on='created_at', how='outer').fillna('N/A')
    x = x.drop(['sentiment'], axis=1)
    x = x.rename(columns={"text": "negative_text", "favorite_count": "negative_favorites"})
    x = pd.merge(x, top_positive, on='created_at', how='outer').fillna('N/A')
    x = x.drop(['sentiment'], axis=1)
    x = x.rename(columns={"text": "positive_text", "favorite_count": "positive_favorites"})
    x = pd.merge(x, top_neutral, on='created_at', how='outer').fillna('N/A')
    x = x.drop(['sentiment'], axis=1)
    x = x.rename(columns={"text": "neutral_text", "favorite_count": "neutral_favorites"})
    
    output = {}
    for index, row in x.iterrows():
        row_data = {}
        row_data['count'] = row['count']
        row_data['negative_count'] = row['negative_count']
        row_data['neutral_count'] = row['neutral_count']
        row_data['positive_count'] = row['positive_count']
        row_data['negative_text'] = row['negative_text']
        row_data['negative_favorites'] = row['negative_favorites']
        row_data['positive_text'] = row['positive_text']
        row_data['positive_favorites'] = row['positive_favorites']
        row_data['neutral_text'] = row['neutral_text']
        row_data['neutral_favorites'] = row['neutral_favorites']
        output[row['created_at']] = row_data

    return jsonify(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)