import paramiko

hostname = '192.168.0.1'    
port = 22
username = 'admin'
password = '1q2w3e4r'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port, username, password)
command = 'cat /config/wlan/radio/0/bss/0/wpapsk'
(stdin, stdout, stderr) = client.exec_command(command)
for line in stdout.readlines():
    print(line)
client.close()

