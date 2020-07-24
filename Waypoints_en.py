# -*- coding: utf-8 -*-
import json as js
import re
import csv
import os
from imp import load_source
PlayerInfoAPI = load_source('PlayerInfoAPI','./plugins/PlayerInfoAPI.py')
path='./config/Waypoints.csv'   # Waypoints File
permission_check=True   # Permission Check: True/False
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
§6Thanks for using the plugin by @GamerNoTitle
§6You can search MCDR-Waypoints on Github to find the repo
The Command §d!!wp§r and §d!!waypoints§r take the same effect in this plugin
§b!!wp§r Show the help message
§b!!wp list§r Show the list of all the waypoints
§b!!wp search <content>§r Search the waypoints that contains the content
§b!!wp show <content>§r Display the waypoint's detail of the content
§b!!wp dim <dim>§r Display all the waypoints of a dimension (0/-1/1/all stands for overworld/nether/end/all)
§b!!wp add <name> (x) (y) (z) (Dimension) §rAdd a waypoints with the <name> (You can add the x,y,z,dimension insteads of using your current position and dimension, 0/-1/1 stands for overworld/nether/end)
§b!!wp del <name>§r Delete the waypoint with the name you input (If the permission check enabled, you need at lease MCDR.helper permission)
§b!!wp reload§r Reload the plugin list
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

def change_dim(dim):
    dimlist={
        "minecraft:overworld": 0,
        "minecraft:the_nether": -1,
        "minecraft:end": 1
    }
    try:
        changed_dim=dimlist[str(dim)]
    except:
        change_dim=0
    return changed_dim

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
        server.tell(info.player, '§b[Waypoints]§4You must input the name of the waypoint!')
    elif len(message) == 3:
        pos,Dimension=get_pos(server,info)
        if type(Dimension) != 'int':
            Dimension=change_dim(Dimension)
        x=int(list(pos)[0])
        y=int(list(pos)[1])
        z=int(list(pos)[2])
        data=[str(message[2]),str(x),str(y),str(z),str(Dimension)]
        append_csv(path,data)
        refresh_list()
        server.tell(info.player, '§b[Waypoints]§rWaypoint [name: {}, x: {}, y: {}, z: {}, dim: {}] has been added.'.format(message[2],x,y,z,Dimension))
    elif len(message) == 6:
        x=message[3]
        y=message[4]
        z=message[5]
        pos,Dimension=get_pos(server,info)
        if type(Dimension) != 'int':
            Dimension=change_dim(Dimension)
        data=[message[2],x,y,z,Dimension]
        append_csv(path,data)
        refresh_list()
        server.tell(info.player, '§b[Waypoints]§rWaypoint [name: {}, x: {}, y: {}, z: {}, dim: {}] has been added.'.format(message[2],x,y,z,Dimension))
    elif len(message) == 7:
        x=message[3]
        y=message[4]
        z=message[5]
        try:
            Dimension=int(message[6])
            if Dimension>1 or Dimension<-1:
                server.tell(info.player,'§b[Waypoints]§4 You must input a integer between -1 to 1!')
            else:
                data=[message[2],x,y,z,Dimension]
                append_csv(path,data)
                refresh_list()
                server.tell(info.player, '§b[Waypoints]§rWaypoint [name: {}, x: {}, y: {}, z: {}, dim: {}] has been added.'.format(message[2],x,y,z,Dimension))
        except:
            server.tell(info.player,'§b[Waypoints]§4You must input a integer!')
    else:
        server.tell(info.player, '§b[Waypoints]§4The format you input is wrong!')    

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
        server.tell(info.player, '§b[Waypoints]§4Cannot find a waypoint with name §d{}§4'.format(point))
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
        server.tell(info.player, '§b[Waypoints]§rThe waypoint §d{}§r has been deleted successfully!'.format(point))


def showdetail(server,info,point):
    is_exist=False
    for i in range(0,len(name)):
        if point == name[i]:
            is_exist=True
            detail='[name: {}, x: {}, y: {}, z: {}, dim: {}]'.format(point,x[i],y[i],z[i],dimension[i])
    if is_exist:
        server.tell(info.player, '§b[Waypoints]§rThe detail of the waypoint §d{}§ris: {}'.format(point,detail))
        is_exist=False
    else:
        server.tell(info.player, '§b[Waypoints]§4Cannot find a waypoint with name §d{}§4!'.format(point))

