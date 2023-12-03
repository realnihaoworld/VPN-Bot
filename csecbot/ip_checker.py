import os
import ipaddress

directory = '/Users/zheng/Documents/Github/discordbot/example_network/'

# Checks if a user occupies a certain ip address
# Dictionary format - ip_dict{'user': 'ip'}

def check_ip(directory, username, cidr_input):
    ip_dict = {}
    #paramaterize this at some point
    netIpv4Address = ipaddress.ip_network(cidr_input)
    # splits the files by '_' and puts the ip into the value
    # and the user in the key
    for filename in os.listdir(directory):
        name = filename.split("_")
        ip_dict[name[1]] = name[0]
    
    if username in ip_dict:
        print(f'{username} already has an ip address at {ip_dict[username]}')
        filename = f"{ip_dict[username]}_{username}"
        file = open("/Users/zheng/Documents/Github/discordbot/test_network/" + filename, 'w')
        file.write("put config file here")
        file.close()
    else:
        # This is if the user who is generating a config file 
        # does not have an ip already.
        # Generate ip addresses using ipaddress module
        new_ip = "temp"
        filename = f"{new_ip}_{username}"
        file = open("/Users/zheng/Documents/Github/discordbot/test_network/" + filename, 'w')
        file.write("put config file info here")
        file.close()
    
    for i in netIpv4Address:
        print(i)

check_ip(directory, "user69", "172.31.0.0/16")

#print(directory + 'test_user')