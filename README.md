# 打包编译python项目中的py文件

##### 支持系统

- ubuntu 
- centos7

##### build_linux简介

- build_linux可以将python文件转化为so文件，达到加密python文件的目的
- build_linux仅支持加密一整个python项目，如想要加密一个py文件，单独创建一个目录并在目录下放置sbin 文件和 py 文件进行加密
- .py生成的.so文件可以被主文件通过 "from module import *" 调用
- build_linux可以自动识别项目中的py文件, 如果项目中某些文件你不想加密，build_linux也可以实现你的目的
- 项目加密完成后，在sbin目录下生成release/censos 目录，路径下就是加密后的项目目录
- build_linux支持 python3

##### 环境配置

```
sudo yum -y install gcc python-devel Cython python3-devel
```

- 安装一些必要的库

##### 使用说明

```
1. 在linux系统中切换至项目路径下的sbin目录
2. 执行命令：python3 build_linux.py -r
3. 不想进行编译的目录，直接拷贝至副本项目中，在 ign_dirs 列表中添加目录名，
4. 不想编译的py文件，将py文件直接拷贝至副本项目中，在 ign_files 列表中添加py文件名
5. 不想出现在副本项目中的目录，编译完成后，舍弃掉的目录，通过exclude += ' --exclude=".idea"'添加

options:
	-r : 删除sbin目录下原有的release目录，没有此参数不执行删除
```

- 执行脚本后，会自动检测到项目根路径，并将路径下目录中的py文件加密

##### 备注：

项目打包完成后，将启动（例：run.py  start.py）文件放置在原有的路径下，即可启动项目