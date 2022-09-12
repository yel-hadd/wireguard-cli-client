from itertools import cycle
from urllib.request import urlopen
from urllib.error import URLError
from sys import stdout
from os import listdir, system
from random import choice as ch
from subprocess import getoutput as output
from termcolor import colored


# add separate get choice function to avoid potential referencing before assignment
# add function to check if connected to internet and time elapsed before connecting

def check_internet():
    emolst = ["🌎", "🌍", "🌏"]
    emo = cycle(emolst)
    while True:
        stdout.write(f"\rConnecting {next(emo)}...")
        try:
            response = urlopen('https://duckduckgo.com/', timeout=10)
            print("\n")
            return 0
        except URLError:
            stdout.flush()
            pass


def get_input():
    while True:
        try:
            choice = int(input(f"Enter your choice : "))
        except ValueError:
            print(colored("\n⛔ invalid Input, Retry! ⛔️\n", "red"))
        else:
            break
    return choice


def disconnect(interface):
    output(f"wg-quick down /etc/wireguard/servers/{interface}.conf")
    print(colored(f"✅ DISCONNECTED {interface} SUCCESSFULLY ✅", "green"))
    return 0


def connect():
    old_ip = output("dig +short myip.opendns.com @resolver1.opendns.com")
    interface = output("sudo wg show interfaces").split(" ")
    if len(interface) == 1:
        interface = interface[0]
        print(colored("STATUS : DISCONNECTED", "red"))
        connected = False
    else:
        interface = interface[-1]
        print(colored(f"STATUS : CONNECTED to {interface}", "green"))
        connected = True

    servers = listdir("/etc/wireguard/servers")
    servers_count = len(servers)
    if servers_count == 0:
        print("⛔ Error : No Servers Available, exiting ... ⛔")
        return 0
    print(f"{servers_count} servers available\n")
    print("🌍 Choose the server in which you want to connect 🌍\n")
    print("0 : random Server")
    for c, v in enumerate(servers):
        print(f"{c + 1} : {v}")
    print(f"\n{servers_count + 1} : disconnect")
    print(f"{servers_count + 2} : quit\n")

    choice = get_input()

    if choice == servers_count + 1:
        if connected:
            disconnect(interface)
            return 0
        else:
            system("clear")
            print(colored(f"ERROR : ALREADY DISCONNECTED", "red"))
            return 0
    elif choice == servers_count + 2:
        print("exiting ...")
        return 0
    elif choice == 0:
        if connected:
            disconnect(interface)
        temp = ch(servers)
        output(f"wg-quick up /etc/wireguard/servers/{temp}")
        interface = temp.split(".")[0]

        print(colored(f"✅ CONNECTED TO {interface} SUCCESSFULLY ✅", "green"))
        new_ip = output("dig +short myip.opendns.com @resolver1.opendns.com")
        print(f"old ip: {old_ip}")
        print(f"new ip: {new_ip}")
    elif 0 < choice <= servers_count:
        if connected:
            disconnect(interface)
        choice = int(choice)
        temp = servers[choice - 1]
        output(f"wg-quick up /etc/wireguard/servers/{temp}")
        interface = temp.split(".")[0]
        print(colored(f"✅ CONNECTED TO {interface} SUCCESSFULLY ✅", "green"))
        new_ip = output("dig +short myip.opendns.com @resolver1.opendns.com")
        print(f"old ip: {old_ip}")
        print(f"new ip: {new_ip}")
    else:
        system("clear")
        print("<--- invalid Input, Retry! --->\n")
        connect()
    return 0


connect()
