# encoding:UTF-8
'''
这个是保存文件的类
'''
import os
import uuid
import urllib.request, urllib.parse

'''保存文件'''
class saveFile :
	def __init__(self):
		self.Error=""

	# 获取文件后缀名
	def getFileExtension(self,file):
		return os.path.splitext(file)[1]
	# 创建文件目录,并返回该目录
	def mkdir(self,path):
	    # 去除左右两边的空格
	    path=path.strip()
	    # 去除尾部 \符号
	    path=path.rstrip("\\")

	    if not os.path.exists(path):
	        os.makedirs(path)

	    return path
	# 自动生成一个唯一的字符串，固定长度为36
	def unique_str(self):
		return str(uuid.uuid1())

	'''
	抓取网页文件内容，保存到内存

	@url 欲抓取文件 ，path+filename
	'''

	def get_file(self,url):
		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
			req = urllib.request.Request(url=url, headers=headers)
			data = urllib.request.urlopen(url=req).read()
			return data
		except BaseException:
			return None

	'''
	保存文件到本地

	@path  本地路径
	@file_name 文件名
	@data 文件内容
	'''

	def save_file(self,path, file_name, data):
		if data == None:
			return None

		self.mkdir(path)
		if (not path.endswith("/")):
			path = path + "/"
		try:
			file = open(path + file_name, "wb")
			file.write(data)
			file.flush()
			file.close()
			return True
		except Exception:
			return None

	'''
		运行

		@get_path  获取路径
		@save_path 保存路径
		@save_name 保存名称
		'''
	def run(self,get_path,save_path=None,save_name=None):
		data=self.get_file(get_path)
		if(data == None):
			self.Error="图片获取失败,地址可能有错!"
			return None
		if(save_path==None):
			save_path="./save_image"
		if(save_name==None):
			save_name=self.unique_str()+self.getFileExtension(get_path)

		status=self.save_file(save_path,save_name,data)
		if(status==None):
			self.Error="图片保存失败!"
			return  None
		else:
			return True
# img_src="http://www.rmdown.com/apk.png"
# saveFile=saveFile()
# status=saveFile.run(img_src,'./ceshi')





