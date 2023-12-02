import os

directory = '/Users/zheng/Documents/Github/discordbot/example_network'

ip_dict = {}

for filename in os.listdir(directory):
    name = filename.split("_")
    ip_dict[name[0]] = name[1]
    print(ip_dict)