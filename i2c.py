import smbus2
import keyboard


lenth_val = 0;
dirsend_flag=0;

with SMBus(1) as bus:
    # Read a block of 16 bytes from address 80, offset 0
    block = bus.read_i2c_block_data(52, 0, 16)
    # Returned value is a list of 16 bytes
    print(block)



while True:
    try:
        if keyboard.is_pressed('q'):
            print('You quit')
            break
    except:
        c = Wire.read();
        break
