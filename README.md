# 操作系统课程实验

## 设计语言

python

## 文件描述

PCB.py 实现PCB设计

RCB.py 实现RCB设计

main.py 实现进程与资源管理、Test shell设计

## 模块介绍

PCB设计：

```python
class PCB(object):
    def __init__(self):
        self.PID='' #进程名
        self.Status='' #进程状态
        self.Child=[] #子进程
        self.Parent='null' #父进程
        self.Priority=0 #优先级为0，1，2
        self.Resource_occupancy=[0,0,0,0]    #当前占有四类资源数
        self.Block_resource_type=0    #引起阻塞资源的种类,1为R1，2为R2，3为R3，4为R4
```

RCB设计：

```python
class RCB(object):
    def __init__(self):
        self.RID=0  #资源名
        self.Remain_num=0   #剩余资源数
```

进程管理模块:

1.创建进程，并将进程加入就绪队列与进程列表

```python
def Create(PID,Parent,Child,Priority)
```

2.对就绪队列按照优先级排列

```python
def sort_Ready_list()
```

3.对阻塞队列按照优先级排列

```python
def sort_Block_List()
```

4.删除进程

```python
def Delete(PID)
```

5.时钟中断

```python
def time_out()
```

资源管理模块：

1.初始化资源列表

```python
def init_resource_list()
```

2.释放资源

```python
def Release(PID)
```

3.对正在运行的进程请求资源

```python
def Request(RID,num)
```

Test shell设计：

首先初始化资源列表，后输入以下命令：

1.cr PID Priority   创建新进程命令

调用Create(PID,Parent,Child,Priority)函数

2.de PID 删除进程命令

调用Delete(PID)函数

3.to 时钟中断命令

调用time_out()函数

4.req RID num 请求资源命令

调用Request(RID,num)函数

5.rel PID 释放资源命令

调用Release(PID)函数

6.listready 打印就绪队列命令

调用list_readyprocess()函数

7.listres 打印资源列表命令

调用list_resource()函数

8.listblock 打印阻塞队列命令

调用list_blockprocess()函数

