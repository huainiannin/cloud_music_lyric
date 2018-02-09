#!usr/bin/python
#-*- conding:utf-8 -*-
import sys

#get album id
id = sys.argv[1]

from urllib.request import urlopen
jsonContent = urlopen("http://localhost:3000/album?id={0}".format(id))

#parse json
import json
jsonObject = json.loads(jsonContent.read().decode('utf-8'))
songList = jsonObject.get('songs')
songIdList = []
album = jsonObject.get('album').get('name')
album = album.replace("/","")
#汉字转拼音
album = '_'.join(lazy_pinyin(album))
print("album name is {0}".format(album))

#get song info to another list
for i in songList:
	songDict = {'id':i.get('id'),'name':i.get('name')}
	songIdList.append(songDict)

#get lyrics
print("lyric ids are{0}".format(songIdList))
lyricList = []
import re
for i in songIdList:
	lyricJson = urlopen("http://localhost:3000/lyric?id={0}".format(i.get('id')))
	lyricDict = json.loads(lyricJson.read().decode("utf-8"))
	if(lyricDict.get('lrc') and lyricDict.get('lrc').get('lyric')):
		lyric = re.sub('\[.*\]','',lyricDict.get('lrc').get('lyric'))
		lyricList.append(i.get('name'))
		lyricList.append("\n")
    templyric = lyric.split('\n')
	#get trans
	if(lyricDict.get('tlyric') and lyricDict.get('tlyric').get('lyric')):
		lyric = re.sub('\[.*\]','',lyricDict.get('tlyric').get('lyric'))
    temptlyric = lyric.split('\n')

  for i in range(len(templyric)):
      lyricList.append(templyric[i])
      if temptlyric[i]:
          lyricList.append(temptlyric[i])

#save file
file = open(album,"w+")
for i in lyricList:
	file.write(i)

file.close()

#send email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
sender = "15206651142@163.com"
receiver = '15206651142@kindle.cn'

message = MIMEMultipart()
subject = album
message['from'] = '15206651142@163.com'
message['to'] = '15206651142@kindle.cn'
message['Subject'] = Header(subject,'utf-8')

att = MIMEText(open(album,'rb').read(),'base64','utf-8')
att["Content-Type"] = 'application/octet-stream'

att["Content-Disposition"]= 'attachment; filename={0}.txt'.format(album)
message.attach(att)

smtp = smtplib.SMTP()    
smtp.connect('smtp.163.com')    
smtp.login('15206651142@163.com', '***')  
smtp.sendmail(sender,receiver,message.as_string())

smtp.quit()


