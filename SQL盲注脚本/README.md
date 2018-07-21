# 使用

#### 查询数据库
python main.py url db_name

![](../images/sqli-1.png)

![](../images/sqli-2.png)

#### 查询数据库版本
python main.py url db_version

![](../images/sqli-3.png)

![](../images/sqli-4.png)

#### 查表

- 如果要查其他数据库，更改main.py的53行中的database()
- database() - > security

python main.py url table_name

![](../images/sqli-5.png)

![](../images/sqli-6.png)

代码写得很烂，学习是一个过程。

安慰自己：大佬也是从这么烂的代码一路过来的