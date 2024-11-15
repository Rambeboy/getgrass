import requests
import time
import asyncio
import json
import ssl
import uuid
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from websockets_proxy import Proxy, proxy_connect
from fake_useragent import UserAgent
from loguru import logger
import schedule
import base64

banner = """
==================================================================
 █████╗ ██╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗ 
██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
███████║██║██████╔╝██║  ██║██████╔╝██║   ██║██████╔╝
██╔══██║██║██╔══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝ 
██║  ██║██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║     
╚═╝  ╚═╝╚═╝╚═╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     
                                                    
██╗███╗   ██╗███████╗██╗██████╗ ███████╗██████╗     
██║████╗  ██║██╔════╝██║██╔══██╗██╔════╝██╔══██╗    
██║██╔██╗ ██║███████╗██║██║  ██║█████╗  ██████╔╝    
██║██║╚██╗██║╚════██║██║██║  ██║██╔══╝  ██╔══██╗    
██║██║ ╚████║███████║██║██████╔╝███████╗██║  ██║    
╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝    

Join our Telegram channel for the latest updates: t.me/airdropinsiderid

Airdrop Insider
==================================================================
"""
print(banner)
time.sleep(1)

test_url = 'https://www.google.com'
encoded_proxy_list_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3IwMHRlZS9Qcm94eS1MaXN0L3JlZnMvaGVhZHMvbWFpbi9Tb2NrczUudHh0'
output_file = 'active_proxies.txt'
user_ids_file = 'users.txt'
proxy_list_url = base64.b64decode(encoded_proxy_list_url).decode()

def check_proxy(proxy):
    try:
        session = requests.Session()
        session.proxies = {'socks5': proxy}
        response = session.head(test_url, timeout=10)
        if response.status_code == 200:
            logger.info(f"Proxy {proxy} Mantep Nih")
            return proxy
        else:
            logger.warning(f"Proxy {proxy} returned status code {response.status_code}.")
            return None
    except Exception as e:
        logger.error(f"Error occurred while checking {proxy}: {e}")
        return None

def save_active_proxies(proxy_list_url, output_file, max_proxies=2000):
    try:
        response = requests.get(proxy_list_url)
        if response.status_code == 200:
            proxy_data = response.text.strip().split('\n')
            random_proxies = random.sample(proxy_data, min(max_proxies, len(proxy_data)))
            active_proxies = []
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(check_proxy, proxy.strip()) for proxy in random_proxies]
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        active_proxies.append(result)
            random_active_proxies = random.sample(active_proxies, min(355, len(active_proxies)))
            with open(output_file, 'w') as f:
                for proxy in random_active_proxies:
                    f.write(f"http://{proxy}\n")
            return random_active_proxies
        else:
            logger.error(f"Gagal mengambil daftar proxy dari {proxy_list_url}. Kode status: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error terjadi pas ambil atau proses daftar proxy dari {proxy_list_url}: {e}")
        return []

def log_reputation(proxy, completeness, consistency, timeliness, availability):
    logger.info(f"Proxy: {proxy}, Complete: {completeness}, Konsistensi: {consistency}, Waktu: {timeliness}, Ketersediaan: {availability}")

async def connect_to_wss(socks5_proxy, user_id, traffic_type='PET'):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, socks5_proxy))
    logger.info(device_id)
    user_agent = UserAgent()
    random_user_agent = user_agent.random

    while True:
        try:
            await asyncio.sleep(1)
            custom_headers = {"User-Agent": random_user_agent}
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            urilist = ["wss://proxy.wynd.network:4444/", "wss://proxy.wynd.network:4650/", "wss://proxy2.wynd.network:4444/", "wss://proxy2.wynd.network:4650/", "wss://proxy3.wynd.network:4444/", "wss://proxy3.wynd.network:4650/"]
            uri = random.choice(urilist)
            proxy = Proxy.from_url(socks5_proxy)

            async with proxy_connect(uri, proxy=proxy, ssl=ssl_context, server_hostname=server_hostname,
                                     extra_headers=custom_headers) as websocket:
                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                        try:
                            await websocket.send(send_message)
                            logger.debug(send_message)
                        except Exception as e:
                            logger.error(f"Gagal kirim PING: {e}")
                        await asyncio.sleep(2)

                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(message)

                    completeness = True 
                    consistency = True
                    timeliness = True 
                    availability = True 

                    log_reputation(socks5_proxy, completeness, consistency, timeliness, availability)

                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers['User-Agent'],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "3.3.2"
                            }
                        }
                        try:
                            await websocket.send(json.dumps(auth_response))
                            logger.debug(auth_response)
                        except Exception as e:
                            logger.error(f"Gagal kirim respon AUTH: {e}")

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        try:
                            await websocket.send(json.dumps(pong_response))
                            logger.debug(pong_response)
                        except Exception as e:
                            logger.error(f"Gagal kirim respon PONG: {e}")

        except Exception as e:
            pass 
            await asyncio.sleep(10) 

async def main():
    with open(user_ids_file, 'r') as file:
        user_ids = file.read().splitlines()

    with open(output_file, 'r') as file:
        socks5_proxy_list = file.read().splitlines()

    tasks = [asyncio.ensure_future(connect_to_wss(proxy, user_id.strip(), traffic_type='PET')) for user_id in user_ids for proxy in socks5_proxy_list]
    await asyncio.gather(*tasks)

def perform_job():
    active_proxies = save_active_proxies(proxy_list_url, output_file)
    if active_proxies:
        asyncio.run(main())
    else:
        logger.error("Kagak ada proxy aktif, lewatin hubungan WebSocket.")

schedule.every(24).hours.do(perform_job)

perform_job()

while True:
    schedule.run_pending()
    time.sleep(1)
