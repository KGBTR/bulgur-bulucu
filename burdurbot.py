import requests
import json
import praw
import time
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from os import environ
from datetime import date

scope = [
  "https://spreadsheets.google.com/feeds",
  "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
client = gspread.authorize(creds)
worksheet = client.open("BurdurBot").sheet1
karaliste = ""
reddit = praw.Reddit("CONFIG")
while True:
    try:
        for submission in reddit.subreddit("KGBTR").new(limit=10):
            sayac = 0
            sayac2 = 0
            linkler = []
            reply = 0
            yorumlar = []
            ensonposttarih = ""
            ensonyorumtarih = ""
            author = str(submission.author)
            url = "https://www.reddit.com/user/{}/top_karma_subreddits.json"
            r = requests.get(url.format(author), headers={"User-agent": ""})
            data = r.json()
            burdurlu = "burdurland" in str(data)
            if burdurlu == True:
                print("----------------------------------------")
                print(author, "burdurlu")
                s = requests.get(
                    "https://api.pushshift.io/reddit/submission/search/?author={}&subreddit=burdurland&limit=100".format(
                        author
                    )
                )
                submissiondata = s.json()
                sayac = 0
                sayac2 = 0
                reply = 0
                linkler = []
                yorumlar = []
                for element in submissiondata["data"]:
                    sayac = sayac + 1
                try:
                    ensonpost = submissiondata["data"][0]["created_utc"]
                    ensonposttarih = datetime.datetime.fromtimestamp(int(ensonpost))
                except:
                    print(author, "postu yok")
                    ensonposttarih = ""
                c = requests.get(
                    "https://api.pushshift.io/reddit/comment/search/?author={}&subreddit=burdurland&limit=100".format(
                        author
                    )
                )
                commentdata = c.json()
                for element in commentdata["data"]:
                    sayac2 = sayac2 + 1
                try:
                    ensonyorum = commentdata["data"][0]["created_utc"]
                    ensonyorumtarih = datetime.datetime.fromtimestamp(int(ensonyorum))
                except:
                    print(author, " yorumu yok")
                    ensonyorumtarih = ""
                sid = submission.id
                try:
                    cell = worksheet.find(sid)
                    if cell:
                        reply = 1
                        print(author, "id veritabanında var")
                        print("----------------------------------------")
                except:
                    print(author, "id veritabanında yok")
                    reply = 0
                try:
                    if reply == 0:
                        if author in karaliste:
                            reply = 1
                            print(author, "kara listede cevap verilmiyor")
                            print("----------------------------------------")
                        else:
                            reply = 0
                            print(author, "kara listede değil")
                except:
                    print("hata")
                try:
                    if reply == 0:
                        if sayac <= 2 and sayac2 <= 5:
                            reply = 1
                            print(author, "şart yerine geldi az bulgurlu")
                            print("----------------------------------------")
                        else:
                            print(author, "çok bulgurlu")
                except:
                    print("hata")
                if reply == 0:
                    submission.reply(
                        """
# Burdurlu Normie Tespit Edildi !
***
***
^{} ^Paylaşım ^Yapmış

^En ^Son ^Paylaşım ^tarihi {} GMT+0

^{} ^Yorum ^Yapmış

^En ^Son ^Yorum ^Tarihi {} GMT+0
***
^Bip ^Bop. ^Ben ^Burdurlu ^Bulucu ^Bot.
***
[Detaylı Rapor](https://burdurlukontrol.herokuapp.com/user?id={})
        """.format(
                            sayac, ensonposttarih, sayac2, ensonyorumtarih, author
                        )
                    )
                    print("Görev tamamlandı bulgurlu bildirildi")
                    print("----------------------------------------")
                    tarih = date.today()
                    worksheet.append_row([sid, author, str(tarih)])
            else:
                print(author, "burdurlu değil")
                time.sleep(5)
        print("++++++++++++++++++++++++++++++++++++++++")
        print("ilk 10 bitti")
        print("++++++++++++++++++++++++++++++++++++++++")
    except:
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("                 HATA                   ")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")