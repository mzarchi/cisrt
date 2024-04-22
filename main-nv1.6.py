from getpass import getpass

import paramiko
import SQLite as sq3
import config as cf
import method as md


print(r'''
   _____ _          _
  / ____( )        | |    - developer: Mohammad Zarchi
 | |     _ ___ _ __| |_   - version: Cisrt-v1.6
 | |    | / __| '__| __|  - release data: 2024 Apr 21
 | |____| \__ \ |  | |_   - github: mzarchi/cisrt
  \_____|_|___/_|   \__|  - languege: python
''')

sq3.create()
exit_opt = None
while True:
    if sq3.count_record()[0] > 0:
        if cf.username is None:
            config = sq3.search()[0]
            cf.switch_core = config[1]
            cf.username = config[2]
            cf.password = config[3]
            cf.ssh_port = config[4]
            
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
                if "DYNAMIC" in port_data['text'] or "dynamic" in port_data['text']:
                    print(f"switch-ip: {switch_ip:<18s}- port-details: {port_data['port'][0]:<10s}- Trunk")#.format(switch_ip, port_data['port'][0]))
                    switch_ip = port_details['ip'][0]
                else:
                    print(f"switch-ip: {switch_ip:<18s}- port-details: {port_data['port'][0]:<10s}- Access")
                    print(f"client-ip: {client_ip:<18s}- mac-address: {mac}")
                    break
                
        except Exception as e:
            print(e)
            
        exit_opt = input("For exit insert \"E\" or Enter for continue: ")
    else:
        switch_core = input("Insert your switch-core ip: ")
        username = input("Insert your username: ")
        password = getpass("Insert your password: ")
        port = input("Insert your ssh port: ")
        sq3.insert(switch_core, username, password, port)
    
    if exit_opt == "E" or exit_opt == "e":
        break