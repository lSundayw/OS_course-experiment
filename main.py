from PCB import PCB
from RCB import RCB

global Resource_List
global Ready_List
global Running
global Process_List
global Block_List

Resource_List=[] # 资源列表
Ready_List=[]    # 就绪队列
Block_List=[]  # 堵塞队列
Process_List=[]  # 进程列表
Running='null'   # 现在正在运行的进程

#进程管理
#创建进程，并将进程加入就绪队列与进程列表
def Create(PID,Parent,Child,Priority):
    global Running

    #初始化进程对象
    new=PCB()
    new.PID=PID

    #检查进程父节点与子节点
    if Parent!="null":
        new.Parent=Parent.PID
    else:
        new.Parent=Parent

    if Child!="null":
        new.Child.append(Child)
    new.Priority=Priority

    for item in Process_List:
        if new.PID==item.PID:
            print("The process already exists and cannot be created again.")
            return
    #若就绪队列为空，将进程状态转为正在运行，否则加入就绪队列
    if Ready_List==[]:
        if Running=='null':
            Running=new.PID
            new.Status='running'
        else:
            new.Status='ready'
            Ready_List.append(new)
    else:
        new.Status='ready'
        Ready_List.append(new)

    Process_List.append(new)
    sort_Ready_list()

#对就绪队列按优先级排序
def sort_Ready_list():
    global Ready_List
    temp=[]
    for item in Ready_List:
        if(item.Priority==2):
            temp.append(item)
    for item in Ready_List:
        if(item.Priority==1):
            temp.append(item)
    for item in Ready_List:
        if(item.Priority==0):
            temp.append(item)
    Ready_List=temp

#对阻塞队列按优先级排序
def sort_Block_List():
    global Block_List
    temp=[]
    for item in Block_List:
        if(item.Priority==2):
            temp.append(item)
    for item in Block_List:
        if(item.Priority==1):
            temp.append(item)
    for item in Block_List:
        if(item.Priority==0):
            temp.append(item)
    Block_List=temp

#删除进程
def Delete(PID):

    global Running


    temp=Release(PID)

    for i in range(len(Block_List)):
        if Block_List[i].PID==PID:
            del Block_List[i]
            break

    for i in range(len(Ready_List)):
        if Ready_List[i].PID==PID:
            del Ready_List[i]
            break

    if(Running==PID):
        Running='null'

    Process_List.remove(temp)

    #递归调用删除该PCB的子进程PCB
    for Child in temp.Child:
        if(Child=='null'):
            return
        else:
            Delete(Child)
#时钟中断
def time_out():

    global Running
    for item in Process_List:
        if item.PID==Running:
            break
    #将正在运行的进程状态转为ready，加入就绪队列
    Ready_List.append(item)
    item.Status="ready"
    #将就绪队列第一个进程转为运行
    Running=Ready_List[0].PID
    Ready_List[0].Status="running"
    Ready_List.pop(0)

    sort_Ready_list()

#资源管理
#初始化资源，并加入资源列表
def init_resource_list():
    global  Resource_List
    #初始化资源对象，其中R1=1，R2=2，R3=3，R4=4
    for i in range(4):
        rcb=RCB()
        rcb.RID=i+1
        rcb.Remain_num=i+1
        Resource_List.append(rcb)
#释放资源
def Release(PID):
    global Running
    global temp
    #将进程对象中所占资源数与资源对象中剩余资源数更改
    for item in Process_List:
        if item.PID==PID:
            temp=item
            Resource_List[0].Remain_num+=item.Resource_occupancy[0]
            item.Resource_occupancy[0]=0
            Resource_List[1].Remain_num+=item.Resource_occupancy[1]
            item.Resource_occupancy[1]=0
            Resource_List[2].Remain_num+=item.Resource_occupancy[2]
            item.Resource_occupancy[2]=0
            Resource_List[3].Remain_num+=item.Resource_occupancy[3]
            item.Resource_occupancy[3]=0
            break

    #检查阻塞队列中的进程，看是否有可唤醒的进程
    for item in Block_List:
        if item.Block_resource_type==0:
            continue
        else:

            if item.Resource_occupancy[item.Block_resource_type-1]<=Resource_List[item.Block_resource_type-1].Remain_num:
                item.Status="ready"
                Resource_List[item.Block_resource_type].Remain_num-=item.Resource_occupancy[item.Block_resource_type-1]
                Block_List.remove(item)
                Ready_List.append(item)
                #重新调整就绪队列与阻塞队列
                sort_Block_List()
                sort_Ready_list()
                break
            else:
                continue
    return temp


