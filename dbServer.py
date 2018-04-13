#!/usr/bin/env python
# pymodbus synchronus server
# this will act as the modbus server, will store data sent to it

from pymodbus.server.sync import StartTcpServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer

def dbServer():
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

    # start the TCP server
    StartTcpServer(context, identity=identity, address=("localhost", 5020))

if __name__ == "__main__":
    dbServer()
