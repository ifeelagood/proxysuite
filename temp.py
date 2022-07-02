import json

block_mask = b'00000000000000001111111111111111'

def ip_to_bin(ip):

    ip_int = int()

    for i,block in enumerate(ip.split('.')):
        block_bin = int(block) << (4-(i+1))*8

        ip_int += block_bin


    return bin(ip_int)


1
with open("output/live.json", 'r') as f:
    live = json.load(f)

ip_list = [p['host'] for p in live]

bin_ip_list = [ip_to_bin(ip) for ip in ip_list]

