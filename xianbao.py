import threading
import time
import tkinter as tk

from lxml import etree
import requests
import webbrowser
import re
class Spider(object):
	url = 'http://www.taolu5.com/sort/x?q='
	page = 'http://www.taolu5.com/sort/x/page/'
	Total_page = 1
	currentPage = 1
	xianbao_href = []
	xianbao_title = []
	xianbo_time = []
	pages_url = []
	def index_request(self):
		self.currentPage = 0
		self.xianbo_time = []
		self.xianbao_href = []
		self.xianbao_title = []
		response=requests.get(self.url)
		html = etree.HTML(response.text)
		href = html.xpath('//html/body/div[2]/div[2]/a/@href')
		title = html.xpath('//html/body/div[2]/div[2]/a/text()')
		ContentTime = html.xpath('//html/body/div[2]/div[2]/a/span/text()')
		count = 0
		for i in range(0,len(title)):
			if i%2 == 1:
				count +=1
				if count >5:
					# 匹配时间
					res = re.findall('\d{2}:\d{2}:\d{2}',ContentTime[int((i-1)/2)],re.S)
					self.xianbo_time.append(res[0])
					self.xianbao_title.append(title[i])
		count = 0
		for i in href:
			count += 1
			if count > 5:
				self.xianbao_href.append(i)
		self.StartGetContent()
		self.DisplyContent()
	def getOnePageContent(self,pageurl):
		response = requests.get(pageurl)
		html = etree.HTML(response.text)
		href = html.xpath('//html/body/div[2]/div[2]/a/@href')
		title = html.xpath('//html/body/div[2]/div[2]/a/text()')
		ContentTime = html.xpath('//html/body/div[2]/div[2]/a/span/text()')
		for i in range(0,len(title)):
			if i%2 == 1:
				res = re.findall('\d{2}:\d{2}:\d{2}', ContentTime[int((i - 1) / 2)], re.S)
				self.xianbo_time.append(res[0])
				self.xianbao_title.append(title[i])
		for i in href:
			self.xianbao_href.append(i)
		# print('当前爬取第 %d 页···'% self.currentPage)
	def setGetContentPage(self,pagesnum):
		self.Total_page = pagesnum
		for i in range(0,pagesnum):
			url = (self.page+str(i+2))
			self.pages_url.append(url)
			# print(url)
	def StartGetContent(self):
		for i in self.pages_url:
			self.getOnePageContent(i)
			time.sleep(1)
			self.currentPage += 1

	def DisplyContent(self):
		# print('爬取 完毕！！！')
		text1.delete(0.0, 'end')
		listbox.delete(0, 'end')
		text3.delete(0.0 ,'end')
		text3.update()
		listbox.update()
		text1.update()
		cnt = 0
		for tc,th in zip(self.xianbao_title,self.xianbao_href):
			text1.insert('end', tc + "\n")
			listbox.insert(cnt, th)
			text3.insert('end',self.xianbo_time[cnt] + '\n')
			cnt += 1

def click(event):
	url = listbox.get((listbox.curselection()))
	webbrowser.open(url)
def getAllcontent():
	spider=Spider()
	# 设置爬取页数
	spider.setGetContentPage(1)
	while True:
		spider.index_request()
		time.sleep(10)
if  __name__== '__main__':
	master = tk.Tk(className='线报监控By QQ 3378954580')
	# 禁止修改窗口大小
	master.resizable(False, False)
	text1 = tk.Text(master,width=60,height=40,font=('宋体',15))
	text1.grid(row=0,column=0,padx=5,pady=5)
	text3 = tk.Text(master,width=10,height=40,font=('宋体',15))
	text3.grid(row=0,column=1,padx=5,pady=5)
	listbox = tk.Listbox(master,width=40,height=38,font=('宋体',15))
	listbox.grid(row=0,column=2,padx=5,pady=5)
	text1.insert('current','Update----')
	text3.insert('current', 'Update--')
	listbox.bind('<Double-Button-1>',click)
	T1 = threading.Thread(target=getAllcontent)
	T1.start()
	tk.mainloop()

