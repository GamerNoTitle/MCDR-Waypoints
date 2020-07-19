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
complicated=False
help_msg='''
======== §bWaypoints §r========
本插件中§d!!wp§r与§d!!waypoints§r效果相同，两者可以互相替换
§b!!wp§r显示本帮助信息
§b!!wp list§r显示路径点列表
§b!!wp search <content>§r搜索含有指定内容名字的路径点
§b!!wp add <name> (x) (y) (z) (Dimension) §r添加名为<name>的路径点（x,y,z指定坐标，Dimension为维度，0是主世界，-1是地狱，1是末地，非必须）
§b!!wp del <name>§r删除名为<name>的路径点（需要MCDR.helper以上权限）
§b!!wp reload§r重载插件列表
'''
def refresh_list():
    global name,x,y,z,dimension,complicated
    database=csv.reader(path)
    name=[]
    x=[]
    y=[]
    z=[]
    dimension=[]
    file=open(path,'r',encoding='utf8')
    database=csv.reader(file)
    for i in database:
        name.append(i[0])
        x.append(i[1])
        y.append(i[2])
        z.append(i[3])
        dimension.append(i[4])
    print(name,x,y,z,dimension)
    complicated==False
refresh_list()
def create_csv(path):
    with open(path,"w+",newline="",encoding="gbk") as file:
        csv_file = csv.writer(file)
        csv_file.writerow('')

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
        print(pos)
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
        Dimension=message[6]
        if type(Dimension) == 'int':
            if Dimension>1 or Dimension<-1:
                server.tell(info.player,'§b[Waypoints]§4你必须输入介于-1到1之间的整数！')
            else:
                data=[message[2],x,y,z,Dimension]
                append_csv(path,data)
                refresh_list()
                server.tell(info.player, '§b[Waypoints]§r导航点[name: {}, x: {}, y: {}, z: {}, dim: {}]已添加！'.format(message[2],x,y,z,Dimension))
        else:
            server.tell(info.player,'§b[Waypoints]§4你必须输入整数！')
    else:
        server.tell(info.player, '§b[Waypoints]§4输入格式不正确！')    

def is_duplicated(point):
    i=0
    for i in range(len(name)):
        print(point,name[i])
        if point==name[i]:
            global complicated
            complicated=True

def delete(server,info,point):
    None
def points_list(server,info):
    None
def search(server,info,point):
    None
def get_pos(server,info):
    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
    nbt=PlayerInfoAPI.getPlayerInfo(server, info.player)
    return nbt

def on_server_startup(server):
    if os.path.exists(path):
        refresh_list()
    else:
        create_csv(path)
        refresh_list()

def on_info(server,info):
    if prefix in info.content or prefix_short in info.content:
        message=info.content.split()
        if info.content == prefix or info.content == prefix_short:
            server.tell(info.player, help_msg)
        elif message[0] == prefix or message[0] == prefix_short:
            if message[1] == 'add':
                global complicated
                is_duplicated(message[2])
                print(complicated)
                if complicated==True:
                    server.tell(info.player, '§b[Waypoints]§4名为{}的路径点已存在！'.format(message[2]))
                    refresh_list()
                    complicated=False
                else:
                    add(server,info,message)
            if message[1] == 'remove':
                None
            
            if message[1] == 'reload':
                try:
                    refresh_list()
                    server.say('§b[Waypoints]§a由玩家§d{}§a发起的Waypoints重载成功'.format(info.player))
                except Exception as e:
                    server.say('§b[Waypoints]§4由玩家§d{}§4发起的Waypoints重载失败：{}'.format(info.player,e))