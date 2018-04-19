# ModdingTheBus
A very simple implementation of the pymodbus library.

**Note: the default implementation is designed to run on the localhost. Please
change the address in each file if you wish to run it on a different address.**

## Setting it up
Ensure you have the pymodbus library installed. These programs were tested in
python 2 not python 3.
1. Start the server: `python endPointServer.py`
3. Start the client, ie `python mgmtClient.py`
4. Enter values into the window running the mgmtClient and the server will read them in.

**Note: the server is to be run on the device you wish to control. The client is what controls the server. This is per the modbus protocol where the slaves store data.**
