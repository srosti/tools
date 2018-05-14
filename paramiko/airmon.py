from scp import SCPClient
import paramiko
import re
import time

server_ip = 'X.X.X.X'
server_port = 2399
server_username = 'XXXXX'
server_password = 'XXXXXX'
wifi_iface = 'wlp2s0'
monitor_iface = None


def enable_mon():
    print("Create ssh connection to server")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server_ip, port=server_port, username=server_username, password=server_password)

    transport = ssh.get_transport()
    channel = transport.open_session()
    channel.get_pty()
    stdout = channel.makefile('rb', 1024)

    print("Put {} into monitor mode".format(wifi_iface))
    enable_command = '/usr/bin/sudo airmon-ng start ' + wifi_iface
    channel.exec_command(enable_command)
    while True:
        time.sleep(1)
        stdout = channel.recv(4096).decode('utf8')
        print(stdout)
        if re.search('[Pp]assword', stdout):
            channel.send(server_password + '\n')
        if re.search('monitor', stdout):
            monitor_iface = re.search('mon\d{1}', stdout).group(0)
            print("Created {} monitor interface".format(monitor_iface))
            break 

    transport.close()
    return monitor_iface


def disable_mon():
    print("Create ssh connection to server")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server_ip, port=server_port, username=server_username, password=server_password)

    transport = ssh.get_transport()
    channel = transport.open_session()
    channel.get_pty()
    stdout = channel.makefile('rb', 1024)

    print("disable {} monitor interface".format(monitor_iface))
    disable_command = '/usr/bin/sudo airmon-ng stop {}'.format(monitor_iface)
    channel.exec_command(disable_command)
    while channel.recv_ready() is False:
        time.sleep(1)
        stdout = channel.recv(4096).decode('utf8')
        if re.search('[Pp]assword', stdout):
            channel.send(server_password + '\n')
        if re.search('removed', stdout):
            print("Disabled {} interface".monitor_iface)
            break


if __name__ == '__main__':
    monitor_iface = enable_mon()
    disable_mon()
