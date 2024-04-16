import paramiko
import config as cf
import method as md

client_ip = input("Insert your client ip: ")
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    switch_ip = cf.switch_core
    mac = None
    
    while True:
        ssh.connect(switch_ip, cf.ssh_port, cf.username, cf.password)
            
        shell = ssh.invoke_shell()
        if switch_ip == cf.switch_core:
            mac = md.showArp(shell, client_ip)[0]
            
        port_data = md.showMacAddressTable(shell, mac)
        port_details = md.showCdpNeighborsDetails(shell, port_data['port'][0])
        if "DYNAMIC" in port_data['text']:
            print("switch-ip: {:<18s}- port-details: {:<10s}- Trunk".format(switch_ip, port_data['port'][0]))
            switch_ip = port_details['ip'][0]
        else:
            print("switch-ip: {:<18s}- port-details: {:<10s}- Access".format(switch_ip, port_data['port'][0]))
            print("client-ip: {:<18s}- Mac Address: {}".format(client_ip, mac))
            break
        
except Exception as e:
    print(e)
    
input("Please insert any key to exit ..")