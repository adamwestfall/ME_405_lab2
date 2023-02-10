# boot.py -- run on boot to configure USB and filesystem
# Put app code in main.py

#import machine
import pyb
#pyb.country('US') # ISO 3166-1 Alpha-2 code, eg US, GB, DE, AU

#pyb.usb_mode('VCP+MSC') # act as a serial and a storage device
#pyb.usb_mode('VCP+HID') # act as a serial device and a mouse

print("Disabling REPL on UART 2...",end='')
pyb.repl_uart(None)
print("done")

f1 = 'main_serialTest.py'
f2 = 'main.py'

print("Please select an option from the list: ")
print("[1]          %s"%(f1))
print("[2]          %s"%(f2))
option = input('')

if option == "1":
    filename = f1
elif option == "2":
    filename = f2
else:
    print("Invalid option")
    exit(99)

print("executing: " + filename + "...")
pyb.main(filename) # main script to run after this one

print("************************************************")