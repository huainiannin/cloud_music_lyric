#引入python系统模块
import sys
#获取专辑id
id = sys.argv[1]
#引入http请求模块
from urllib.request import urlopen
jsonContent = urlopen("http://localhost:3000/album?id={0}".format(id))
#解析json
import json
jsonObject = json.loads(jsonContent.read().decode('utf-8'))

