# MCDR-Waypoints

这是一个服务器内全员共享的Volexmap的标记点插件，需要PlayerInfoAPI支持！

注意，在此插件中，`!!waypoints`可以简写为`!!wp`，下面的使用说明将以`!!wp`为例子

`!!wp`可以显示帮助信息

`!!wp list`列出所有路径点

`!!wp search <content>`搜索名字中含有content的路径点

`!!wp add <name> (x) (y) (z) (Dimension)`添加位置为x,y,z，维度为Dimension的导航点，x,y,z,Dimension非必填，若不填写将获取玩家当前位置和维度，也可以只填写坐标不填写维度

`!!wp del <name>`删除名为name的导航点（需要MCDR.Helper权限及以上）

`!!wp reload`重载路径点列表

## 开发进程

- [x] 帮助信息显示
- [x] 路径点列出
- [x] 路径点信息显示
- [x] 搜索路径点
- [x] 添加路径点
- [ ] 删除路径点
- [x] 重载列表