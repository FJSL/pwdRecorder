#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 使用剪切板
import pyperclip
# 读取参数表
import sys
# 序列化工具
import pickle

DB_HEADER ="---------ZQ_DB---------\n"
HINT_ACC_NOT_EXIST = 'Account does not exist'
FILENAME  ="some"

# 账号的数据模型
class Account:
	hint =''
	account = ''
	pwd = ''
	pass

#打开数据库
def openReadalbeDB():
	# 打开可读文件
	try:
		db = open(FILENAME,'r')
	except Exception :
		# 创建数据库
		createDB();
		# 数据库创建后重新打开数据库
		db = open(FILENAME,'r')
	#文件不会太大 直接全部加载等内存中
	#del the db header
	db.readline()
	return db

# 关闭数据库
def closeDB(file):
	file.close()

#chuan
def createDB():
	createdDb = open(FILENAME,"w")
	# 设置数据库的头
	createdDb.write(DB_HEADER)
	createdDb.close()

def updateDB():
	db = open(FILENAME,"w")
	# 设置数据库的头
	db.write(DB_HEADER)
	for user in accounts:
		db.write(user.hint+":"+user.account+":"+user.pwd+"\n")
		pass

def writeClipboard(astr):
	pyperclip.copy(astr)
	pyperclip.paste()
	pass

def readClipboard():#读取剪切板  
   return pyperclip.paste()


def getPWD(argv):
	cmd = argv[0]
	# find pwd by hint 
	for acnt in accounts:
		# str.find()返回下标或者-1
		if cmd in acnt.hint:
			# if find account by hint 
			# it must return the account and pwd 
			# so not write the pwd to clipboard 
			#writeClipboard(acnt.pwd)
			print("account:"+acnt.account)
			print("pwd    :"+acnt.pwd)
			return 
	#find pwd by account 
	for acnt1 in accounts:
		if acnt1.account == cmd:
			# find account by account 
			# it no need to return the account 
			# so write pwd to clipboard
			writeClipboard(acnt1.pwd)
			print("write pwd to clilpboard")
			#find the pwd so return from this function
			return
		pass
	# both not find pwd by hint and account.
	# so print some message to user 
	print("Account does not exist\n")
	pass
def addaccount(argv):
	if len(argv)!=3:
		print("param error")
		return
	user = Account()
	user.hint = argv[0]
	user.account = argv[1]
	user.pwd = argv[2]
	accounts.append(user)
	#更新到文件中
	updateDB()
	pass
def modif(argv):
	if len(argv)!=2:
		return
	for cnt in accounts:
		# 如果命令中的账号被找到
		if argv[0] == cnt.account:
			# find the account 
			# record new pwd
			lastpwd = argv[1]
			# check new pwd is correct ?
			if input("please enter pwd again:") == lastpwd:
				# change pwd 
				cnt.pwd  = lastpwd
				# update DB
				updateDB()
				return
			else:# 两次密码不一致
				print("Entered passwords differ")
		else:
			print(HINT_ACC_NOT_EXIST)
	pass
def delete(argv):
	for cnt in accounts:
		if(cnt.account == argv[0] and input("enter y to confirm:")=="y"):
			accounts.remove(cnt)
			updateDB()
			return
	print(HINT_ACC_NOT_EXIST)
#list all account with hint
def listall(argv):
	for cnt in accounts:
		print(cnt.hint+" "*(8-len(cnt.hint))+': '+cnt.account)
	pass
def cmdError(argv):
	print("cmd error")
def showHelp(argv):
	print("-pwd [hint] or -pwd [account]")
	print("-modif [account]")
	print("-add [hint] [account] [pwd]")
	print("-del [account]")
	print("-list ")
	pass
''' cmd demo   account like this  qq 1398587039  fjsl7788
	pwd   :-pwd qq        or   -pwd 1398587039
	modif :-modif qq{must account}  12345
	add   :-add qq 616626687 fjsl7788
	del   :-del 616626687  
	list  :-list 
'''

cmdList =['-pwd','-modif','-del','-add','-list','-help']
# 功能表
funcMap={
	'-pwd':getPWD,
	'-add':addaccount,
	'-modif':modif,
	'-del':delete,
	'-list':listall,
	'-help':showHelp,
	'error':cmdError,}

# 准备数据 大致是从
# 数据库里面把数据解析出来
# 构建自己的数据结构
def dealData():
	db = openReadalbeDB()
	#提示输入账号或者提示
	for cnt in db.readlines():
		# 去掉换行
		cnt.replace('\n','')
		if cnt == "" or cnt.find(":")<0: # 过滤掉空行 或者不满足协议的行
			continue
		token = cnt.split(':')
		#实例化Account对象
		acnt = Account()
		acnt.hint 	= token[0]
		acnt.account = token[1]
		acnt.pwd 	= token[2]
		accounts.append(acnt)
#声明账号集合
accounts = []

if __name__ == '__main__':
	# 预处理数据
	dealData()
	# 函数指针
	fun = funcMap.get(sys.argv[1],funcMap.get('error'))
	# 截取指令列表后面得参数
	if(len(sys.argv)>2): # 过滤掉不带参数的命令
		fun(sys.argv[2:])
	else:
		fun(sys.argv)
    