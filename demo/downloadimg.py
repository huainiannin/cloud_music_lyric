from urllib.request import urlopen
img = urlopen('http://res.hbswcx.gov.cn/hbcredit/img/FR0000894491/2018011214411379178.jpg')
file = open('album.jpg','wb+')
file.write(img.read())
file.close()
