import serial

def printButtonStates(bluetooth_button, tmh_rotary,
                      frnt1_button, frnt2_button,frnt3_button,frnt4_button,frnt5_button,frnt6_button,
                      sndr_rotary, volume_rotary, brightnes_rotary):
    print("Bluetooth: {}, TMH: {}, Buttons: {}{}{}{}{}{}, Sender: {}, Volume: {}, Brightness: {}".format
          (bluetooth_button, tmh_rotary, frnt1_button, frnt2_button, frnt3_button, frnt4_button, frnt5_button, frnt6_button,
           sndr_rotary >> 2, volume_rotary >> 2, brightnes_rotary >> 2))

ser = serial.Serial('/dev/ttyUSB0')  # open serial port

while True:
    line = ser.readline()
    elements = line.strip().split(b',')
    values = []
    for element in elements:
        values.append(int(element))

    printButtonStates(*values)




#ser.close()             # close port