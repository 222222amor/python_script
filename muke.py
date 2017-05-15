# coding:utf-8

import xlrd
import urlparse

final_url = []
haha_list = []
data=xlrd.open_workbook('st.xlsx')
sheet = data.sheet_by_index(0)
cols = sheet.col_values(0)
data_list = []
for line in cols:
	if '.action' or '.do'in line:
		data_list.append(line.strip())
list(set(data_list))

for item in data_list:
	new_url = urlparse.urlparse(item.strip()).netloc
	if new_url not in final_url:
		if '?' in item:
			url = item.split('?')[0]
			if url.endswith('.action'):
				final_url.append(url)
			if url.endswith('.do'):
				final_url.append(url)
for line in final_url:
	repeat_url = urlparse.urlparse(line.strip()).netloc
	if line not in haha_list:
		haha_list.append(line)

with open('xxxx.txt','a') as f:
	for i in haha_list:
		f.writelines(i.strip()+'\n')