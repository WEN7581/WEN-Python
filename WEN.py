import requests
import os
import time
# 配置部分
# 注意：请替换为真实的视频链接，IP地址通常不是直接的视频文件链接
video_url = ""
audio_url = ""
# 建议将 Cookie 放在配置文件中或环境变量中，不要硬编码在代码里
# 这里仅作示例，请填入你自己的有效 Cookie
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    "Cookie": "UIFID_TEMP=c8c20d54553eadab8c678961c2b0df95555df87bbc6b890988ad105aec15abc082ff6bf35865e35de80f70f75642a493ec009ecc4010c3eb876baa83f3b3baef0ca784f4874e7106a24fd4c755960989; hevc_supported=true; xgplayer_user_id=657190849197; bd_ticket_guard_client_web_domain=2; fpk1=U2FsdGVkX1/L+BeWv0x6Uwl3sf2rzFMuqwdG55nmYNrrkPIO/1gZv0z6ud13VKJteYOIR+FPJroimZelXRTnCg==; fpk2=8369da3c75ccd12bc017791df73a85c8; d_ticket=8c1fa446e111477fe6538c856bd32e97e4441; is_staff_user=false; UIFID=c8c20d54553eadab8c678961c2b0df95555df87bbc6b890988ad105aec15abc082ff6bf35865e35de80f70f75642a4939a96fdcdc5c837d163e846841c6f4b602e1913ed813983758bf55fe0526056b8148232b69966663afc33cd6bd3bfb11911779655eed7408eb56f88c9e94d2cf5d84fdc4f2cbc19d86e4dd8fbb330651dabe262e6fe38f04fbf02a977329421038b599a8178cd0a851eb343a8235210d9; my_rd=2; xgplayer_device_id=94669768064; SearchResultListTypeChangedManually=%221%22; enter_pc_once=1; live_use_vvc=%22false%22; __live_version__=%221.1.3.9904%22; dy_swidth=1920; dy_sheight=1080; is_dash_user=1; n_mh=HzlioHjI5I9wntqCGtTd39Tm1rnlRMsWJKsz04of4C4; uid_tt=01be9accab4bdbe29ed487c7cf1aae72; uid_tt_ss=01be9accab4bdbe29ed487c7cf1aae72; sid_tt=88d1c4c348c7a61a6b76ceedb357f85e; sessionid=88d1c4c348c7a61a6b76ceedb357f85e; sessionid_ss=88d1c4c348c7a61a6b76ceedb357f85e; SEARCH_RESULT_LIST_TYPE=%22multi%22; enter_pc_first_on_day=20251213; theme=%22dark%22; manual_theme=%22dark%22; s_v_web_id=verify_mktcowxd_l0NKVUqV_JisW_4Ws6_AoXa_fk6FRxLIReeg; passport_csrf_token=c427e14bc28e550ea0de0b82d3af94fe; passport_csrf_token_default=c427e14bc28e550ea0de0b82d3af94fe; __druidClientInfo=JTdCJTIyY2xpZW50V2lkdGglMjIlM0E0NzAlMkMlMjJjbGllbnRIZWlnaHQlMjIlM0E4MDIlMkMlMjJ3aWR0aCUyMiUzQTQ3MCUyQyUyMmhlaWdodCUyMiUzQTgwMiUyQyUyMmRldmljZVBpeGVsUmF0aW8lMjIlM0ExJTJDJTIydXNlckFnZW50JTIyJTNBJTIyTW96aWxsYSUyRjUuMCUyMChXaW5kb3dzJTIwTlQlMjAxMC4wJTNCJTIwV2luNjQlM0IlMjB4NjQpJTIwQXBwbGVXZWJLaXQlMkY1MzcuMzYlMjAoS0hUTUwlMkMlMjBsaWtlJTIwR2Vja28pJTIwQ2hyb21lJTJGMTQ1LjAuMC4wJTIwU2FmYXJpJTJGNTM3LjM2JTIwRWRnJTJGMTQ1LjAuMC4wJTIyJTdE; download_guide=%223%2F20260217%2F0%22; vdg_s=1; publish_badge_show_info=%220%2C0%2C0%2C1771845143979%22; EnhanceDownloadGuide=%220_0_2_1771925547_0_0%22; passport_assist_user=Cj3DLNdXPuiTx6F5G8Lvc-EMb5WX-47ORTA4eFmtlhUwOupxnxRbvmg1slwrw-6UDnGuRI6t4Z4RBrs-pFj1GkoKPAAAAAAAAAAAAABQHQtmdJa2f8luoWtKvw8wRSjKzXlG09eHjDH2yjGDQTWqKOGsqwFxz1NCVG5ewNZcXRDGx4oOGImv1lQgASIBA1vhNbw%3D; sid_guard=88d1c4c348c7a61a6b76ceedb357f85e%7C1772005243%7C5184000%7CSun%2C+26-Apr-2026+07%3A40%3A43+GMT; session_tlb_tag=sttt%7C20%7CiNHEw0jHphprds7ts1f4Xv_________KkfiqRnhbGsMYkLOGwmvpu-HWFLcoEmysiE_vx0wuTm4%3D; sid_ucp_v1=1.0.0-KGE3Y2ExNjkwNTllNWRmMDk1MDk3ZGY3MGRkOGUwYWUxY2Y1NmRlMDQKHwjJ05aflwMQ-876zAYY7zEgDDC70IzhBTgFQPsHSAQaAmxxIiA4OGQxYzRjMzQ4YzdhNjFhNmI3NmNlZWRiMzU3Zjg1ZQ; ssid_ucp_v1=1.0.0-KGE3Y2ExNjkwNTllNWRmMDk1MDk3ZGY3MGRkOGUwYWUxY2Y1NmRlMDQKHwjJ05aflwMQ-876zAYY7zEgDDC70IzhBTgFQPsHSAQaAmxxIiA4OGQxYzRjMzQ4YzdhNjFhNmI3NmNlZWRiMzU3Zjg1ZQ; login_time=1772005244317; _bd_ticket_crypt_cookie=9e3e2ae4d4386ef48b58fd750284c602; SelfTabRedDotControl=%5B%7B%22id%22%3A%227544972578880751651%22%2C%22u%22%3A52%2C%22c%22%3A0%7D%2C%7B%22id%22%3A%227553804049070442506%22%2C%22u%22%3A16%2C%22c%22%3A0%7D%5D; shareRecommendGuideTagCount=2; __security_mc_1_s_sdk_crypt_sdk=d9f55786-46b1-b881; __security_mc_1_s_sdk_cert_key=b5de0c17-4e34-9a5c; __security_mc_1_s_sdk_sign_data_key_web_protect=694323d6-4944-bbc8; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAIC7ctjT5I2bELwn_OiFTSR8ZCtfUnXqZm-i6lc149WE%2F1772121600000%2F0%2F1772109849038%2F0%22; douyin.com; xg_device_score=7.481074081749139; device_web_cpu_core=4; device_web_memory_size=8; architecture=amd64; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A9.5%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; strategyABtestKey=%221772153382.915%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAIC7ctjT5I2bELwn_OiFTSR8ZCtfUnXqZm-i6lc149WE%2F1772208000000%2F0%2F1772153382921%2F0%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRzBqZm1UVVM0S0YzcnExQVhLN3Bxc3Zxc2pINjZBbzFXcXBaNnQrRWVuMEpaMitwOXJXZUpoeUZTekwwRU9VZ0xSKzJIOE5jSkFPZDhzTmx5MnNSWDQ9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; ttwid=1%7CO-EqEauJrUnjLPKFzJ7bwBsHDibcd58xT2Rklkv7-lc%7C1772153386%7C9ff406b04c159bc2003ba5cb7d67bb4458f2693385f458ed467fbe403241a104; home_can_add_dy_2_desktop=%221%22; biz_trace_id=f7500232; volume_info=%7B%22isMute%22%3Afalse%2C%22isUserMute%22%3Afalse%2C%22volume%22%3A0.503%7D; odin_tt=5fdc9f5da4651840d202315a50e0fa2ccfab13ec6923744c0738cbeaf034b8542fbf645dd7a860436c6968056be3e20b046a67537443a2b25de76cf237a8f19e; playRecommendGuideTagCount=2; totalRecommendGuideTagCount=26; bd_ticket_guard_client_data_v2=eyJyZWVfcHVibGljX2tleSI6IkJHMGpmbVRVUzRLRjNycTFBWEs3cHFzdnFzakg2NkFvMVdxcFo2dCtFZW4wSloyK3A5cldlSmh5RlN6TDBFT1VnTFIrMkg4TmNKQU9kOHNObHkyc1JYND0iLCJ0c19zaWduIjoidHMuMi43NWZlZmI0MGNhMWY4YTZjMDk4ZTU2NzQ4MWViZmJlZjBiZDAyZmJiY2ZkNTJiODA2N2ZmMGVjMjljNmE5MjIzYzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcV9jb250ZW50Ijoic2VjX3RzIiwicmVxX3NpZ24iOiJRMDY5anFpUjliL21oVGZrbHdNRTFOUWh0V1dueUJReUhFdjNSYWZjbGFzPSIsInNlY190cyI6IiN1OEFCVXg3SXhGTmEwcjYrRTNTTWhVcW1VNnRuaU0vODRQbWtyeVFuYUdCdDRkQmI3Tm5PemNxdVdWa1YifQ%3D%3D; IsDouyinActive=false; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; __ac_nonce=069a0fa2d0032bfdb95e3; __ac_signature=_02B4Z6wo00f01gaWczgAAIDCyuBlQZJybe4GtneAAOgT9a; __ac_referer=__ac_blank",
    "Referer": "https://www.douyin.com/",
    
    
    
    
    
    
    
    
    
    
}
print("海内存知己,天涯若比邻")
def download_file(url, output_path, headers):
    """下载文件的通用函数"""
    if not url:
        print("URL 为空，跳过下载。")
        return
    try:
        print(f"正在请求: {url}")
        # stream=True 启用流式下载，适合大文件
        # timeout 设置超时时间，防止长时间无响应
        with requests.get(url, headers=headers, timeout=15, stream=True) as response:
            response.raise_for_status()  # 检查请求是否成功 (状态码 200)
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            print(f"开始下载: {output_path}")
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024 * 5): # 每次写入 5MB
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        # 可选：打印下载进度
                        print(f"下载进度: {downloaded_size}/{total_size}", end='\r')
            
            print("下载完成！")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误: {e}")
    except requests.exceptions.ConnectionError:
        print("网络连接错误，请检查网络。")
    except requests.exceptions.Timeout:
        print("请求超时。")
    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

# 主程序逻辑
if __name__ == "__main__":
    print("海内存知己,天涯若比邻")
    
    # 下载视频
    video_output = r"D:\YES\WEN\Python\Downloads\测试video.mp4"
    download_file(video_url, video_output, headers)
    
    # 下载音频
    audio_output = r"D:\YES\WEN\Python\Downloads\测试audio.mp3"
    download_file(audio_url, audio_output, headers)

'''
user_agents = [
# Windows Edge/Chrome
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
"Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 edg/145.0.0.0",
# Mac Safari/Chrome
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
# Linux系统(Kali/Ubuntu)
"Mozilla/5.0 (X11; Kali Linux; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
# 移动端设备
"Mozilla/5.0 (Linux; Android 13; SM-S908E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
'''