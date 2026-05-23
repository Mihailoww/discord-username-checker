import requests
import random
import string
from colorama import init, Fore

init()

proxy_index = 0
request_count = 0

option = 0


def random_name(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


print("""
Choose your option!
      
1. 3 Letter name finder
2. 4 Letter name finder
""")

def option_name():
    global option

    cmd = int(input('Type your option: '))

    if cmd == 1:
        option = 3
    elif cmd == 2:
        option = 4
    else:
        print(Fore.RED + 'Invalid Option!')


option_name()

with open('proxies.txt', 'r') as f:
    proxies = f.read().split('\n')

def get_proxy():
    return {
        'https': proxies[proxy_index]
    }


while True:

    payload = { "username": random_name(option) }

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', 
               'Origin': 'https://discord.com', 
               'Referer': 'https://discord.com/register', 
               'Content-Type': 'application/json' }
    

    try:
        req = requests.post('https://discord.com/api/v9/unique-username/username-attempt-unauthed', headers=headers, json=payload, proxies=get_proxy())

        request_count += 1

        if request_count >= 10:
            proxy_index = (proxy_index + 1) % len(proxies)
            request_count = 0

    except:
        proxy_index = (proxy_index + 1) % len(proxies)
        request_count = 0
        continue


    try:
        req_json = req.json()
    except:
        continue


    if req_json.get('message') == "The resource is being rate limited.":
        print(Fore.YELLOW + 'Rate Limited. Switching to next proxy')
        proxy_index = (proxy_index + 1) % len(proxies)
        request_count = 0
        continue

    elif req_json.get('taken') == True:
        print(Fore.RED + f'{payload["username"]} is Taken')
    
    elif req_json.get('taken') == False:
        print(Fore.GREEN + f'{payload["username"]} is Available (Added to available.txt)')
        with open ('available.txt', 'a') as valid:
            valid.write(f'\n{payload["username"]}')