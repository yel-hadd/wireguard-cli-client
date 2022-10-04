from subprocess import run, CalledProcessError, DEVNULL, PIPE
from multiprocessing import Process
from urllib.request import urlopen
from urllib.error import URLError
from random import choice as ch
from termcolor import colored
from itertools import cycle
from sys import stdout
from os import listdir
from time import sleep


def connect_animation():
    emolst = ["🌎", "🌍", "🌏"]
    emo = cycle(emolst)
    while True:
        stdout.write(f"\rConnecting {next(emo)}...")
        sleep(0.3)
        stdout.flush()


def check_internet():
    while True:
        try:
            urlopen("https://duckduckgo.com/", timeout=10)
            print("\n")
            return 0
        except URLError:
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
    # ADD ERROR HANDLING LATER
    run(
        ["wg-quick", "down", f"/etc/wireguard/{interface}.conf"],
        check=True,
        stdout=DEVNULL,
        stderr=DEVNULL,
    )
    print(colored(f"✅ DISCONNECTED {interface} SUCCESSFULLY ✅", "green"))
    return 0


def connect():
    thread = Process(target=connect_animation)
    try:
        run(
            ["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"],
            check=True,
            stdout=PIPE,
            stderr=DEVNULL,
        )
    except CalledProcessError:
        print(
            colored("\n⛔ Connection Error: Please Verify Your Internet Connection ⛔\n")
        )
        return
    try:
        interface = run(
            ["sudo", "wg", "show", "interfaces"],
            check=True,
            stdout=PIPE,
            stderr=DEVNULL,
        )
        interface = interface.stdout.decode("utf-8").replace("\n", "")
        interface = interface.split(" ")
    except CalledProcessError:
        print(
            colored(
                "\n⛔ Permission Error: Please Run the Program with Root Privilege ⛔\n"
            )
        )
        return
    if interface[0] == "":
        interface = None
        print(colored("STATUS : DISCONNECTED", "red"))
        connected = False
    else:
        interface = interface[-1]
        print(colored(f"STATUS : CONNECTED to {interface}", "green"))
        connected = True
    servers = []
    try:
        for file in listdir("/etc/wireguard/"):
            if file.endswith(".conf") and not file.endswith("wg0.conf"):
                servers.append(file)
    except PermissionError:
        print(
            colored(
                "\n⛔ PermissionError: Please Run the Program with Root Privilege ⛔\n"
            )
        )
        return
    servers_count = len(servers)
    if servers_count == 0:
        print(colored("\n⛔ Error : No Servers Available, exiting ... ⛔\n", "red"))
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
            if interface:
                disconnect(interface)
            return 0
        else:
            run(["clear"])
            print(colored(f"ERROR : ALREADY DISCONNECTED", "red"))
            return 0
    elif choice == servers_count + 2:
        print("exiting ...")
        return 0
    elif choice == 0:
        if connected:
            if interface:
                disconnect(interface)
        temp = ch(servers)
        # add error handeling later
        run(
            ["wg-quick", "up", f"/etc/wireguard/{temp}"],
            check=True,
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
        interface = temp.split(".")[0]
        thread.start()
        check_internet()
        thread.terminate()
        print(colored(f"✅ CONNECTED TO {interface} SUCCESSFULLY ✅", "green"))
        new_ip = run(
            ["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"],
            check=True,
            stdout=PIPE,
            stderr=DEVNULL,
        )
        new_ip = new_ip.stdout.decode("utf-8").replace("\n", "")
        print(f"new ip: {new_ip}")
    elif 0 < choice <= servers_count:
        if connected:
            if interface:
                disconnect(interface)
        choice = int(choice)
        temp = servers[choice - 1]
        # add error handling later
        run(
            ["wg-quick", "up", f"/etc/wireguard/{temp}"],
            check=True,
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
        interface = temp.split(".")[0]
        thread.start()
        check_internet()
        thread.terminate()
        print(colored(f"✅ CONNECTED TO {interface} SUCCESSFULLY ✅", "green"))
        new_ip = run(
            ["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"],
            check=True,
            stdout=PIPE,
            stderr=DEVNULL,
        )
        new_ip = new_ip.stdout.decode("utf-8").replace("\n", "")
        print(f"new ip: {new_ip}")
    else:
        run("clear")
        print("<--- invalid Input, Retry! --->\n")
        connect()
    return 0


connect()
