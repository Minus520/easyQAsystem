# easyQAsystem（![](https://img.shields.io/badge/Python-3.6.7-blue.svg)）
my first flask project
功能：用户注册后邮箱发送确认信息，密码加密存储等。

## ********************* update history ********************* 
2019年4月项目基本功能上线（单例代码）；

2019年5月9日程序加入蓝图。原来单例源代码见/easyQAsystem/[resource](resource) 目录；

## 注：

1、python2.7版本也可以使用，但需在服务器的python安装目录/usr/lib/python2.7/site-packages/
下增加一个文件：sitecustomize.py

内容如下：

import sys
sys.setdefaultencoding('utf-8')

否则会报：UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 0: ordinal not in range(128)错误。

2、获取客户端地址：

需在nginx 配置文件中配置：proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;

然后在本程序中center.py中添加：g.user_ip = request.headers['X-Forwarded-For']

## ********************* How to use *********************

## 1 克隆到本地
git clone https://github.com/commitsession/easyQAsystem.git

## 2 安装依赖
**  automatic **

pip install -r [requiremets.text](requiremets.text)

** or manual **

依赖包下载网址:https://pypi.org/project

(我已经下载好放在/easyQAsystem/[requirementlib](requirementlib)目录下了)

linux系统安装：

python setup.py build

python setup.py install

## 3 数据库初始化
python manage.py db init

## 4 数据库迁移
python manage.py db migrate

## 5 映射数据库
python manage.py db upgrade

## 6 启动项目
python manage.py runserver

