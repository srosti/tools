import subprocess

ssid_list = ['SSID', 'Toby']


ssid_found = None

#sudo iw wlx00026f855193 scan | egrep 'SSID|signal' | egrep -B1 'Toby'
#while(True):
#output = subprocess.check_output(['sudo', 'iw', 'wlx00026f855193', 'scan', '|', '\'SSID|signal\'', '|', 'egrep', '-B1', '\'Toby\''])
output = subprocess.check_output(['sudo', 'iw', 'wlx00026f855193', 'scan'])
for line in output.splitlines():
#    if 'Toby' in line.decode():
    if all(x in line.decode() for x in ssid_list):
        ssid_found = True
        print(line.decode())
    if 'signal' in line.decode() and ssid_found:
        temp_string = line.decode().split(' ')
        dbm = float(temp_string[1])
        print(dbm)
        ssid_found = False

