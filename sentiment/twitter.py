from re import S
import requests
import time
from datetime import datetime, date

bearer_token = "AAAAAAAAAAAAAAAAAAAAAM01KwEAAAAAG%2BCXwrqH9tqlzgJfhaX5zHKUl3M%3DyKnVr7Yon9T3E5EoidlYDtBVaypIeEVl9l4mghYoUd9hVOLUIr"

def create_url(pagination_token=None, search=None):
    max_result = 100
    fields = 'in_reply_to_user_id,author_id,created_at,conversation_id'
    query = "lang:id -RT telkomuniversity OR universitastelkom OR telkom university -is:retweet"
    url = f'https://api.twitter.com/2/tweets/search/recent?query={query}&tweet.fields={fields}&max_results={max_result}&next_token={pagination_token}'
    
    if search:
        search = search.replace(' ', ' OR ')
        query = f'lang:id -RT {search} -is:retweet'

    if pagination_token == None:
        url = f'https://api.twitter.com/2/tweets/search/recent?query={query}&tweet.fields={fields}&max_results={max_result}'
    
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_next_token(json_response):
    if 'next_token' not in json_response['meta']:
        return None

    next_token = json_response['meta']['next_token']
    return next_token


def get_data(tweets, query, next_token=None):
    url = create_url(pagination_token=next_token, search=query)
    json_response = connect_to_endpoint(url)

    results = json_response.get('data', None)

    if results:
        for res in results:
            created_at = date.today()

            if res.get('created'):
               created_at = datetime.strptime(res['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")

            month = datetime.strftime(created_at, "%B")
            year =  datetime.strftime(created_at, "%Y")
            created_at = datetime.strftime(created_at, "%Y-%m-%d")
            
            tweet = {
                'text' : res['text'],
                'created_at' : created_at ,
                'month': month,
                'year': year
            } 

            tweets.append(tweet)

            if len(tweets) >= 200:
                break

    return json_response, tweets


def get_tweets(query):
    tweets = []
    json_response, tweets = get_data(tweets, query)

    if len(tweets) != 0:
        next_token = get_next_token(json_response)

        while next_token:
            json_response, tweets = get_data(tweets, query, next_token)
            next_token = get_next_token(json_response)

            if next_token == None:
                json_response, tweets = get_data(tweets, query, next_token)
                break

            if (len(tweets) >= 200):
                break
            
            time.sleep(5)

    return tweets
    