# -*- coding: utf-8 -*-

'''
@auther : Jacob
@time:2020.2.17
@version: V1.0
@project name: chat room

The py file is Tcp client programme of chat room. can resiger,login,insert and delete friend,
delete group,Besides can chat with your friend or more people chat in group together.
'''

#sys model
import sys
from socket import *

#third party model
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QRegExp, QSize, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QWidget, QListWidgetItem, QLineEdit
from PyQt5.QtGui import QRegExpValidator

#user model
import config

class Chat_Client( QWidget ):
    '''
    Chat client main logic.
    use Tcp connect with server.
    The class parent is Qwidget class. Because We need to create Window,whereas Qwidget is basics of create window.
    '''
    def __init__(self):
        #call parent class init.
        super().__init__()
        #whether is login.
        self.is_sign_up = False
        #Three window init.
        self.frame_init()

    def setupUi(self, MainWindow):
        '''
        login window Pyqt5 data. the function is Qt Desiger Automatic generation
        :param MainWindow: window
        :return:void
        '''
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(752, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(210, 120, 291, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lab_passwd = QtWidgets.QLabel( self.verticalLayoutWidget )
        self.lab_passwd.setAlignment( QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter )
        self.lab_passwd.setObjectName( "label_2" )
        self.gridLayout_2.addWidget( self.lab_passwd, 1, 0, 1, 1 )

        self.user_name = QtWidgets.QLineEdit( self.verticalLayoutWidget )
        self.user_name.setEchoMode( QtWidgets.QLineEdit.Normal )
        self.user_name.setCursorMoveStyle( QtCore.Qt.LogicalMoveStyle )
        self.user_name.setObjectName( "lineEdit" )
        self.gridLayout_2.addWidget( self.user_name, 0, 1, 1, 1 )
        self.password = QtWidgets.QLineEdit( self.verticalLayoutWidget )
        self.password.setEchoMode( QtWidgets.QLineEdit.Normal )
        self.password.setObjectName( "lineEdit_2" )
        self.gridLayout_2.addWidget( self.password, 1, 1, 1, 1 )
        self.chat_user_name = QtWidgets.QLabel( self.verticalLayoutWidget )
        self.chat_user_name.setAlignment( QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter )
        self.chat_user_name.setObjectName( "label" )
        self.gridLayout_2.addWidget( self.chat_user_name, 0, 0, 1, 1 )
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btn_sign_in = QtWidgets.QPushButton( self.verticalLayoutWidget )
        self.btn_sign_in.setObjectName( "pushButton" )
        self.gridLayout.addWidget( self.btn_sign_in, 0, 0, 1, 1 )
        self.btn_sign_up = QtWidgets.QPushButton( self.verticalLayoutWidget )
        self.btn_sign_up.setObjectName( "pushButton_2" )
        self.gridLayout.addWidget( self.btn_sign_up, 0, 1, 1, 1 )
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 752, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi( MainWindow )
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        '''
        login window Pyqt5 data. the function is Qt Desiger Automatic generation.
        Besides the function is used for update the login window data.
        :param MainWindow: window
        :return:void
        '''
        self._translate = QtCore.QCoreApplication.translate
        # set default show text
        MainWindow.setWindowTitle(self._translate("MainWindow", "MainWindow"))
        self.lab_passwd.setText( self._translate( "MainWindow", "password:" ) )
        self.chat_user_name.setText( self._translate( "MainWindow", "user:" ) )
        self.btn_sign_in.setText( self._translate( "MainWindow", "sign in" ) )
        self.btn_sign_up.setText( self._translate( "MainWindow", "sign up" ) )

        #set Placeholder Text. If you don't click the text. It will show.
        self.user_name.setPlaceholderText( "User name" )
        ##set Placeholder Text. If you don't click the text. It will show.
        self.password.setPlaceholderText("Password")

        # set Password edit can't Mouse down right click.
        # (default mouse down right click in the edit will show copy,del function,whereas We not hope show this)
        self.password.setContextMenuPolicy(Qt.NoContextMenu)
        # set the password show text mode is not visible.
        self.password.setEchoMode(QLineEdit.Password)

        # Create a 正则表达式，可以把这个正则表达式安在控件上，加正则匹配，只有匹配成立，才能输入进去。
        # 这个正则表达式只接收数字，也就是设置账户只能输入纯数字
        regx_user = QRegExp("^[0-9]*$")
        validator_user = QRegExpValidator(regx_user,self.user_name)
        self.user_name.setValidator(validator_user)

        # the same as above，密码必须以字母开头，且只包含数字和字母，长度最长为15位
        regx_passwd = QRegExp("^[0-9A-Za-z]{24}$")
        validator_passwd = QRegExpValidator(regx_passwd,self.password)
        self.password.setValidator(validator_passwd)

        # set sign in button click event.
        self.btn_sign_in.clicked.connect(self.sign_in)
        # set sign up button click event.
        self.btn_sign_up.clicked.connect(self.update_login_frame)
        # set input number max length is 12 of user edit.
        self.user_name.setMaxLength(12)

    def setupUi_login(self, MainWindow):
        '''
        The same as above. The function is login window.
        '''
        MainWindow.setObjectName( "MainWindow" )
        MainWindow.resize( 373, 962 )
        MainWindow.setMaximumSize( QtCore.QSize( 16777215, 16777215 ) )
        self.centralwidget = QtWidgets.QWidget( MainWindow )
        self.centralwidget.setObjectName( "centralwidget" )
        self.verticalLayoutWidget = QtWidgets.QWidget( self.centralwidget )
        self.verticalLayoutWidget.setGeometry( QtCore.QRect( 0, 0, 371, 951 ) )
        self.verticalLayoutWidget.setObjectName( "verticalLayoutWidget" )
        self.verticalLayout = QtWidgets.QVBoxLayout( self.verticalLayoutWidget )
        self.verticalLayout.setContentsMargins( 0, 0, 0, 0 )
        self.verticalLayout.setObjectName( "verticalLayout" )
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName( "horizontalLayout" )
        self.lab_friend = QtWidgets.QLabel( self.verticalLayoutWidget )
        self.lab_friend.setContextMenuPolicy( QtCore.Qt.NoContextMenu )
        self.lab_friend.setLayoutDirection( QtCore.Qt.LeftToRight )
        self.lab_friend.setAlignment( QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter )
        self.lab_friend.setObjectName( "label_2" )
        self.horizontalLayout.addWidget( self.lab_friend )
        self.net_name = QtWidgets.QLabel( self.verticalLayoutWidget )
        self.net_name.setAlignment( QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter )
        self.net_name.setObjectName( "label" )
        self.horizontalLayout.addWidget( self.net_name )
        self.verticalLayout.addLayout( self.horizontalLayout )
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName( "verticalLayout_3" )
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName( "horizontalLayout_2" )
        self.lab_friend_2 = QtWidgets.QLabel( self.verticalLayoutWidget )
        self.lab_friend_2.setText( "" )
        self.lab_friend_2.setObjectName( "label_3" )
        self.horizontalLayout_2.addWidget( self.lab_friend_2 )
        self.btn_insert_friend = QtWidgets.QPushButton( self.verticalLayoutWidget )
        self.btn_insert_friend.setObjectName( "pushButton" )
        self.horizontalLayout_2.addWidget( self.btn_insert_friend )
        self.horizontalLayout_2.setStretch( 0, 2 )
        self.horizontalLayout_2.setStretch( 1, 1 )
        self.verticalLayout_3.addLayout( self.horizontalLayout_2 )
        self.verticalLayout.addLayout( self.verticalLayout_3 )
        self.friend_list = QtWidgets.QListWidget( self.verticalLayoutWidget )
        self.friend_list.setObjectName( "listWidget" )
        self.verticalLayout.addWidget( self.friend_list )
        self.verticalLayout.setStretch( 0, 3 )
        self.verticalLayout.setStretch( 1, 3 )
        self.verticalLayout.setStretch( 2, 60 )
        MainWindow.setCentralWidget( self.centralwidget )
        self.menubar = QtWidgets.QMenuBar( MainWindow )
        self.menubar.setGeometry( QtCore.QRect( 0, 0, 373, 26 ) )
        self.menubar.setObjectName( "menubar" )
        MainWindow.setMenuBar( self.menubar )
        self.statusbar = QtWidgets.QStatusBar( MainWindow )
        self.statusbar.setObjectName( "statusbar" )
        MainWindow.setStatusBar( self.statusbar )

        self.retranslateUi_login( MainWindow )
        QtCore.QMetaObject.connectSlotsByName( MainWindow )

    def retranslateUi_login(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle( _translate( "MainWindow", "MainWindow" ) )
        self.lab_friend.setText( _translate( "MainWindow", "user id:" ) )
        self.net_name.setText( _translate( "MainWindow", "label" ) )
        self.btn_insert_friend.setText( _translate( "MainWindow", "insert" ) )
        #set frame coordinate.
        # self.friend_list_frame.move( config.WINDOWS_SIZE[0], 50 )

        #bind event. click insert friend button.
        self.btn_insert_friend.clicked.connect(self.insert_friend)

        #bind event. double click friend list(list widget) item.
        self.friend_list.doubleClicked.connect( self.double_cliecked )

    def setupUi_chat(self, MainWindow):
        '''
        The same as above. The function is chat window.
        '''
        MainWindow.setObjectName( "MainWindow" )
        MainWindow.resize( 1052, 880 )
        self.centralwidget = QtWidgets.QWidget( MainWindow )
        self.centralwidget.setObjectName( "centralwidget" )
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget( self.centralwidget )
        self.horizontalLayoutWidget_2.setGeometry( QtCore.QRect( 60, 30, 901, 741 ) )
        self.horizontalLayoutWidget_2.setObjectName( "horizontalLayoutWidget_2" )
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout( self.horizontalLayoutWidget_2 )
        self.horizontalLayout_2.setContentsMargins( 0, 0, 0, 0 )
        self.horizontalLayout_2.setObjectName( "horizontalLayout_2" )
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName( "verticalLayout_4" )
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName( "verticalLayout_2" )
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins( -1, 0, -1, 11 )
        self.gridLayout.setObjectName( "gridLayout" )
        self.btn_del_friend = QtWidgets.QPushButton( self.horizontalLayoutWidget_2 )
        self.btn_del_friend.setObjectName( "pushButton" )
        self.gridLayout.addWidget( self.btn_del_friend, 1, 2, 1, 1 )
        self.label_5 = QtWidgets.QLabel( self.horizontalLayoutWidget_2 )
        self.label_5.setText( "" )
        self.label_5.setObjectName( "label_5" )
        self.gridLayout.addWidget( self.label_5, 0, 2, 1, 1 )
        self.label_7 = QtWidgets.QLabel( self.horizontalLayoutWidget_2 )
        self.label_7.setText( "" )
        self.label_7.setObjectName( "label_7" )
        self.gridLayout.addWidget( self.label_7, 1, 1, 1, 1 )
        self.label_8 = QtWidgets.QLabel( self.horizontalLayoutWidget_2 )
        self.label_8.setText( "" )
        self.label_8.setObjectName( "label_8" )
        self.gridLayout.addWidget( self.label_8, 1, 0, 1, 1 )
        self.lab_friend = QtWidgets.QLabel( self.horizontalLayoutWidget_2 )
        self.lab_friend.setObjectName( "label_2" )
        self.gridLayout.addWidget( self.lab_friend, 0, 0, 1, 1 )
        self.verticalLayout_2.addLayout( self.gridLayout )
        self.print_edit = QtWidgets.QTextBrowser( self.horizontalLayoutWidget_2 )
        self.print_edit.setObjectName( "textBrowser" )
        self.verticalLayout_2.addWidget( self.print_edit )
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName( "horizontalLayout" )
        self.label = QtWidgets.QLabel( self.horizontalLayoutWidget_2 )
        self.label.setText( "" )
        self.label.setObjectName( "label" )
        self.horizontalLayout.addWidget( self.label )
        self.verticalLayout_2.addLayout( self.horizontalLayout )
        self.input_edit = QtWidgets.QTextEdit( self.horizontalLayoutWidget_2 )
        self.input_edit.setObjectName( "textEdit" )
        self.verticalLayout_2.addWidget( self.input_edit )
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName( "horizontalLayout_4" )
        self.label_9 = QtWidgets.QLabel( self.horizontalLayoutWidget_2 )
        self.label_9.setText( "" )
        self.label_9.setObjectName( "label_9" )
        self.horizontalLayout_4.addWidget( self.label_9 )
        self.btn_send = QtWidgets.QPushButton( self.horizontalLayoutWidget_2 )
        self.btn_send.setObjectName( "pushButton_2" )
        self.horizontalLayout_4.addWidget( self.btn_send )
        self.horizontalLayout_4.setStretch( 0, 4 )
        self.horizontalLayout_4.setStretch( 1, 1 )
        self.verticalLayout_2.addLayout( self.horizontalLayout_4 )
        self.verticalLayout_2.setStretch( 0, 2 )
        self.verticalLayout_2.setStretch( 1, 11 )
        self.verticalLayout_4.addLayout( self.verticalLayout_2 )
        self.horizontalLayout_2.addLayout( self.verticalLayout_4 )
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName( "verticalLayout_3" )
        self.lab_friend_2 = QtWidgets.QLabel( self.horizontalLayoutWidget_2 )
        self.lab_friend_2.setAlignment( QtCore.Qt.AlignCenter )
        self.lab_friend_2.setObjectName( "label_3" )
        self.verticalLayout_3.addWidget( self.lab_friend_2 )
        self.label_10 = QtWidgets.QLabel( self.horizontalLayoutWidget_2 )
        self.label_10.setText( "" )
        self.label_10.setObjectName( "label_10" )
        self.verticalLayout_3.addWidget( self.label_10 )
        self.chat_user_name = QtWidgets.QLabel( self.horizontalLayoutWidget_2 )
        self.chat_user_name.setAlignment( QtCore.Qt.AlignCenter )
        self.chat_user_name.setObjectName( "label_4" )
        self.verticalLayout_3.addWidget( self.chat_user_name )
        self.horizontalLayout_2.addLayout( self.verticalLayout_3 )
        MainWindow.setCentralWidget( self.centralwidget )
        self.menubar = QtWidgets.QMenuBar( MainWindow )
        self.menubar.setGeometry( QtCore.QRect( 0, 0, 1052, 26 ) )
        self.menubar.setObjectName( "menubar" )
        MainWindow.setMenuBar( self.menubar )
        self.statusbar = QtWidgets.QStatusBar( MainWindow )
        self.statusbar.setObjectName( "statusbar" )
        MainWindow.setStatusBar( self.statusbar )

        self.retranslateUi_chat( MainWindow )
        QtCore.QMetaObject.connectSlotsByName( MainWindow )

    def retranslateUi_chat(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle( _translate( "MainWindow", "MainWindow" ) )
        self.btn_del_friend.setText( _translate( "MainWindow", "delete friend" ) )
        self.lab_friend.setText( _translate( "MainWindow", "对方用户名" ) )
        self.btn_send.setText( _translate( "MainWindow", "发送" ) )
        self.lab_friend_2.setText( _translate( "MainWindow", "对方用户名" ) )
        self.chat_user_name.setText( _translate( "MainWindow", "自己" ) )

        # bind event. click delete friend button.
        self.btn_del_friend.clicked.connect( self.del_friend )
        # bind event. click send button.
        self.btn_send.clicked.connect(self.clicked_send)
        # set text browser move end. 也就是让这个多行文本框的滑轮一直在最下边
        self.print_edit.moveCursor(self.print_edit.textCursor().End)

        # set timer event.  2s run the update_text.
        self.timer = QTimer()
        self.timer.start(2000)
        self.timer.timeout.connect(self.update_text)

    def frame_init(self):
        '''
        create three window,login and friend_list and chat frame.
        set login frame visible is True. other frame set False.
        '''

        #create and show login window.
        self.login_frame = QMainWindow()
        self.setupUi( self.login_frame )
        self.login_frame.show()

        #create and show friend list window.
        self.friend_list_frame = QMainWindow()
        self.setupUi_login( self.friend_list_frame )
        self.friend_list_frame.show()

        # create and show chat window.
        self.chat_frame = QMainWindow()
        self.setupUi_chat(self.chat_frame)
        self.chat_frame.show()

        #set friend list window and chat window visible is False. because the user is not login.Can't show.
        self.friend_list_frame.setVisible( False )
        self.chat_frame.setVisible(False)

        sys.exit( app.exec_() )

    def sign_in(self):
        '''
        Login button event function.
        :return:void
        '''
        if not self.is_sign_up:  # 如果是登陆的情况
            # 在文件夹中找有没有跟这个账号一样的文件，然后再进入这个文件找对应的password，是否相同，如果相同，就说明登陆成功
            if self.user_name.text().__len__() >= 8 and self.password.text().__len__() >= 8:
                # 创建一个txt文件，名字为账号，第一行为User: 账号 第二行为 Password:密码   第三行是Friend一个列表
                self.send_message( (config.SIGN_IN_STATE + ",", self.user_name.text() + ",", self.password.text()) )
                print("sessu")
        # else explain This is sign up.
        else:
            # 账号在8-12
            # 密码在8 -25
            if self.user_name.text().__len__() >= 8 and self.password.text().__len__() >= 8:
                # send a state number,user name,password.
                self.send_message( (config.SIGN_UP_STATE + ",", self.user_name.text() + ",", self.password.text()) )

    def update_login_frame(self):
        '''
        当你点击注册按钮的时候，负责整个frame的重新绘制，改变为注册界面。 再点一下，变成登陆界面。
        We can know the frame state now through the is_sign_uo variable.
        :return: void
        '''
        # 如果点的时候，按钮的状态为登陆，就切换为注册按钮
        if not self.is_sign_up:
            self.btn_sign_up.setText( self._translate( "MainWindow", "go back" ) )
            self.btn_sign_in.setText( self._translate( "MainWindow", "sign up" ) )

            # 设置当你不选中的时候的文本   账号只能有数字，账号是8-12位
            self.user_name.setPlaceholderText( "账号8-12位，只能有数字" )
            # 密码8-25位，只能有数字和字母，必须以字母开头
            self.password.setPlaceholderText( "密码8-25位，只能有数字和字母，必须以字母开头" )

            self.password.clear()
            self.user_name.clear()

            self.is_sign_up = True
        else:
            self.btn_sign_up.setText( self._translate( "MainWindow", "sign up" ) )
            self.btn_sign_in.setText( self._translate( "MainWindow", "sign in" ) )

            # 设置当你不选中的时候的文本   账号只能有数字
            self.user_name.setPlaceholderText( "User name" )
            # 密码6-15位，只能有数字和字母，必须以字母开头
            self.password.setPlaceholderText( "Password" )

            self.password.clear()
            self.user_name.clear()
            self.is_sign_up = False

    def send_message(self,data):
        '''
        The function is send message to server.
        :param data:send to server data.
        :return: return server receive data.
        '''

        # Create socket.  AF_INET is use ipv4 agreement. choose SOCK_STREAM because use tcp agreement.
        self.tcp_client_socket = socket( AF_INET, SOCK_STREAM )
        # connect server.The server ip and port is constant,storage in config.
        self.tcp_client_socket.connect( (config.SERVER_IP, config.SERVER_PORT) )

        # 数据传过来是一个列表，我们可以通过这个列表的第一个元素来判断client是要做什么事情。因为做的事情不同，可能发送的格式也不同
        # 如果是01,或者是02,，就说明是登陆或者注册。因为它们的格式相同，所以我就在一起判断了。
        if data[0] == "01," or data[0] == "02,":
            # 解包裹。   如果你传过来的是 ["01,","12345678,","123456789,"].
            # 解包裹就是 state = "01," user_name = "12345678," password = "123456789,"
            # 为什么需要在字符串后面加个","呢？ 因为你连着发送的数据，再服务器那里会堆砌起来，比如你先send "123"
            # 然后send "456" ，服务器那里接收的就是123456. 你就不知道边界在哪，所以用逗号隔开，分清每一部分。
            # Besides, If you use windows os. You should encode named "gbk".
            # whereas if you use linux os. You should encode named "utf-8".
            # Because windows os send and receive data is "gbk".

            state,user_name,password = data
            self.tcp_client_socket.send(state.encode("gbk"))
            self.tcp_client_socket.send(user_name.encode("gbk"))
            self.tcp_client_socket.send(password.encode(("gbk")))
        elif data[0] == "03,":
            state,friend_name,user_name = data
            self.tcp_client_socket.send( state.encode( "gbk" ) )
            self.tcp_client_socket.send( friend_name.encode( "gbk" ) )
            self.tcp_client_socket.send( user_name.encode( "gbk" ) )
        elif data[0] == "04,":
            state,user_name,mesg,friend_name = data
            self.tcp_client_socket.send( state.encode( "gbk" ) )
            self.tcp_client_socket.send( user_name.encode( "gbk" ) )
            self.tcp_client_socket.send( mesg.encode( "gbk" ) )
            self.tcp_client_socket.send( friend_name.encode( "gbk" ) )
        elif data[0] == "05,":
            state,user_name,friend_name = data
            self.tcp_client_socket.send( state.encode( "gbk" ) )
            self.tcp_client_socket.send( user_name.encode( "gbk" ) )
            self.tcp_client_socket.send( friend_name.encode( "gbk" ) )

        # waiting for server receive data. Besides The data max size is 10240B.
        recv_data = self.tcp_client_socket.recv(10240)
        # decode the server receive data.
        recv_data = recv_data.decode("gbk")

        # 通过判断返回回来的数据的前三位来判断是否是成功的。
        # If resiger is success,clear the edit text.
        if recv_data[0:3] == "01,":
            self.user_name.clear()
            self.password.clear()
            print("注册成功")
        elif recv_data[0:3] == "02,":
            # receive 02, It show login is success. We need show friend list frame.
            self.friend_list_frame.setVisible(True)
            self.login_frame.setVisible(False)
            # set friend list label is login user name edit text.
            self.net_name.setText( self.user_name.text() )
            # 登陆上去的时候，需要检查一下好友列表，然后更新一下。
            self.update_friend_list(recv_data[3:recv_data.__len__()])
        elif recv_data[0:3] == "030" or recv_data[0:3] == "03,":
            # insert friend. If insert success. update friend list.
            if recv_data[0:3] == "030":
                print("已经添加过了")
            else:
                self.update_friend_list( recv_data[3:recv_data.__len__()] )
                print("添加成功")
        # delete friend. If delete friend is success. update friend list.
        elif recv_data[0:3] == "05,":
            self.update_friend_list( recv_data[3:recv_data.__len__()] )
            self.chat_frame.setVisible(False)

        # After the client send and receive,close the socket.
        self.tcp_client_socket.close()
        # return receive data.
        return recv_data

    def update_text(self):
        '''
        update chat text.  and update friend list.
        也就是要解决一个问题，当你发送给对方聊天的时候，怎么让对方显示你的聊天。
        我的方法就是定时2s看看聊天记录有没有变化，如果有变化的话，就刷新，这样就实现了
        用户之间聊天的显示问题。   用户好友列表的刷新也是这个原理，一直去检测用户的好友列表有没有
        变化，如果有变化，就更新好友列表。
        这里么有两个大坑：
        多线程无法跨线程调用GUI资源，而GUI资源是有它本身的线程的，如果你要循环做某些事情
        要么要GUI自己集成的Qtimer事件，来定时触发某个函数。  或者使用GUI自己的QThread来做多线程操作。
        （GUI编程没法使用Thread多线程）
        :return:
        '''
        if self.chat_user_name.text() != "自己":
            # send a empty data. 我在服务器设定发送空的数据会返回你和对方的聊天记录。
            # 然后一直把返回的数据显示在print_edit控件，就实现了聊天记录的刷新
            recv_data = self.send_message(
                (config.CHAT_STATE + ",", self.net_name.text() + ",", "" + ",", self.lab_friend_2.text()) )
            if recv_data != "040":
                self.print_edit.clear()
                self.print_edit.append( recv_data )
            else:
                self.print_edit.clear()
            print( "刷新" + recv_data )
        # update user friend list.
        # if net_name.text() == label. 说明是你还没登陆，如果登陆的话net name就会变成你的账号，所以不更新。
        if self.net_name.text() != "label":
            self.send_message( (config.SIGN_IN_STATE + ",", self.user_name.text() + ",", self.password.text()) )

    def double_cliecked(self, item):
        '''
        double click item event.
        这个函数的思想就是当你双击好友列表的某一项的时候，就跳到对应好友的聊天窗体上。
        那么你就需要在弹出窗体的时候，刷新一下你和好友的聊天记录。而好友的聊天机制和群的聊天机制是不一样的。
        我就通过点击的时候，判断你点击的那一项的名字长度来判断它是用户还是群，如果是群就按照群的设定去做，否则按用户去做。
        :param item: listwidget item. 点击的是listwidget哪一项.
        :return:void
        '''

        # set chat frame visible is true.
        self.chat_frame.setVisible(True)
        # get item text. If the text length >= 19. Explain This is a friend,not a group.
        # Because I provide friend number length is 8 - 12. add "friend :" length 11. Explain friend number min length is 19.
        if str(item.data()).__len__() >= 19:
            self.lab_friend.setText(str(item.data()))
            self.lab_friend_2.setText(str(item.data())[11:])
            self.chat_user_name.setText(self.net_name.text())
        # else is group.  I provide group number length is 4 - 7.So it's cant >= 19.
        else:
            self.lab_friend.setText( str( item.data() ) )
            self.lab_friend_2.setText( str( item.data() )[10:] )
            self.chat_user_name.setText( self.net_name.text() )

        #update chat text.
        recv_data = self.send_message(
            (config.CHAT_STATE + ",", self.net_name.text() + ",", "" + ",", self.lab_friend_2.text()) )

        if recv_data != "040":
            self.input_edit.clear()
            self.print_edit.clear()
            self.print_edit.append( recv_data )
        else:
            self.input_edit.clear()
            self.print_edit.clear()

    def clicked_send(self):
        '''
        If clieck send button.send text to server. Then update edit text.
        :return:
        '''
        recv_data = self.send_message((config.CHAT_STATE + "," ,self.net_name.text() + "," , str(self.input_edit.toPlainText()) + "," , self.lab_friend_2.text()))
        if recv_data != "040":
            self.input_edit.clear()
            self.print_edit.clear()
            self.print_edit.append(recv_data)
        else:
            self.input_edit.clear()
            self.print_edit.clear()

    def del_friend(self):
        '''
        click delete friend button event.
        :return:void
        '''
        self.send_message((config.DEL_FRIEND_STATE + "," , self.net_name.text() + "," , self.lab_friend_2.text()))
        self.chat_user_name.setText("自己")

    def insert_friend(self):
        '''
        When we click the insert button. Will 弹出一个框，让你输入值。 然后获取这个值，如果合法，就发送给服务器
        判断是否可以添加好友
        :return:
        '''
        # text storage you input text. ok storage whether you click ok.
        text,ok = QInputDialog.getText(self,'Insert friend','Please input user number')

        if ok:
            # isdigit == True. explain you input type is number.
            if text.isdigit():
                if text.__len__() >= 4 and text.__len__() <= 12:
                    # if not insert self.
                    if text != self.user_name.text():
                        self.send_message((config.INSERT_FRIEND_STATE + ",",text + ",",self.net_name.text()))

    def update_friend_list(self, friend):
        '''
        update friend list.  传过来一个friend list。 如果和当前的列表相同就不清零listwidget.
        如果发现发过来的friend的数量和当前显示的数量不同，就把当前的listwidget清零，然后重新添加。
        :param friend: friend list
        :return: void.
        '''
        friend = friend.split( "," )

        i = 0
        j = 0
        if friend[0].__len__() > 0:
            if self.friend_list.count() != friend.__len__():
                self.friend_list.clear()
                if friend.__len__() != self.friend_list.__len__():
                    for friend in friend:
                        item = QListWidgetItem()
                        item.setSizeHint(QSize(10,100))
                        if friend.__len__() >= 8 :
                            i += 1
                            item.setText("friend " + str(i) + ":  " + friend)
                        else:
                            # else is group.
                            j += 1
                            item.setText("group " + str(j) + ":  " + friend)
                        self.friend_list.addItem(item)
                    # sort listwidget item.  order = 1 or = 0. 对应升序或者降序（我分不清）
                    self.friend_list.sortItems(order = 1)

if __name__ == '__main__':
    # 因为这个需要在Gui编程之前运行，因为上面那个类继承Qwidget，所以也不能写在init里。只能写在这里。
    app = QApplication( sys.argv )
    Chat_Client()
