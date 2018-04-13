#!/usr/bin/env python
# pymodbus synchronus endpoint client
# using this, you can read from a synchronous server to control an endpoint

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time

UNIT = 0x1

def endpointClient():
    # create the endpoint client
    client = ModbusClient('localhost', port=5020)
    # connect the client to the server
    client.connect()

    print "Reading data from coil..."
    # set temporary variable
    val = False

    # create an infinite loop
    while(True):
        # read the coils
        rr = client.read_coils(1, 1, unit=UNIT)
        # we care about the first value as that is what is modified by the
        # other client
        if (rr.bits[0] != val) and (rr.bits[0] == True):
            #if both are different and we receive True, do this:
            print "Turning water pump on."
            val = True
        elif (rr.bits[0] != val) and (rr.bits[0] == False):
            #if both are different and we receive False, do this:
            print "Turning water pump off."
            val = False
        # sleep for 5 seconds so it is not constantly checking
        time.sleep(5)

    # close the client
    client.close()


if __name__ == "__main__":
    endpointClient()
