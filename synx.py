import re
import requests
import base64
import os
import json
import asyncio
import ping3
from ping3 import ping
import time

CONFIG_FILE = "config_kuranomiprojectSYnX.json"

# ==================== FIXED URL ====================
FIXED_URL = "https://portal-as.ruijienetworks.com/api/auth/wifidog?stage=portal&gw_id=c8cd555c90fe&gw_sn=H1T07Y5002825&gw_address=192.168.110.1&gw_port=2060&ip=192.168.110.14&mac=b2:d5:ee:b0:d8:f6&slot_num=8&nasip=192.168.1.151&ssid=VLAN233&ustate=0&mac_req=1&url=http%3A%2F%2F192.168.0.1%2F&chap_id=%5C111&chap_challenge=%5C133%5C017%5C322%5C100%5C140%5C102%5C321%5C360%5C140%5C300%5C055%5C154%5C140%5C312%5C116%5C071"
# ===================================================

# Color codes
g = "\033[1;32m"
y = "\033[1;33m"
r = "\033[1;31m"
w = "\033[0m"
c = "\033[1;36m"

# Global variables
auto_loop_running = False
loop_interval = 240  # Default
internet_connected = False
last_ping_time = 0
ping_history = []

# Store user inputs
user_mac = ""
user_voucher = ""
user_gateway = ""

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print("\033[1;31m" + "="*56)
    print("\033[1;31m  ██╗  ██╗██╗   ██╗██████╗  █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗██╗\033[0m")
    print("\033[1;31m  ██║ ██╔╝██║   ██║██╔══██╗██╔══██╗████╗  ██║██╔═══██╗████╗ ████║██║\033[0m")
    print("\033[1;31m  █████╔╝ ██║   ██║██████╔╝███████║██╔██╗ ██║██║   ██║██╔████╔██║██║\033[0m")
    print("\033[1;31m  ██╔═██╗ ██║   ██║██╔══██╗██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║\033[0m")
    print("\033[1;31m  ██║  ██╗╚██████╔╝██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║\033[0m")
    print("\033[1;31m  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝\033[0m")
    print("\033[1;31m" + "="*56 + "\033[0m")
    print("\033[0m          KURANOMI - Project SYnX \033[0m")
    print("\033[1;36m       Developer: @Kuranomi10\033[0m")
    print("\033[1;31m" + "="*56 + "\033[0m")

