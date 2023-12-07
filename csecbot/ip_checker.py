import os
import ipaddress

directory = '/Users/zheng/Documents/Github/discordbot/example_network/'

# Checks if a user occupies a certain ip address
# Dictionary format - ip_dict{'user': 'ip'}

def check_ip(directory, username, cidr_input):
    ip_dict = {}
    # generates the ip addresses and puts them in a list
    netIpv4Address = ipaddress.ip_network(cidr_input)
    
    ip_list = []
    for i in netIpv4Address:
        ip_list.append(i)
    
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
        new_ip = ip_list[0]
        filename = f"{new_ip}_{username}"
        file = open("/Users/zheng/Documents/Github/discordbot/test_network/" + filename, 'w')
        file.write("put config file info here, this file creates a new ip")
        file.close()
        ip_list.pop(0)
    
    print(ip_list)
    
    
example_cidr = "172.31.0.0/16"
test_cidr = "172.31.0.0/30"

#TODO bring ip_list out of the function
check_ip(directory, "user69", test_cidr)

check_ip(directory, "test", test_cidr)
check_ip(directory, "yoooo", test_cidr)