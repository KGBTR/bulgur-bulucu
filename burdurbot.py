import requests
import json
import praw
import time
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from os import environ
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
client = gspread.authorize(creds)
worksheet = client.open('BurdurBot').sheet1
reddit = praw.Reddit(
    client_id='BXftGrRszEp0GQ',
    client_secret='2_qNIZ1x5Z1T4PdP4aqSXGBO67w',
    username='PeriodicDioxide',
    password='19931993',
    user_agent='u/ruzgarerik Bot')
keyphrase = 'u/PeriodicDioxide'
print("---BOT BAŞLIYOR---")
while True:
	for submission in reddit.subreddit("KGBTR").new(limit=10):
		for comment in submission.comments:
			if keyphrase in comment.body:
				print("istek var")
				sayac = 0
				sayac2=0 
				linkler = []
				reply = 0
				yorumlar = []
				ensonposttarih=""
				ensonyorumtarih=""
				author = str(submission.author)
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
						sayac=sayac+1
					try:
						ensonpost = submissiondata['data'][0]['created_utc']
						ensonposttarih = datetime.datetime.fromtimestamp(int(ensonpost))
					except:
						print(author,"postu yok")
						ensonposttarih = ""
					c = requests.get('https://api.pushshift.io/reddit/comment/search/?author={}&subreddit=burdurland'.format(author))
					commentdata = c.json()
					for element in commentdata['data']:
						sayac2=sayac2+1


					try:
						ensonyorum = commentdata['data'][0]['created_utc']
						ensonyorumtarih = datetime.datetime.fromtimestamp(int(ensonyorum))

					except:
						print(author," yorumu yok")
						ensonyorumtarih = ""
						
					sid = submission.id
					

					try:
						cell = worksheet.find(sid)
						if cell:
							reply = 1
					except:
						print("id veritabanında yok")
						reply = 0




					if reply == 0:
						comment.reply('''
# Burdurlu Normie Tespit Edildi !
***
{}
***
^{} ^Paylaşım ^Yapmış

^En ^Son ^Paylaşım ^tarihi {} ^GMT+0

^{} ^Yorum ^Yapmış

^En ^Son ^Yorum ^Tarihi {} ^GMT+0
***
^Bip ^Bop. ^Ben ^Burdurlu ^Bulucu ^Bot. 
^Son ^Güncelleme ^23 ^Temmuz ^2020
^Bir ^posta ^sadece ^bir ^kere ^geliyorum

[Beni Yapan Kisi](https://www.reddit.com/user/ruzgarerik) [Sorun Bildir](https://www.reddit.com/message/compose/?to=PeriodicDioxide)
***
			'''.format(author,sayac,ensonposttarih,sayac2,ensonyorumtarih))
						print("Görev tamamlandı bulgurlu bildirildi")
						worksheet.append_row([sid,author,'Yeni bot'])
					else:
						print("Daha önceden cevap verildi")

				else:
					print(author, "bulgursuz")
					if reply == 0:
						comment.reply('''
# {} Burdurlu Değil
***
^Bip ^Bop. ^Ben ^Burdurlu ^Bulucu ^Bot.

[Beni Yapan Kisi](https://www.reddit.com/user/ruzgarerik) [Sorun Bildir](https://www.reddit.com/message/compose/?to=PeriodicDioxide)
	'''
		.format(author))
						print("bildirildi")
						worksheet.append_row([sid,'Yeni bot'])

				
			print("Kontrol")