def show_menu():
    print("\n" + "="*56)
    print("\033[1;33m[ MODE SELECTION ]\033[0m")
    print("  \033[1;32m[1]\033[0m 🖕Kill!")
    print("  \033[1;34m[2]\033[0m 📱Gaming Mode  ")
    print("  \033[1;36m[3]\033[0m ⭐ Stable  ")
    print("  \033[1;36m[4]\033[0m 📈Super Stable ")
    print("  \033[1;31m[5]\033[0m 🔄 Change WiFi Settings")
    print("  \033[1;31m[6]\033[0m 🚪 Exit")
    print("="*56)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(mac_address, voucher, gateway_ip):
    config = {
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
            
            if 'error' in res_text.lower() or 'invalid' in res_text.lower():
                return None, res_text
            
            token_match = re.search('token=(.*?)&', res_text)
            if token_match:
                return token_match.group(1), None
            else:
                return None, res_text
                
    except Exception as Error:
        print(f"\033[1;31m[-] Voucher Login Error: {Error}\033[0m")
        return None, str(Error)

async def get_smart_ping():
    """Ping စစ်ပြီး latency ကို အရောင်နဲ့ပြပေးမယ်"""
    global internet_connected, last_ping_time, ping_history
    
    targets = ["google.com", "8.8.8.8", "cloudflare.com"]
    
    print("\n" + "="*56)
    print("  📶 Real-Time Internet Status")
    print("="*56)
    
    connected = False
    best_result = None
    best_latency = 9999
    
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
                
                if ping_ms < best_latency:
                    best_latency = ping_ms
                    best_result = f"{color}{ping_ms} ms ({target}){w}"
            else:
                print(f"  {r}✗{w} {target:15} → {r}Timeout{w}")
                
        except Exception as e:
            print(f"  {r}✗{w} {target:15} → {r}Error{w}")
            continue
    
    print("="*56)
    
    internet_connected = connected
    last_ping_time = time.time()
    if connected:
        ping_history.append(best_latency)
        if len(ping_history) > 10:
            ping_history.pop(0)
    
    if connected:
        print(f"\n  {g}✅ Internet Connected!{w}")
        return best_result if best_result else f"{g}Connected{w}"
    else:
        print(f"\n  {r}❌ No Internet Connection (Offline){w}")
        return f"{r}Offline{w}"

def get_internet_status():
    """Real-time internet status check without printing"""
    global internet_connected
    
    try:
        result = ping("8.8.8.8", timeout=2)
        if result is not None:
            internet_connected = True
            return True
        else:
            internet_connected = False
            return False
    except:
        internet_connected = False
        return False

def do_bypass(session_url, mac_address, voucher, gateway_ip):
    """Bypass လုပ်ငန်းစဉ်"""
    session_id = get_session_id(session_url, mac_address)
    print(f"[+] Inactive Session Id: {session_id}")
    
    if not session_id:
        return False
        
    active_session_id, error_msg = login_voucher(session_id, voucher)
    
    if not active_session_id:
        print(f"\033[1;31m[✗] Voucher code သက်တမ်းကုန်ဆုံးနေပါသည် သို့မဟုတ် Session Id ရှာမတွေ့ပါ\033[0m")
        return False
    
    print(f"[+] Active Session Id: {active_session_id}")

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    params = {
        'token': active_session_id,
        'phoneNumber': 'KuranomiUser',
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
            print("\n\033[1;31m[-] Internet Bypass မအောင်မြင်ပါ သို့မဟုတ် Router မှ Bypass အောင်မြင်ခြင်းကို မမြင်စေရန် တားမြစ်ထားသည်.\033[0m")
            return False
    except Exception as e:
        print(f"\n\033[1;31m[-] Auth Gateway connection error: {e}\033[0m")
        return False

async def auto_loop_bypass(session_url, mac_address, voucher, gateway_ip, mode="gaming"):
    """Auto loop bypass function"""
    global auto_loop_running, loop_interval, internet_connected
    
    auto_loop_running = True
    loop_count = 0
    
    # Set interval based on mode
    if mode == "gaming":
        loop_interval = 180
        mode_name = "🎮 Gaming Mode"
    elif mode == "stable":
        loop_interval = 420
        mode_name = "🛡️ Stable Mode"
    elif mode == "super":
        loop_interval = 240
        mode_name = "⭐ Super Stable (Recommended)"
    else: #kill
         loop_interval = 10
         mode_name =" Kill "
    
    print("\n" + "="*56)
    print(f"  🔄 {mode_name}")
    print(f"  ⏱️  Interval: {loop_interval} seconds")
    print("  ⏹️  Press Ctrl+C to stop")
    print("="*56)
    
    while auto_loop_running:
        loop_count += 1
        print(f"\n{'='*56}")
        print(f"  🔄 Loop #{loop_count} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  📡 Mode: {mode_name}")
        print(f"{'='*56}")
        
        # Run bypass
        success = do_bypass(session_url, mac_address, voucher, gateway_ip)
        
        # Always check internet status
        result = await get_smart_ping()
        print(f"\n  📊 Ping Result: {result}")
        
        # ===== WAIT FOR NEXT LOOP =====
        print(f"\n  ⏳ Waiting {loop_interval} seconds before next loop...")
        wait_steps = max(1, loop_interval // 10)
        for i in range(loop_interval, 0, -wait_steps):
            if not auto_loop_running:
                break
            status = "🌐 Online" if get_internet_status() else "📴 Offline"
            print(f"  ⏱️  {i}s remaining | {status}")
            await asyncio.sleep(wait_steps)
    
    print("\n  🛑 Auto loop stopped.")

def get_user_inputs():
    """Get MAC, Voucher, Gateway from user"""
    global user_mac, user_voucher, user_gateway
    
    config = load_config()
    
    old_mac = config.get("mac_address", "")
    old_voucher = config.get("voucher", "")
    old_ip = config.get("gateway_ip", "")
    
    print("\033[1;33m[+] WiFi Settings Configuration\033[0m")
    print("="*56)
    print("\033[1;36m[!] Wifiအချက်အလက်များဖြည့်သွင်းပါ:\033[0m\n")

    if old_mac:
        print(f"\033[1;34m[ Saved MAC ]: {old_mac}\033[0m")
    mac_address = input("\033[1;32m=> MAC Address (e.g. 10:3f:44:9d:b8:e4): \033[0m").strip() or old_mac
    if not mac_address:
        print("\033[1;31m[-] MAC Address ထည့်ပါ!\033[0m")
        return None, None, None

    if old_voucher:
        print(f"\033[1;34m[ Saved Voucher ]: {old_voucher}\033[0m")
    voucher = input("\033[1;32m=> Voucher Code: \033[0m").strip() or old_voucher
    if not voucher:
        print("\033[1;31m[-] Voucher Code ထည့်ပါ\033[0m")
        return None, None, None

    if old_ip:
        print(f"\033[1;34m[ Saved Gateway ]: {old_ip}\033[0m")
    gateway_ip = input("\033[1;32m=> Gateway IP (e.g. 192.168.60.1): \033[0m").strip() or old_ip
    if not gateway_ip:
        print("\033[1;31m[-] Gateway IP ထည့်ပါ!\033[0m")
        return None, None, None

    save_config(mac_address, voucher, gateway_ip)
    
    # Store in global variables
    user_mac = mac_address
    user_voucher = voucher
    user_gateway = gateway_ip
    
    return mac_address, voucher, gateway_ip

def start_bypass(mode="gaming"):
    """Main bypass function with mode selection"""
    global user_mac, user_voucher, user_gateway
    
    clear_screen()
    banner()
    
    session_url = FIXED_URL
    
    # Show current settings
    print("\n" + "="*56)
    print("\033[1;36m[ Current Settings ]\033[0m")
    print(f"  📌 MAC: \033[1;32m{user_mac}\033[0m")
    print(f"  📌 Voucher: \033[1;32m{user_voucher}\033[0m")
    print(f"  📌 Gateway: \033[1;32m{user_gateway}\033[0m")
    print("="*56)
    
    print("\n\033[1;33m[*] Internet Bypass စတင်နေပါပြီ..(bypass fail  ပြလည်းpingပေါ်ရင်လိုင်းရပါတယ်\033[0m")
    
    # First bypass
    success = do_bypass(session_url, user_mac, user_voucher, user_gateway)
    
    # Ping check (Bypass အောင်သည်ဖြစ်စေ မအောင်သည်ဖြစ်စေ)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_smart_ping())
        loop.close()
        print(f"\n  📊 Ping Result: {result}")
    except Exception as e:
        print(f"\n\033[1;31m[-] Ping Error: {e}\033[0m")
    
    # ===== Auto Loop =====
    print("\n" + "="*56)
    print(f"  🔄 Starting Auto Bypass Loop ({mode})...")
    print("="*56)
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(auto_loop_bypass(session_url, user_mac, user_voucher, user_gateway, mode))
        loop.close()
    except KeyboardInterrupt:
        print("\n\n  🛑 Auto loop stopped by user.")
    except Exception as e:
        print(f"\n\033[1;31m[-] Auto loop error: {e}\033[0m")
        
    input("\nPress Enter to exit...")

def main():
    global user_mac, user_voucher, user_gateway
    
    # First time - get user inputs
    clear_screen()
    banner()
    mac, voucher, gateway = get_user_inputs()
    
    if not mac or not voucher or not gateway:
        print("\n\033[1;31m[-] All fields are required. Exiting...\033[0m")
        time.sleep(2)
        return
    
    while True:
        clear_screen()
        banner()
        
        # Show current settings
        print("\n" + "="*56)
        print("\033[1;36m[ Current Settings ]\033[0m")
        print(f"  📌 MAC: \033[1;32m{user_mac}\033[0m")
        print(f"  📌 Voucher: \033[1;32m{user_voucher}\033[0m")
        print(f"  📌 Gateway: \033[1;32m{user_gateway}\033[0m")
        print("="*56)
        
        show_menu()
        
        choice = input("\n\033[1;32m=> Select option (1-6): \033[0m").strip()
        
        if choice == "1":
            start_bypass("kill")
        elif choice == "2":
            start_bypass("gaming")
        elif choice == "3":
            start_bypass("stable")
        elif choice == "4":
            start_bypass("super")
        elif choice == "5":
            clear_screen()
            banner()
            mac, voucher, gateway = get_user_inputs()
            if not mac or not voucher or not gateway:
                print("\n\033[1;31m[-] All fields are required. Keeping old settings.\033[0m")
                time.sleep(2)
        elif choice == "6":
            print("\n\033[1;36mGood Bye! See you again.\033[0m")
            break
        else:
            print("\033[1;31m[-] မှားယွင်းနေပါသည်။ 1-6 အတွင်းသာ ရွေးပေးပါ။\033[0m")
            time.sleep(1)

if __name__ == "__main__":
    main()