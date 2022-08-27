
import os
import tweepy
import json
from datetime import datetime, timedelta, timezone

BEARER_TOKEN = os.environ.get("SEARCH_API_BEARER_TOKEN")

def get_client():
    auth = tweepy.Client(bearer_token=BEARER_TOKEN, return_type=dict)
    return auth

def get_previous_day_utc():
    now = datetime.today().now(timezone.utc)
    prev = now-timedelta(days=1)
    start_dt = datetime.combine(prev.date(), prev.min.time())
    end_dt = datetime.combine(prev.date(), prev.max.time())
    return start_dt, end_dt

def get_search_api_tweets(query, start_time, end_time, limit):
    client = get_client()
    response = client.search_recent_tweets(query=query, 
                                        start_time=start_time, 
                                        end_time=end_time, 
                                        max_results=limit, 
                                        expansions=['author_id','geo.place_id'], 
                                        tweet_fields=['created_at',"lang","source","geo"], 
                                        user_fields=['id','name','username','location'], 
                                        place_fields=['id','country'])
    return response

def flatten_search_tweets(raw_tweets):
    tweets = []
    for data, user in zip(raw_tweets['data'], raw_tweets['includes']['users']):
      item = {
          'id': data['id'],
          'created_at': data['created_at'],
          'lang': data['lang'],
          'text': data['text'],
          'source': data['source'],
          'author_id': data['author_id'],
          'username': user['username'],
          'name': user['name'],
          'location': user['location']
      }

      tweets.append(item)
    return tweets

def save_json_to_local(_json, _filename):
    path = './task2/' + _filename
    with open(path, 'w') as out_file:
        json.dump(_json, out_file, indent=4, sort_keys=True, separators=(',',":"), ensure_ascii = False)



if __name__ == '__main__':
    
    #api parameters
    start_dt, end_dt = get_previous_day_utc()
    query = '#ecommerce -is:retweet'
    max_results = 10

    raw_tweets = get_search_api_tweets(query, start_dt, end_dt, max_results)
    #flattened_tweets = flatten_search_tweets(raw_tweets)

    file_name = 'task2-output.json'
    save_json_to_local(raw_tweets, file_name)
