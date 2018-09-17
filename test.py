import time
import requests
import redis

redis_client = redis.Redis.from_url()

redis_client.set('latest_id', None)

while True:
    article_list = requests.get('https://api.spaceflightnewsapi.net/articles?limit=1').json()
    for article in article_list:
        if article['_id'] == redis_client.get('latest_id').decode():
            print('niets')
            continue
        else:
            print('new article')
            redis_client.set('latest_id', article['_id'])
    time.sleep(10)
