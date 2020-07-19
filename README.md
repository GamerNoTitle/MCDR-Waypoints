# MCDR-Waypoints

这是一个服务器内全员共享的Volexmap的标记点插件，需要PlayerInfoAPI支持！

本插件会在`config`文件夹内新建一个名为`Waypoints.csv`的文件用于存放路径点信息

注意，在此插件中，`!!waypoints`可以简写为`!!wp`，下面的使用说明将以`!!wp`为例子

`!!wp`可以显示帮助信息

`!!wp list`列出所有路径点

`!!wp search <content>`搜索名字中含有content的路径点

`!!wp add <name> (x) (y) (z) (Dimension)`添加位置为x,y,z，维度为Dimension的导航点，x,y,z,Dimension非必填，若不填写将获取玩家当前位置和维度，也可以只填写坐标不填写维度

`!!wp del <name>`删除名为name的导航点（需要MCDR.Helper权限及以上，可以在文件最开始关掉）

`!!wp reload`重载路径点列表

赞助：[爱发电](https://afdian.net/@GamerNoTitle)

## 下一步开发内容
- [ ] 自动识别玩家发布的Volexmap路径点信息并记录入数据库 