#对正在运行的进程请求资源
def Request(RID,num):
    global Running


    if(Running=='null'):
        print("No running process, request resource operation failed.")
        return
    #如果资源数足够，申请资源
    if(Resource_List[RID-1].Remain_num-num<0):
        print("Not enough resources are allocated to the process")
        for item in Process_List:
            if item.PID==Running:
                temp=item
                break
        temp.Block_resource_type=RID
        temp.Resource_occupancy[RID - 1] += num
        temp.Status='blocked'
        Block_List.append(temp)
        if len(Ready_List)==0:
            Running="null"
        else:
            Running=Ready_List[0].PID
            Ready_List[0].Status='running'
            Ready_List.pop(0)

    else:
        for item in Process_List:
            if item.PID==Running:
                item.Resource_occupancy[RID-1]+=num
                Resource_List[RID-1].Remain_num-=num
    #重新调整阻塞队列
    sort_Block_List()



#Test_shell设计
#打印就绪队列
def list_readyprocess():
    p0=[]
    p1=[]
    p2=[]
    global Ready_List
    for item in Ready_List:
        if item.Priority == 0:
            p0.append(item.PID)
        if item.Priority == 1:
            p1.append(item.PID)
        if item.Priority == 2:
            p2.append(item.PID)
    pdict={0:p0,1:p1,2:p2}
    print(pdict)

#打印资源列表
def list_resource():
    global Resource_List
    Rdict={}
    for temp in Resource_List:
        if temp.RID==1:
            R1=temp.Remain_num
            Rdict['R1']=R1
        if temp.RID == 2:
            R2 = temp.Remain_num
            Rdict['R2'] = R2
        if temp.RID == 3:
            R3 = temp.Remain_num
            Rdict['R3'] = R3
        if temp.RID == 4:
            R4 = temp.Remain_num
            Rdict['R4'] = R4
    print(Rdict)

#在资源列表中寻找进程
def search_process_info(PID):
    global Process_List
    for item in Process_List:
        if item.PID==PID:
            return item
    return "null"

#打印阻塞队列
def  list_blockprocess():
    R1=[]
    R2=[]
    R3=[]
    R4=[]
    for item in Block_List:
        if item.Block_resource_type==1:
            R1.append(item.PID)
        elif item.Block_resource_type==2:
            R2.append(item.PID)
        elif item.Block_resource_type == 3:
            R3.append(item.PID)
        elif item.Block_resource_type == 4:
            R4.append(item.PID)
    dict={"R1":R1,"R2":R2,"R3":R3,"R4":R4}
    print(dict)

#Test_shell主函数
def Test_shell():
    #初始化资源列表
    init_resource_list()
    while (True):
        Running_PCB = search_process_info(Running)
        command = input("shell>").split()
        #创建进程
        if command[0] == 'cr':
            Create(PID=command[1], Parent=Running_PCB, Child="null", Priority=int(command[2]))
            new_PCB = search_process_info(command[1])
            if Running_PCB == "null":
                pass
            else:
                Running_PCB.Child.append(new_PCB.PID)
        #删除进程
        elif command[0] == 'de':
            Delete(command[1])
        #时钟中断
        elif command[0] == 'to':
            time_out()
        #请求资源
        elif command[0] == 'req':
            if command[1] == 'R1':
                Request(1, int(command[2]))

            elif command[1] == 'R2':
                Request(2, int(command[2]))

            elif command[1] == 'R3':
                Request(3, int(command[2]))

            elif command[1] == 'R4':
                Request(4, int(command[2]))

        #释放资源
        elif command[0] == 'rel':
            Release(Running)
        #查看就绪队列
        elif command[0] == 'listready':
            list_readyprocess()
        #查看资源列表
        elif command[0] == 'listres':
            list_resource()
        #查看阻塞队列
        elif command[0] == 'listblock':
            list_blockprocess()
        #输出正在运行的进程
        print("{} is running".format(Running))
#主函数
if __name__=='__main__':
    Test_shell()


