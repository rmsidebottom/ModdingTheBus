#!/usr/bin/env python
# pymodbus synchronus managment client
# using this, you can write to a synchronous server

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from key import ip


UNIT = 0x1

def mgmtClient():
    # create the TCP client
    client = ModbusClient(ip, port=5020)

    # connect the client to the server
    client.connect()

    print("Write to a Coil and read back")

    # retrieve user input
    tf = input("Enter on or off, exit to quit: ")
    while tf.lower() != "exit":
        if tf == "on":
            # write ON signal to server
            rq = client.write_coil(1, True, unit=UNIT)
        else:
            # write OFF signal to server
            rq = client.write_coil(1, False, unit=UNIT)
        # retrieve user input again
        tf = input("Enter on or off, exit to quit: ")

    # close the client
    client.close()

if __name__ == "__main__":
    mgmtClient()
