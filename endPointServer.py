#!/usr/bin/env python3
# pymodbus synchronus server
# this will act as the modbus server, will store data sent to it

from pymodbus.server.sync import StartTcpServer
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer

from key import key, ip, bridge
import time, threading, requests, pprint

UNIT = 0x1

class ClientThread (threading.Thread):
    def __init__(self, threadID, name, client):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.client = client

    def run(self):
        # set temporary variable
        val = None
        url="http://"+bridge+"/api/"+key+"/lights/1/state"

        # create an infinite loop
        while(True):
            # read the coils
            rr = self.client.read_coils(1, 1, unit=UNIT)
            # we care about the first value as that is what is modified by the
            # other client
            if (rr.bits[0] != val) and (rr.bits[0] == True):
                #if both are different and we receive True, do this:
                print('Turning water pump on.\n')
                r = requests.put(url=url, data="{\"on\": true}")
                # pprint.PrettyPrinter(indent=4).pprint(r.json())
                val = True
            elif (rr.bits[0] != val) and (rr.bits[0] == False):
                #if both are different and we receive False, do this:
                print('Turning water pump off.\n')
                r = requests.put(url=url, data="{\"on\": false}")
                # pprint.PrettyPrinter(indent=4).pprint(r.json())
                val = False
            # sleep for 5 seconds so it is not constantly checking
            time.sleep(5)

class ServerThread (threading.Thread):
    def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

    def run(self):
        # utilizing the data store created in the example
        store = ModbusSlaveContext(
          di = ModbusSequentialDataBlock(0, [17]*100),
          co = ModbusSequentialDataBlock(0, [17]*100),
          hr = ModbusSequentialDataBlock(0, [17]*100),
          ir = ModbusSequentialDataBlock(0, [17]*100))
        context = ModbusServerContext(slaves=store, single=True)

        # initialize the server
        identity = ModbusDeviceIdentification()
        identity.VendorName = 'SCADA Capstone'
        identity.ProductCode = 'scadaDemo'
        identity.VendorUrl = 'https://github.com/rmsidebottom/ModdingTheBus'
        identity.ProductName = 'Database Store'
        identity.ModelName = 'Database Store'
        identity.MajorMinorRevision = '1.0'

        # start the TCP server, in different thread
        StartTcpServer(context, identity=identity, address=(ip, 5020))

def dbServer():
    # start server thread
    sThread = ServerThread(1, 'ServerThread')
    sThread.start()

    # start client on the main thread, client will interact with the server
    client = ModbusClient(ip, port=5020)
    # connect the client to the server
    client.connect()

    cThread = ClientThread(2, 'ClientThread', client)
    cThread.start()

    userIn = input("Enter exit to quit, client and server running in background: ")
    while(userIn.lower() != "exit"):
        userIn = input("Enter exit to quit, client and server running in background: ")

    # join thread, close client connection
    cThread.join()
    client.close()
    sThread.join()

    print("Exiting Main Thread")

if __name__ == "__main__":
    dbServer()
