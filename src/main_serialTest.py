import pyb

def writeTo(external, content):
    pass

def readFrom(external):
    pass

def initializeUART():
    print("Initializing UART...",end='')
    BAUDRATE = 115200
    external_device = pyb.UART(2, baudrate=BAUDRATE)
    external_device.init(BAUDRATE, bits=8, parity=None, stop=1, read_buf_len=0)
    print('done')
    return external_device

if __name__ == '__main__':
    
    
    try:
        external = initializeUART()
        msgVisible = False
        hey = False
        
        while True:

            if (external.any() > 0):
                print("Reading data from COMPORT: ",end='')
                charIn = external.read().decode()
                print(charIn)
                msgVisible = False
                hey = True
                print("done") 
                   
            else:
                if not msgVisible:
                    print("Waiting for input...")
                    msgVisible = True
                    external.write("Hey buddy!")
                    hey = True
                pass
                    

    except KeyboardInterrupt:
        print('leaving')