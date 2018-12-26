import qrcode
import image

image = qrcode.make('WIFI:T:WPA;S:AER2200-b15-5g;P:12345678;H:false;;')
image.save('wifi-qrcode.png')
