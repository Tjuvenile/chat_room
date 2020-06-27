# chat_room

在学习Socket的时候，做了一个chat room练手。  没有做界面美化工作，界面用的是Designer自动生成的pyqt5界面，仿qq聊天窗口框架。
先运行tcp_server.py
再运行tcp_client.py

我没有用数据库来存储账号和密码，而是在/user下为每个用户创建一个"用户名.txt"的文件，里面存的有此用户的密码以及friend。
/user/chat下存储的是用户的聊天记录

![](https://github.com/Tjuvenile/chat_room/raw/master/project_screenshot/file_list.png)

登陆窗口

![](https://github.com/Tjuvenile/chat_room/raw/master/project_screenshot/login.png)

注册窗口

![](https://github.com/Tjuvenile/chat_room/raw/master/project_screenshot/register.png)

登陆进去之后，显示好友列表窗口

![](https://github.com/Tjuvenile/chat_room/raw/master/project_screenshot/friend_list.png)

双击好友列表里的好友，可以进入聊天窗口

![](https://github.com/Tjuvenile/chat_room/raw/master/project_screenshot/chat_window.png)


