# FileSystem-Simulation
UFS simulation in python

UFS 1.0

# UFS模拟文件系统 使用说明




## 使用环境：

操作系统环境：各操作系统平台通用

语言环境：python3.x

第三方库：numpy



## 使用方法：

在windows环境下打开cmd窗口 ，或者在Unix/ Linux/Mac os环境下打开terminal窗口，进入该文件夹后，可选择建立虚拟环境或者系统环境，输入以下命令。

1.若无安装numpy，请输入：
	pip install numpy
	或者
	pip install –r requirements.txt
  
2.python server.py 启动文件系统服务器。使文件系统在后台运行。

3.server启动后，新建cmd/terminal窗口输入：python client.py 启动文件系统用户端。根据需求打开多个终端运行用户端可以体验多进程操作。

4.打开客户端后，请尽情输入Linux系统命令。输入：help可以查看可支持的命令以及语法。

5.退出时，直接关闭cmd/terminal窗口即可。

## 命令说明：

    stat [name] 输入文件名 在当前目录下查看文件信息

    cd  [name]  输入文件夹名 在当前目录下进入该文件夹

    cd ..	  返回上一层

    ls  列出当前文件夹所有文件名

    mkdir  [name] 输入新文件夹名在当前文件夹下创建新文件夹

    rmdir  [name]	输入文件夹名在当前文件夹下删除该文件夹

    rm [name] 输入文件名在当前文件夹下删除该文件夹

    find  [name]  输入文件名在当前文件夹以及所有子文件夹下查找文件

    more  [name]  输入文本文件名查看文本文件内容

    cp  [name1]  [name2]  输入原文件名以及新文件名在当前目录下将原文件复制成新文件

    import [name1] [name2]  输入本地文件系统文件名以及新文件名在当前目录下将本地系统文件导入成新文件

    export [name] [path]  输入文件名和路径件名在当前目录下将本地系统文件导出成新文件

    clear 输出10个换行符

    exit  退出系统

## 文件系统默认参数：

    文件系统大小：1GB

    系统位数：64

    inode大小：128KB

    inode密度：2048

    数据块大小：8KB

    数据块索引大小：4KB

    数据块数量：120000

## 其他事项

1.由于在电脑内存中模拟，请根据电脑性能效果，在file_system/structure.py文件里Superblock类里__init__函数中修改默认入口参数。
主要是修改数据块数量或者数据块大小。

2.请不要在server服务开启前开启client端。

3.本系统理论上最大支持16GB左右的单个文件读写存储操作。但一般电脑内存无法支持。请在系统可支持的范围下操作。

4．本系统根目录带有测试图片文件和测试文本文件，程序内部做了路径处理，以减少输入路径因不同环境下产生的差错。若要测试自己的文件请放置在UFS 1.0文件夹下。

可使用如下命令：
    
    import a.png b.png 	在项目文件夹下导入a.png 为b.png
    
    export b.png c.png 	在项目文件夹下导出b.png 为c.png
  
    import a.txt b.txt 	在项目文件夹下导导入a.txt 为b.txt

    export b.txt c.txt 	在项目文件夹下导导出b.txt 为c.txt
  
    more b.txt  查看b.txt文本文件


