import usb.core
import time
import argparse

def initUSB ():
    dev = usb.core.find(idVendor=0x0403, idProduct=0xc630)
    
    if dev is None:
        raise ValueError('Device not found')
    
    return dev

def main ():
    parser = argparse.ArgumentParser(description="ping+ cli interface")
    parser.add_argument('-s', '--sendstring', help="Sends a string to the ping+")
    parser.add_argument('-c', '--clear', action="store_true", help="Clears the display by scrolling it out")
    parser.add_argument('-p', '--scrollspeed', type=int, help="Sets the scrolling speed")
    parser.add_argument('-w', '--waitdelay', type=int, help="Sets the wait delay")

    args = parser.parse_args()

    dev = initUSB()

    # Sends the clear command to the usb device and waits 0.5 seconds
    if (args.clear):
        dev.ctrl_transfer(0x40, 20, 0, 0)
        time.sleep(0.5)
    
    # Clears the off-screen buffer, sends the string to the usb device and copies the off-screen buffer to the main
    # buffer. 
    if (args.sendstring):
        dev.ctrl_transfer(0x40, 10, 0, 0)
        
        for c in args.sendstring:
            dev.ctrl_transfer(0x40, 4, 0, ord(c))
        
        dev.ctrl_transfer(0x40, 5, 0, 0)
    
    # Sets the wait delay at the end of a line        
    if (args.waitdelay):
        dev.ctrl_transfer(0x40, 25, args.waitdelay, 0)
    
    # Sets the scrolling speed
    if (args.scrollspeed):
        dev.ctrl_transfer(0x40, 26, args.scrollspeed, 0)

main()
print("All done. Type -h for help")