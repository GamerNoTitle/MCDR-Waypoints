# -*- coding: utf-8 -*-
import json as js
import re
import csv
import os
from imp import load_source
PlayerInfoAPI = load_source('PlayerInfoAPI','./plugins/PlayerInfoAPI.py')
path='./config/Waypoints.csv'   # 路径点保存位置
prefix_short='!!wp'
prefix='!!waypoints'
name=[]
x=[]
y=[]
z=[]
dimension=[]
complicated=False
help_msg='''
======== §bWaypoints §r========
§6欢迎使用由@GamerNoTitle开发的路径点插件！
§6你可以在Github搜索MCDR-Waypoints找到本项目！
本插件中§d!!wp§r与§d!!waypoints§r效果相同，两者可以互相替换
§b!!wp§r显示本帮助信息
§b!!wp list§r显示路径点列表
§b!!wp search <content>§r搜索含有指定内容名字的路径点
§b!!wp show <content> (dim)§r显示名字为指定内容的导航点信息（dim为维度，主世界/地狱/末地/全部维度分别对应0/1/-1/all，默认为当前维度）
§b!!wp dim <dim>§r显示在主世界/地狱/末地的所有导航点（分别对应dim：0,-1,1）
§b!!wp add <name> (x) (y) (z) (Dimension) §r添加名为<name>的路径点（x,y,z指定坐标，Dimension为维度，0是主世界，-1是地狱，1是末地，非必须）
§b!!wp del <name>§r删除名为<name>的路径点（需要MCDR.helper以上权限）
§b!!wp reload§r重载路径点列表
'''
def refresh_list():
    global name,x,y,z,dimension,complicated
    database=csv.reader(path)
    name=[]
    x=[]
    y=[]
    z=[]
    dimension=[]
    file=open(path,'r',encoding='gbk')
    database=csv.reader(file)
    for i in database:
        name.append(i[0])
        x.append(i[1])
        y.append(i[2])
        z.append(i[3])
        dimension.append(i[4])
    complicated==False

def create_csv(path):
    with open(path,"w+",newline='',encoding="gbk") as file:
        file.close()

def append_csv(path,data):
    with open(path,"a+",newline='',encoding="gbk") as file:
        csv_file = csv.writer(file)
        data=[data]
        csv_file.writerows(data)

def add(server,info,message):
    if len(message) == 2:
        server.tell(info.player, '§b[Waypoints]§4你必须输入路径点的名字！')
    elif len(message) == 3:
        nbt=get_pos(server,info)
        pos=list(nbt['Pos'])
        Dimension=nbt['Dimension']
        x=int(list(pos)[0])
        y=int(list(pos)[1])
        z=int(list(pos)[2])
        data=[str(message[2]),str(x),str(y),str(z),str(Dimension)]
        append_csv(path,data)
        refresh_list()
        server.tell(info.player, '§b[Waypoints]§r导航点[name: {}, x: {}, y: {}, z: {}, dim: {}]已添加！'.format(message[2],x,y,z,Dimension))
    elif len(message) == 6:
        x=message[3]
        y=message[4]
        z=message[5]
        nbt=get_pos(server,info)
        Dimension=nbt['Dimension']
        data=[message[2],x,y,z,Dimension]
        append_csv(path,data)
        refresh_list()
        server.tell(info.player, '§b[Waypoints]§r导航点[name: {}, x: {}, y: {}, z: {}, dim: {}]已添加！'.format(message[2],x,y,z,Dimension))
    elif len(message) == 7:
        x=message[3]
        y=message[4]
        z=message[5]
        try:
            Dimension=int(message[6])
            if Dimension>1 or Dimension<-1:
                server.tell(info.player,'§b[Waypoints]§4你必须输入介于-1到1之间的整数！')
            else:
                data=[message[2],x,y,z,Dimension]
                append_csv(path,data)
                refresh_list()
                server.tell(info.player, '§b[Waypoints]§r导航点[name: {}, x: {}, y: {}, z: {}, dim: {}]已添加！'.format(message[2],x,y,z,Dimension))
        except:
            server.tell(info.player,'§b[Waypoints]§4你必须输入整数！')
    else:
        server.tell(info.player, '§b[Waypoints]§4输入格式不正确！')    

def is_duplicated(point):
    i=0
    for i in range(len(name)):
        if point==name[i]:
            global complicated
            complicated=True

def delete(server,info,point):
    point_pos=None
    for i in range(0,len(name)):
        if point == name[i]:
            point_pos=i
    if point_pos == None:
        server.tell(info.player, '§b[Waypoints]§4未找到名为§d{}§4的路径点！'.format(point))
    else:
        for i in range(point_pos,len(name)):
            try:
                name[i] = name[i+1]
                x[i] = x[i+1]
                y[i] = y[i+1]
                z[i] = z[i+1]
                dimension[i] = dimension[i+1]
            except:
                None
        del(name[len(name)-1])
        del(x[len(x)-1])
        del(y[len(y)-1])
        del(z[len(z)-1])
        del(dimension[len(dimension)-1])
        os.remove(path)
        create_csv(path)
        for i in range(0,len(name)):
            data=[name[i],x[i],y[i],z[i],dimension[i]]
            append_csv(path,data)
        refresh_list()


def showdetail(server,info,point):
    is_exist=False
    for i in range(0,len(name)):
        if point == name[i]:
            is_exist=True
            detail='[name: {}, x: {}, y: {}, z: {}, dim: {}]'.format(point,x[i],y[i],z[i],dimension[i])
    if is_exist:
        server.tell(info.player, '§b[Waypoints]§r导航点§d{}§r的信息：{}'.format(point,detail))
        is_exist=False
    else:
        server.tell(info.player, '§b[Waypoints]§4未查询到名为§d{}§4的导航点的相关信息！'.format(point))