def showlist(server,info):
    if len(name) == 0:
        server.tell(info.player, '§b[Waypoints]§6There\'s nothing in waypoints list')
    else:
        pointlist=''
        for i in range(0,len(name)):
            if i==len(name):
                pointlist=pointlist+name[i]
            else:
                pointlist=pointlist+name[i]+', '
        server.tell(info.player, '§b[Waypoints]§rThe following are the waypoints in database: {}'.format(pointlist))
        server.tell(info.player, '§b[Waypoints]§rYou can use §b!!wp show <name> §rto show the detail of a waypoint.')

def search(server,info,point,dim):
    result=[]
    if dim == 'all':
        for i in range(0,len(name)):
            if str(point) in str(name[i]):
                result.append(name[i])
        if result == []:
            server.tell(info.player, '§b[Waypoints]§4Cannot find a waypoint with content §d{}§4!'.format(point))
        else:
            server.tell(info.player, '§b[Waypoints]§rThe following are the waypoints with d{}§r: §6{}'.format(point,result))
            server.tell(info.player, '§b[Waypoints]§rYou can use §b!!wp show <name> §rto show the detail of a waypoint.')
    elif int(dim) == 1 or int(dim) == -1 or int(dim) == 0:
        for i in range(0,len(name)):
            if str(point) in str(name[i]) and int(dimension[i]) == dim:
                result.append(name[i])
        if result == []:
            server.tell(info.player, '§b[Waypoints]§4Cannot find a waypoint with content §d{}§4!'.format(point))
        else:
            server.tell(info.player, '§b[Waypoints]§rThe following are the waypoints with §d{}§r: §6{}'.format(point,result))
            server.tell(info.player, '§b[Waypoints]§rYou can use §b!!wp show <name> §rto show the detail of a waypoint.')
    else:
        server.tell(info.player, '§b[Waypoints]§4Dimension wrong! Please use §b!!wp§r for more information!')

def dimshow(server,info,dim):
    if int(dim) == 0:
        dimension_name = '§aoverworld'
    if int(dim) == 1:
        dimension_name = '§5end'
    if int(dim) == -1:
        dimension_name = '§cnether'
    result=[]
    for i in range(0,len(name)):
        if int(dimension[i]) == dim:
            result.append(name[i])
    server.tell(info.player, '§b[Waypoints]§rThere\'re {0}§r points in §d{1}§r: {}'.format(dimension_name,len(result),result))

def on_load(server, old_module):
    refresh_list()
    server.add_help_message('!!wp', '§bGet the usage of Waypoints')

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
                    server.tell(info.player, '§b[Waypoints]§4The waypoint with name {} has already exists!'.format(message[2]))
                    refresh_list()
                    complicated=False
                else:
                    add(server,info,message)
            if message[1] == 'del':
                if permission_check:
                    if(server.get_permission_level(info)>2):
                        if len(message) == 2:
                            server.tell(info.player, '§b[Waypoints]§4You must input the name of the waypoint you want to delete!')
                        elif len(message) == 3:
                            delete(server,info,message[2])
                        else:
                            server.tell(info.player, '§b[Waypoints]§4Wrong format!')
                    else:
                        server.tell(info.player, '§b[Waypoints]§4Permission Denied!')
                else:
                    if len(message) == 2:
                        server.tell(info.player, '§b[Waypoints]§4You must input the name of the waypoint you want to delete!')
                    elif len(message) == 3:
                        delete(server,info,message[2])
                    else:
                        server.tell(info.player, '§b[Waypoints]§4Wrong format!')

            if message[1] == 'reload':
                try:
                    refresh_list()
                    server.say('§b[Waypoints]§aThe reload operation by §d{}§a has run successfully!'.format(info.player))
                except Exception as e:
                    server.say('§b[Waypoints]§4The reload operation by §d{}§4 has run failed：{}'.format(info.player,e))

            if message[1] == 'list':
                showlist(server,info)

            if message[1] == 'search':
                if len(message) == 2:
                    server.tell(info.player, '§b[Waypoints]§4Please type the content you want to search!')
                elif len(message) == 3:
                    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
                    nbt=PlayerInfoAPI.getPlayerInfo(server, info.player)
                    search(server,info,message[2],nbt['Dimension'])
                elif len(message) == 4:
                    search(server,info,message[2],message[3])
                else:
                    server.tell(info.player, '§b[Waypoints]§4Wrong format!')
            
            if message[1] == 'show':
                if len(message) == 2:
                    server.tell(info.player, '§b[Waypoints]§4Please input the name of the waypoint you want to show!')
                elif len(message) == 3:
                    showdetail(server,info,message[2])
                else:
                    server.tell(info.player, '§b[Waypoints]§4Wrong format!')

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
                        server.tell(info.player, '§b[Waypoints]§4Wrong dimension! Please type §b!!wp§4 for more information!')

