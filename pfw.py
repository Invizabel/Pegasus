import argparse
import binascii
import os
import re
import threading
from collections import Counter
from scapy.all import *

def transforn(file_dict):
    models = []
    for key, value in file_dict.items():
        print(f"transforming: {key}")
        try:
            # open files
            with open(value, "r") as file:
                data = file.read()

            hits = []
            model = {}

            results = data.split("\n")

            # process data
            count = 0
            for result in results:
                count += 1
                cat = re.findall(r"\w{2}", result)
                tokens = Counter(cat).most_common(256)
                for token_x, token_y in tokens:
                    try:
                        model[f"{key},{token_x}"] += int(token_y)

                    except KeyError:
                        model[f"{key},{token_x}"] = int(token_y)

            # normalize data
            new_model = {}
            for i, j in model.items():
                new_model[i] = j / count

            models.append(new_model)

        except FileNotFoundError:
            pass

    return models

def train(packet):
    if packet.haslayer(ARP):
        print(packet.summary())
        with open("arp_dump.txt", "a") as file:
            file.write(f"{binascii.hexlify(raw(packet)).decode()}\n")

    if packet.haslayer(DNS):
        print(packet.summary())
        with open("dns_dump.txt", "a") as file:
            file.write(f"{binascii.hexlify(raw(packet)).decode()}\n")

    if packet.haslayer(TCP) and packet[TCP].dport == 80 or packet.haslayer(TCP) and packet[TCP].sport == 80 or packet.haslayer(TCP) and packet[TCP].dport == 8080 or packet.haslayer(TCP) and packet[TCP].sport == 8080:
        print(packet.summary())
        with open("http_dump.txt", "a") as file:
            file.write(f"{binascii.hexlify(raw(packet)).decode()}\n")

    if packet.haslayer(TCP) and packet[TCP].dport == 443 or packet.haslayer(TCP) and packet[TCP].sport == 443 or packet.haslayer(TCP) and packet[TCP].dport == 8443 or packet.haslayer(TCP) and packet[TCP].sport == 8443:
        print(packet.summary())
        with open("https_dump.txt", "a") as file:
            file.write(f"{binascii.hexlify(raw(packet)).decode()}\n")


def main():
    os.system("clear")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-mode", required = True, type = str, choices = ["train", "transform"])
    args = parser.parse_args()

    if args.mode == "train":
        sniff(prn=train)

    if args.mode == "transform":
        file_dict = {"ARP": "arp_dump.txt", "DNS": "dns_dump.txt", "HTTP": "http_dump.txt", "HTTPS": "https_dump.txt"}
        models = transforn(file_dict)

        with open("model.csv", "w") as file:
            file.write("protocol,hex,vector\n")
            for model in models:
                for i, j in model.items():
                    file.write(f"{i},{j}\n")

if __name__ == "__main__":
    main()
