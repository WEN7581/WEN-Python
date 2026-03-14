import sys
import psutil
from scapy.all import conf
def get_interface_guid(interface_name):
    """
    根据用户输入的网卡名称，查找对应的 GUID
    """
    for iface, addrs in psutil.net_if_addrs().items():
        if iface.lower() == interface_name.lower():
            # 查找对应的 GUID（Windows 下为 NPF 设备）
            for guid in conf.ifaces.keys():
                if guid.endswith(iface.replace("{", "").replace("}", "")):
                    return guid
    return None

# 检查是否指定了网卡
if len(sys.argv) >= 4:
    interface = sys.argv[3]
    try:
        # 方法三：使用 psutil 匹配网卡名称并转换为 GUID
        guid = get_interface_guid(interface)
        if guid is None or guid not in conf.ifaces:
            print(f"[-] 错误: 网卡 '{interface}' 不存在或无法识别！")
            print("[*] 可用的网卡列表:")
            for i, (guid, desc) in enumerate(conf.ifaces.items()):
                print(f"  [{i}] {desc} ({guid})")
            sys.exit(1)
        conf.iface = guid
        print(f"[*] 已强制指定网卡为: {interface} ({guid})")
    except Exception as e:
        print(f"[-] 无法设置网卡 {interface}: {e}")
        sys.exit(1)
else:
    print("[*] 未指定网卡，使用 Scapy 默认检测...")