def showlist(server,info):
    if len(name) == 0:
        server.tell(info.player, '§b[Waypoints]§6导航点列表还是空荡荡的哦~')
    else:
        pointlist=''
        for i in range(0,len(name)):
            if i==len(name):
                pointlist=pointlist+name[i]
            else:
                pointlist=pointlist+name[i]+', '
        server.tell(info.player, '§b[Waypoints]§r数据库中有以下导航点： {}'.format(pointlist))
        server.tell(info.player, '§b[Waypoints]§r你可以使用§b!!wp show <name> §r来展示导航点的相关信息')

def search(server,info,point,dim):
    result=[]
    if dim == 'all':
        for i in range(0,len(name)):
            if point in name[i]:
                result.append(name[i])
        if result == []:
            server.tell(info.player, '§b[Waypoints]§4暂时没有含有§d{}§4关键词的路径点哦~'.format(point))
        else:
            server.tell(info.player, '§b[Waypoints]§r含有关键词§d{}§r的路径点有§6{}'.format(point,result))
            server.tell(info.player, '§b[Waypoints]§r你可以使用§b!!wp show <name> §r来展示导航点的相关信息')
    elif int(dim) == 1 or int(dim) == -1 or int(dim) == 0:
        for i in range(0,len(name)):
            if point in name[i] and int(dimension[i]) == dim:
                result.append(name[i])
        if result == []:
            server.tell(info.player, '§b[Waypoints]§4暂时没有含有§d{}§4关键词的路径点哦~'.format(point))
        else:
            server.tell(info.player, '§b[Waypoints]§r含有关键词§d{}§r的路径点有§6{}'.format(point,result))
            server.tell(info.player, '§b[Waypoints]§r你可以使用§b!!wp show <name> §r来展示导航点的相关信息')
    else:
        server.tell(info.player, '§b[Waypoints]§4维度输入错误！请输入§b!!wp§r获取使用方法！')

def dimshow(server,info,dim):
    if int(dim) == 0:
        dimension_name = '§a主世界'
    if int(dim) == 1:
        dimension_name = '§2末地'
    if int(dim) == -1:
        dimension_name = '§c地狱'
    result=[]
    for i in range(0,len(name)):
        if int(dimension[i]) == dim:
            result.append(name[i])
    server.tell(info.player, '§b[Waypoints]§r在维度{}§r里共有导航点§d{}§r个，列表如下：{}'.format(dimension_name,len(result),result))

def on_load(server, old_module):
    refresh_list()

def get_pos(server,info):
    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
    nbt=PlayerInfoAPI.getPlayerInfo(server, info.player)
    return nbt

def on_server_startup(server):
    if os.path.exists(path):
        refresh_list()
    else:
        create_csv(path)


def on_info(server,info):
    if info.content == '!!create':
        create_csv(path)
    if prefix in info.content or prefix_short in info.content:
        message=info.content.split()
        if info.content == prefix or info.content == prefix_short:
            server.tell(info.player, help_msg)
        elif message[0] == prefix or message[0] == prefix_short:
            if message[1] == 'add':
                global complicated
                is_duplicated(message[2])
                if complicated==True:
                    server.tell(info.player, '§b[Waypoints]§4名为{}的路径点已存在！'.format(message[2]))
                    refresh_list()
                    complicated=False
                else:
                    add(server,info,message)
            if message[1] == 'del':
                if len(message) == 2:
                    server.tell(info.player, '§b[Waypoints]§4你必须输入要删除的路径点名字！')
                elif len(message) == 3:
                    delete(server,info,message[2])
                else:
                    server.tell(info.player, '§b[Waypoints]§4输入格式不正确！')
            
            if message[1] == 'reload':
                try:
                    refresh_list()
                    server.say('§b[Waypoints]§a由玩家§d{}§a发起的Waypoints重载成功'.format(info.player))
                except Exception as e:
                    server.say('§b[Waypoints]§4由玩家§d{}§4发起的Waypoints重载失败：{}'.format(info.player,e))

            if message[1] == 'list':
                showlist(server,info)

            if message[1] == 'search':
                if len(message) == 2:
                    server.tell(info.player, '§b[Waypoints]§4请在命令后输入查询的导航点关键词！')
                elif len(message) == 3:
                    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
                    nbt=PlayerInfoAPI.getPlayerInfo(server, info.player)
                    search(server,info,message[2],nbt['Dimension'])
                elif len(message) == 4:
                    search(server,info,message[2],message[3])
                else:
                    server.tell(info.player, '§b[Waypoints]§4输入格式不正确！')
            
            if message[1] == 'show':
                if len(message) == 2:
                    server.tell(info.player, '§b[Waypoints]§4请在命令后输入展示的导航点名称！')
                elif len(message) == 3:
                    showdetail(server,info,message[2])
                else:
                    server.tell(info.player, '§b[Waypoints]§4输入格式不正确！')

            if message[1] == 'dim':
                if len(message) == 2:
                    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
                    nbt=PlayerInfoAPI.getPlayerInfo(server, info.player)
                    dimshow(server,info,nbt['Dimension'])
                if len(message) == 3:
                    dim=int(message[2])
                    if dim == 1 or dim == 0 or dim == -1:
                        dimshow(server,info,dim)
                    else:
                        server.tell(info.player, '§b[Waypoints]§4维度输入错误！请输入§b!!wp§4获取使用信息！')

