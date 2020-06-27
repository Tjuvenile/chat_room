# -*- coding: utf-8-*-

import os

from socket import *
import threading
import datetime

import config

class TcpServer( object ):
    '''
    The chat Server.
    '''
    def __init__(self):
        # connect user pool. storage alive user.
        self.conn_user_pool = []
        # define root route.
        self.file_path = "./user/"
        self.run()

    def run(self):
        '''
        server main function.
        :return: void
        '''

        # create server socket.
        tcp_server_socket = socket( AF_INET, SOCK_STREAM )
        # bind ip and port. Because server ip and port is changeless. So storage is constant.
        tcp_server_socket.bind( (config.SERVER_IP, config.SERVER_PORT) )
        # set user maximum connect number. Besides set server is listen mode.
        tcp_server_socket.listen( 128 )
        # The function is receive and handle client data.
        self.recv_mesg( tcp_server_socket )

        # Finally close the socket. But this can't
        tcp_server_socket.close()

    def recv_mesg(self, tcp_server_socket):
        '''
        让服务器一直处于 listen mode.  当一个用户连接的时候，就为这个用户创建一个线程。
        :param tcp_server_socket:
        :return:
        '''
        # 一直响应
        while True:
            new_client_socket, client_addr = tcp_server_socket.accept()
            create_user = threading.Thread( target=self.user_handler, args=(new_client_socket,) )
            # 设置为守护线程，即当主线程关闭之后，子线程都会关闭
            create_user.setDaemon( True )
            create_user.start()

    def user_handler(self, new_client_socket):
        '''
        根据客户端发来的状态码，进入对应的逻辑中进行数据处理。
        :param new_client_socket:
        :return:
        '''
        self.user = ''
        # init a lock.
        R = threading.Lock()
        while True:
            # 因为我发现在使用过程中，会出现多个线程争抢资源的情况，加锁就解决了问题。
            R.acquire()
            # receive client data.
            recv_data = new_client_socket.recv( 1024 )
            data = (str( recv_data.decode( "gbk" ) )).split( "," )
            if not recv_data:
                print( "此用户退出" )
                for user in self.conn_user_pool:
                    if self.user == user:
                        self.conn_user_pool.remove( self.user )
                break
            else:
                # Create file.  First line is user number,second is password.
                if data[0] == "01":
                    self.register( data, new_client_socket )
                elif data[0] == "02":
                    self.login( data, new_client_socket )
                elif data[0] == "03":
                    self.insert_friend( data, new_client_socket )
                elif data[0] == "04":
                    self.chat( data, new_client_socket )  # data 为 04，发送方名字，发送数据，好友的名字
                elif data[0] == "05":
                    self.del_friend(data,new_client_socket)
        R.release()
        new_client_socket.close()

    def login(self, data, new_client_socket):
        '''
        login. 先判断能不能找到这个用户的用户名，能找到说明存在这个用户，再找一下这个用户名
        下的password是否和发来的相同，如果相同就可以登录，并且在log文件记录一下登录的用户和时间。否则显示密码错误。
        :param data: login state number，user name，password
        :param new_client_socket: user socket
        :return:
        '''
        file_path = self.file_path

        for file_name in os.listdir( file_path ):
            if file_name == data[1] + '.txt':
                with open( file_path + data[1] + '.txt', "r" ) as f:
                    txt = f.readlines()
                    txt = (txt[1])[9:txt[1].__len__() - 1]

                if data[2] == txt:
                    self.user = data[1]
                    friend = "02," + self.get_friend_list( data[1] )
                    new_client_socket.send( friend.encode( "gbk" ) )
                    self.inert_user_pool( data )
                    # storage login data in log.py
                    with open( 'log.txt', "a" ) as f:
                        f.write( "time:" + str( datetime.datetime.now() ) + "\n" )
                        f.write( "login user:" + data[1] + "\n" )
                        f.write( "user count:" + str( self.conn_user_pool.__len__() ) + "\n" )
                        f.write( "online user list:" )
                        for user in self.conn_user_pool:
                            if user == self.conn_user_pool[self.conn_user_pool.__len__() - 1]:
                                f.write( user )
                            else:
                                f.write( user + "," )
                        f.write( "\n" + "\n" )
                else:
                    new_client_socket.send( "020".encode( "gbk" ) )
                    print( "密码错误" )
                return

        new_client_socket.send( "021".encode( "gbk" ) )
        print( "请先注册" )

    def register(self, data, new_client_socket):
        '''
        遍历一下文件列表名，如果发现有一样的，就说明已经注册过了，直接返回。
        否则就添加这个文件信息，创建一个用户名.txt文件，然后添加三条它的信息
        再创建一个对应的dir文件，用来存储用户对应的数据
        :param data: login state number, user name, password.
        :param new_client_socket:
        :return:
        '''
        filePath = './user/'
        # os.listdir can get the filePath all file. return a list.
        for file_name in os.listdir( filePath ):
            if file_name == data[1] + '.txt':
                print( "已经注册过了" )
                return

        with open( filePath + data[1] + '.txt', "a" ) as f:
            f.write( "user:" + data[1] + "\n" )
            f.write( "password:" + data[2] + "\n" )
            f.write( "friend:" )

        os.mkdir( "./user/chat/" + data[1] )

        new_client_socket.send( "01,".encode( "gbk" ) )

    def inert_user_pool(self, data):
        '''
        will user insert user pool.
        :param data:
        :return:
        '''
        if self.conn_user_pool.__len__() == 0:
            self.conn_user_pool.append( data[1] )
        else:
            for user in self.conn_user_pool:
                if user == data[1]:
                    return

            self.conn_user_pool.append( data[1] )

    def click_friend(self,data, new_client_socket):
        '''
        double click friend. 看有没有对应的聊天文件，如果有救不创建，如果没有创建一个双方的聊天文件。
        chat file 格式是 user_name to friend_name.  如果你不判断一下，就直接读取，但是没有这个文件会报错。
        :param data:
        :param new_client_socket:
        :return:
        '''
        state, user_name, friend_name = data
        is_have_user_file = self.find_file( "./user/chat/" + user_name, user_name + "to" + friend_name + ".txt" )
        is_have_friend_file = self.find_file( "./user/chat/" + friend_name, friend_name + "to" + user_name + ".txt" )

        if not is_have_user_file:
            with open( "./user/chat/" + user_name + "/" + user_name + "to" + friend_name + ".txt", "a" ):
                print( "创建成功" )

        if not is_have_friend_file:
            with open( "./user/chat/" + friend_name + "/" + friend_name + "to" + user_name + ".txt", "a" ):
                print( "创建成功" )

        with open( "./user/chat/" + user_name + "/" + user_name + "to" + friend_name + ".txt", "r" ) as f:
            read = f.read()

        if read != "":
            new_client_socket.send( read.encode( "gbk" ) )
        else:
            new_client_socket.send( "060".encode( "gbk" ) )

    def chat(self, data, new_client_socket):
        '''
        If client send message is empty string. return the user and the friend chat file data.
        else will message insert the user and the friend chat file. Then return chat file now.
        :param data: state number , user name , send message, friend name.
        :param new_client_socket:
        :return:
        '''
        state, user_name, send_mesg, friend_name = data

        if send_mesg == "" :
            # friend_name length >=8,explain this is a user. else is a group.
            if friend_name.__len__() >= 8:
                is_have_user_file = self.find_file( "./user/chat/" + user_name,
                                                    user_name + "to" + friend_name + ".txt" )
                is_have_friend_file = self.find_file( "./user/chat/" + friend_name,
                                                      friend_name + "to" + user_name + ".txt" )

                if not is_have_user_file:
                    with open( "./user/chat/" + user_name + "/" + user_name + "to" + friend_name + ".txt", "a" ):
                        print( "创建成功" )

                if not is_have_friend_file:
                    with open( "./user/chat/" + friend_name + "/" + friend_name + "to" + user_name + ".txt", "a" ):
                        print( "创建成功" )

                # 为空，说明是点击item发送的socket，把不需要添加信息，直接返回user与这个friend的聊天记录即可。
                with open( "./user/chat/" + user_name + "/" + user_name + "to" + friend_name + ".txt",
                           "r" ) as f:
                    read = f.read()
            # about group. Don't need to create user chat file. Only storage chat file in group.
            else:
                # 为空，说明是点击item发送的socket，把不需要添加信息，直接返回user与这个friend的聊天记录即可。
                with open( "./user/chat/" + friend_name +  "/group.txt",
                           "r" ) as f:
                    read = f.read()

            if read != "":
                new_client_socket.send( read.encode( "gbk" ) )
            else:
                new_client_socket.send( "040".encode( "gbk" ) )

        else:
            # if is user. storage message in user chat file and friend chat file.
            # else is group. Only storage message in group chat file.
            if friend_name.__len__() >= 8:
                with open( "./user/chat/" + user_name + "/" + user_name + "to" + friend_name + ".txt", "a" ) as f:
                    f.write(user_name + "  " + str(datetime.datetime.now()) + "\n")
                    f.write( send_mesg + "\n" + "\n" )

                with open( "./user/chat/" + friend_name + "/" + friend_name + "to" + user_name + ".txt", "a" ) as f:
                    f.write(user_name + "  " + str(datetime.datetime.now()) + "\n")
                    f.write( send_mesg + "\n" + "\n" )

                with open( "./user/chat/" + user_name + "/" + user_name + "to" + friend_name + ".txt", "r" ) as f:
                    new_client_socket.send(f.read().encode("gbk"))
                    print("发送信息成功")
            else:
                with open( "./user/chat/" + friend_name + "/group.txt", "a" ) as f:
                    f.write(user_name + "  " + str(datetime.datetime.now()) + "\n")
                    f.write( send_mesg + "\n" + "\n" )

                with open( "./user/chat/" + friend_name + "/group.txt", "r" ) as f:
                    new_client_socket.send(f.read().encode("gbk"))
                    print("发送信息成功")

    def del_friend(self,data,new_client_socket):
        '''
        在双方的文件中删除对应的数据即可
        :param data: delete state number,user, will delete friend
        :param new_client_socket:
        :return:
        '''
        state,user,friend = data
        friend_file = []

        user_friend = self.get_friend_list(user).split(",")
        print(user_friend)
        user_friend.remove(friend)

        with open(self.file_path + user + ".txt" , "r") as f:
            friend_file.append( f.readlines( 1)[0] )
            friend_file.append( f.readlines( 2 )[0] )

        with open(self.file_path + user + ".txt" , "a") as f:
            f.seek(0,0)
            f.truncate()
            f.write(str(friend_file[0]) )
            f.write(str(friend_file[1]))
            f.write("friend:")
            for fred in user_friend:
                f.write( fred + "," )

        user_friend = self.get_friend_list( friend ).split( "," )
        user_friend.remove( user )

        with open(self.file_path + friend + ".txt" , "r") as f:
            friend_file.clear()
            friend_file.append(f.readlines(1)[0])
            friend_file.append(f.readlines( 2 )[0])

        with open(self.file_path + friend + ".txt" , "a") as f:
            f.seek(0,0)
            f.truncate()
            f.write(str(friend_file[0]))
            f.write(str(friend_file[1]))
            f.write("friend:")
            for frid in user_friend:
                f.write(frid + ",")

        # 上面是删除对应的好友信息，下面是删除对应的聊天数据文件
        if os.path.exists(self.file_path + "chat/" + user + "/" + user + "to" + friend + ".txt"):
            os.remove(self.file_path + "chat/" + user + "/" + user + "to" + friend + ".txt")

        if os.path.exists(self.file_path + "chat/" + friend + "/" + friend + "to" + user + ".txt"):
            os.remove(self.file_path + "chat/" + friend + "/" + friend + "to" + user + ".txt")

        friend_list = self.get_friend_list(user)

        new_client_socket.send(("05," + friend_list) .encode("gbk"))

    def insert_friend(self, data, new_client_socket):
        '''
        Open file,insert friend number date in third line.
        :param data: insert state number, user,friend
        :param new_client_socket:
        :return:
        '''
        #state friend_name user_name
        is_find = self.find_file( self.file_path, data[1] + ".txt" )
        if is_find:
            with open( self.file_path + data[1] + '.txt', "r" ) as f:
                txt = f.readlines()
                txt = (txt[2])[7:txt[2].__len__() - 1]
                txt = txt.split( "," )
                for friend in txt:
                    if friend == data[2]:
                        new_client_socket.send( "030".encode( "gbk" ) )
                        return
                with open( self.file_path + data[1] + '.txt', "a" ) as f:
                    f.write( data[2] + "," )
                with open( self.file_path + data[2] + '.txt', "a" ) as f:
                    f.write( data[1] + "," )
                friend = "03," + self.get_friend_list( data[2] )
                new_client_socket.send( friend.encode( "gbk" ) )
        else:
            new_client_socket.send( "030".encode("gbk") )

    def find_file(self, file_path, text):
        '''
        Find file in the route. If find it return True,else return False.
        :param file_path:route
        :param text:File name
        :return:
        '''
        for file in os.listdir( file_path ):
            if file == text:
                return True

        return False

    def get_friend_list(self, user):
        '''
        :param user:user
        :return: the user friend list
        '''
        with open( self.file_path + user + '.txt', "r" ) as f:
            txt = f.readlines()
            txt = (txt[2])[7:txt[2].__len__() - 1]
            return txt

if __name__ == '__main__':
    TcpServer()
