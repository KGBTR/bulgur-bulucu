import requests
import json
import praw
import time
from os import environ
reddit = praw.Reddit(
    client_id=environ['client_id'],
    client_secret=environ['client_secret'],
    username='PeriodicDioxide',
    password=environ['password'],
    user_agent='u/ruzgarerik Bot')



while True:
	for submission in reddit.subreddit("KGBTR").new(limit=1500):
	    author = submission.author
	    print(author)
	    url = "https://www.reddit.com/user/{}/top_karma_subreddits.json"
	    r = requests.get(url.format(author), headers = {'User-agent': 'u/ruzgarerik bot'})
	    data = r.json()
	    burdurlu = "burdurland" in str(data)
	    if burdurlu == True:
	    	submission.reply('''
	    		# Burdurlu Normie Tespit Edildi !
	    		***
	    		## Bu Yorum Burdurlu Bulucu Bot Tarafından Yapılmıştır
	    		''')
	    	print("Görev tamamlandı bulgurlu bildirildi")
	    else:
	    	print(author, "bulgursuz")
	    time.sleep(20) 