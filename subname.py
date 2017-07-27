#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import requests
import sys
import os


#删除过程文件函数
def removefile(filename):
	if os.path.exists(filename):
		os.remove(filename)

#去除列表中的空格和换行
def removelistspecial(list):
	newlist=[]
	for i in range(0,len(list)):
		temp=list[i].strip()
		temp=temp.strip("\n")
		newlist.append(temp)
	return newlist

# ip地址转化为C段
def iptransc(list):
	c_list=[]
	for each in list:
		temp=each.split(".")
		temp[3]='0'
		c='.'.join(temp)
		c_list.append(c)
	return c_list

#列表去重
def norepetlist(list):
	return sorted(set(list), key = list.index)


# 格式化subdommain结果域名和IP到两个文件
def cut():
	with open(resulut,"r") as f:
		for line in f:
			line.strip();
			bottle=line.split("\t"); 
			subfile=open("result/subdomain.log","a") 
			subfile.write(bottle[0]+"\n")
			subfile.close()
			ipfile=open("result/ip.log","a")
			removelistspecial(bottle)
			if "," in bottle[len(bottle)-1]:
				t=bottle[len(bottle)-1]
				ip=t.split(",")
				templist=removelistspecial(ip)
				for i in range(int(len(templist))):
					ipfile.write(templist[i]+"\n")
			else:
				ipfile.write(bottle[len(bottle)-1])
			ipfile.close()
	f.close()

# 将筛选出的私有IP去除并去重
def ip():
	print "正在进行C段地址整理与统计："
	with open("result/ip.log","r") as f:
		for line in f:
			t=line.split(".")
			if t[0]=="172" or t[0]=="192" or t[0]=="10":
				continue
			else:
				file=open("result/middle_ip.log","a")
				file.write(line)
				file.close
	f.close()
	removefile("result/ip.log")
	middle=open("result/middle_ip.log","r")
	temp=middle.readlines()
	new_temp=[]
	for ip in temp:
		if ip not in new_temp:
			new_temp.append(ip)
	new_temp=removelistspecial(new_temp)
	middle.close()
	removefile("result/middle_ip.log")
	repetclist=iptransc(new_temp)
	norepetclist=norepetlist(repetclist)
	cfile=open("result/c_ip.log","a")
	for each in norepetclist:
		count=0
		for statment in repetclist:
			if statment in each:
				count=count+1
		z="有%d个地址出现在网段%s"%(count,each)
		print z
		cfile.write(z+"\n")
	cfile.close()
	finalip=open("result/final_ip.log","a")
	for i in range(0,len(new_temp)-1):
		 finalip.write(new_temp[i]+"\n")
	finalip.close()

# 对爆出的域名进行请求测试
def url():
	print "正在对子域名可用性进行检测："
	code_404=[]
	code_200=[]
	code_unknown=[]
	connet_timeout=[]
	with open("result/subdomain.log","r") as f:
		for line in f:
			try:
				k=line.splitlines()
				t="http://"+k[0].strip()
				r=requests.get(url=t,timeout=5)
				print t+"\t"+"status is："+str(r.status_code)
				if r.status_code==200:
					code_200.append(t)
				elif (r.status_code)==404:
					code_404.append(t)
				elif (r.status_code!=200 and r.status_code!=404):
					code_unknown.append(t)
			except:
				print "超时:"+t
				connet_timeout.append(t)
	f.close()
	finalsub=open("result/subdomain.html","a")
	finalsub.write("200的网页有"+"<br>"+"<br>")
	writehtml(finalsub,code_200)
	finalsub.write("404的网页有"+"<br>"+"<br>")
	writehtml(finalsub,code_404)
	finalsub.write("未知状态码的网页有"+"<br>"+"<br>")
	writehtml(finalsub,code_unknown)
	finalsub.write("超时网页有"+"<br>"+"<br>")
	writehtml(finalsub,connet_timeout)
	finalsub.close()


def writehtml(filecontrol,list):
	for n in range(0,len(list)-1):
		temp="<a href="+list[n]+" "+"target=\"_blank\">"+list[n]+"</a>"+"<br>"
		filecontrol.write(temp)			
	
if __name__ == '__main__':
	try:
		resulut=sys.argv[1];
		removefile("result/subdomain.log")
		removefile("result/final_ip.log")
		removefile("result/subdomain.html")
		removefile("result/c_ip.log")
		cut()
		ip()
		url()
	except:
		print "useage:python subname.py (filename)"