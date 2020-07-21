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
	for submission in reddit.subreddit("KGBTR").new(limit=100):
		sayac = 0
		sayac2=0 
		linkler = []
		author = submission.author
		print(author)
		url = "https://www.reddit.com/user/{}/top_karma_subreddits.json"
		r = requests.get(url.format(author), headers = {'User-agent': 'u/ruzgarerik bot'})
		data = r.json()
		burdurlu = "burdurland" in str(data)

		if burdurlu == True:
			s = requests.get('https://api.pushshift.io/reddit/submission/search/?author={}&subreddit=burdurland'.format(author))
			submissiondata = s.json()
			sayac=0
			sayac2=0
			linkler = []
			for element in submissiondata['data']:
				linkler.append(element['full_link'])
				sayac=sayac+1
			c = requests.get('https://api.pushshift.io/reddit/comment/search/?author={}&subreddit=burdurland'.format(author))
			commentdata = c.json()
			for element in commentdata['data']:
				sayac2=sayac2+1
			submission.reply('''
# Burdurlu Normie Tespit Edildi !
***
# Bu Kişinin r/burdurland subredditindeki paylaşımları:
{}
***
## {} paylaşım yapmış
## {} yorum yapmış
***
# Bu Yorum Burdurlu Bulucu Bot Tarafından Yapılmıştır
***
'''.format(linkler,sayac,sayac2))
			print("Görev tamamlandı bulgurlu bildirildi")
		else:
			print(author, "bulgursuz")
		time.sleep(5) 