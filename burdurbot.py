import requests
import json
import praw
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from os import environ
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
client = gspread.authorize(creds)
worksheet = client.open('BurdurBot').sheet1
reddit = praw.Reddit(
    client_id=environ['client_id'],
    client_secret=environ['client_secret'],
    username='PeriodicDioxide',
    password=environ['password'],
    user_agent='u/ruzgarerik Bot')

while True:
	for submission in reddit.subreddit("KGBTR").new(limit=40):
		sayac = 0
		sayac2=0 
		linkler = []
		reply = 0
		yorumlar = []
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
			reply = 0
			linkler = []
			yorumlar = []
			for element in submissiondata['data']:
				linkler.append(element['full_link'])
				sayac=sayac+1
			c = requests.get('https://api.pushshift.io/reddit/comment/search/?author={}&subreddit=burdurland'.format(author))
			commentdata = c.json()
			for element in commentdata['data']:
				sayac2=sayac2+1
				yorumlar.append(element['body'])
			sid = submission.id
			try:
				cell = worksheet.find(sid)
				if cell:
					reply = 1
	
			except:
				print("id veritabanında yok")
				reply = 0

			if reply == 0:
				submission.reply('''
# Burdurlu Normie Tespit Edildi !
***
# Bu Kişinin burdurland subredditindeki paylaşımları:
{}
***
# Bu kişinin burdurland subredditindeki yorumları:
{}
***
## {} paylaşım yapmış
## {} yorum yapmış
***

Bip Bop. Ben Burdurlu Bulucu Bot. 
[Beni Yapan Kişi](https://www.reddit.com/user/ruzgarerik) [Sorun Bildir](https://www.reddit.com/message/compose/?to=PeriodicDioxide)

***
'''.format(linkler,yorumlar,sayac,sayac2))
				print("Görev tamamlandı bulgurlu bildirildi")
				worksheet.append_row([sid])

		else:
			sid = submission.id
			try:
				cell = worksheet.find(sid)
				if cell:
					reply = 1
				else:
					reply = 0

			print(author, "bulgursuz")

			if reply == 0:
				submission.reply("Bulgurlu değilsin. İyi günler. ")
				worksheet.append_row([sid])

		time.sleep(2)
	print("Soğuma zamanı")
	time.sleep(15)
