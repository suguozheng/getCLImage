# encoding:utf-8
'''
抓取某网站图片的爬虫
本程序由suger开发,一切最终解释权归于suger.
本程序为开源,只用于技术交流,只供开发者参考与学习.
不得用于违反法律以及未经许可不得用于商业.保留其追责权利.
本程序不涉及任何违法敏感因素,如有人拿程序改造成违法工具,将与本程序开发者无关.
勇于开源,请勿滥用.内部学习交流,请勿传播.违反者造成相关法律事故,自行承担刑事责任.
'''
import urllib.request, urllib.parse
import socket
import re
from savefile import saveFile
# 超时设置
socket.setdefaulttimeout(10)
'''第一步格式验证'''
# 初始输入网址,不带/斜杠
while(1):
	url=input("请输入你的域名(http开头且不带斜杠结束):")
	print("您输入的域名为:"+url)
	print("现在正在验证...")
	if(url==''):
		print('抱歉,url不能为空')
		continue
	else:
		# 验证域名格式的正确
		expression=re.compile(r"^(http://)\w{1,5}\.\w+\.\w{1,5}(?!/)$")
		result=expression.match(url)
		if(result == None):
			print("抱歉,域名格式错误!(http开头且不带斜杠结束)")
			continue
		else:
			print(result.group(0)+" 格式合法!进行下一步验证......")
			break
'''第一步验证结束'''
'''第二步地址正确验证开始'''
#
get_url=result.group(0)+"/index.php"
# 获取页面内容
def get_cent(url):
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
		req=urllib.request.Request(url=url,headers=headers)
		data=urllib.request.urlopen(url=req).read()
		data = data.decode('gbk', 'ignore')
		return data
	except Exception:
		return None

# 获取到首页内容
while(1):
	page_cenTents=get_cent(get_url)
	if(page_cenTents==None):
		slogan=input("可能因为网络原因获取内容失败,回车后重新获取!")
		continue
	else:
		break
# 正则匹配要获取的两大块
expression=re.compile(r'(((?<=<h2><a href=").+(?=">新時代的我們))|((?<=<h2><a href=").+(?=">達蓋爾的旗幟)))')
result=expression.findall(page_cenTents)
source_url=[]
if(result==[]):
	print('没有搜索到需要的信息,可能地址是错的!请重新运行本程序!')
	exit()
print("验证成功!正在搜索源......")
'''第二步地址验证结束'''
'''第三步源获取与选择'''
i=0
print("**********这就是编号开头************")
for row in result:
	source_url.append(row[0])
	str_text=str(i)+":"+source_url[i]
	print(str_text)
	i+=1
print("**********这就是编号结束************")

# 接收指令
while 1:
	source_number=input("搜索到"+str(i)+"个源,请输入您要抓取的源的编号:")
	try:
		number_get_url=url+"/"+source_url[int(source_number)]
		page = get_cent(number_get_url)
		if page != None:
			break
		else:
			print("源内容获取失败!")
			continue
	except Exception:
		print("输入有误!请重新输入:")
'''第三步结束'''
'''第四步读取选择的页面内容'''
# 帖子总页数
card_num_expression=re.compile(r'(?<=value=\"1/)\d{1,5}')
card_page_num=card_num_expression.search(page)
# 如果获取到总页数的话,就按总页数来,如果没有默认为100
if card_page_num != None:
	card_page_num=card_page_num.group(0)
else:
	card_page_num=100
# 初始页
x=1
while(x<int(card_page_num)):
	x+=1
	# 判断获取下一页信息
	if(page==None):
		number_get_down_url=number_get_url+"&search=&page="+str(x)
		page=get_cent(number_get_down_url)
		if page == None:
			continue
	# 帖子正则-查询出该页所有的合格帖子
	card_expression=re.compile(r'<h3><a href="htm_data/.+\[.{1,4}\]</a></h3>')
	card=card_expression.findall(page)
	saveFile=saveFile()
	# 图片保存地址
	save_img_path="./save_image"
	saveFile.mkdir(save_img_path)
	'''第四步结束'''
	'''第五步保存图片'''
	# 获取帖子链接和地址正则
	card_expression = re.compile(r'((?<=href=").+(?="\starget)|(?<=">).+(?=</a))')
	# 获取图片曾泽
	getImg_expression = re.compile(r"(?<=src=\')http://.+?jpg|png|jpeg(?=\')")
	for row in card:
		# 链接和标题分离
		print("任务开始!")
		card_arr=card_expression.findall(row)
		img_dir_name=save_img_path+"/"+card_arr[1]
		saveFile.mkdir(img_dir_name)
		print("创建'"+card_arr[1]+"'目录完成!")
		card_get_url=url+"/"+card_arr[0]
		# 获取全部图片地址
		card_cent=get_cent(card_get_url)
		if card_cent == None:
			continue
		img_url=getImg_expression.findall(card_cent)
		# 保存图片
		if img_url != []:
			s=1
			for row in img_url:
				save_img_name=saveFile.unique_str() + ".jpg"
				saveFile.run(row,img_dir_name,save_img_name)
				print("保存-NO"+str(s)+"'"+save_img_name+"'完成!")
				s+=1
			print(card_arr[1]+"-目录已全部获取完成!共有"+str(s-1)+"张,正等待继续获取中......")
		page=None
		print("任务已全部结束!")
	'''结束'''
