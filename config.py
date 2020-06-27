
import win32api




#get Windows screen size
WINDOWS_SIZE = (win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1))

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

#注册状态码  01
SIGN_UP_STATE = "01"
#登陆状态码  02     020 密码错误  021 账号错误
SIGN_IN_STATE = "02"
#添加好友状态码 03    成功返回03，失败返回030
INSERT_FRIEND_STATE = "03"
#聊天状态码 04  成功返回 04，  失败返回 040
CHAT_STATE = "04"
#删除好友状态码 05 成功返回05 ,  失败返回050
DEL_FRIEND_STATE = "05"

