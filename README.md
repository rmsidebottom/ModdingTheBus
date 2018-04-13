# ModdingTheBus
A very simple implementation of the pymodbus library.

**Note: the default implementation is designed to run on the localhost. Please
change the address in each file if you wish to run it on a different address.**

## Setting it up
Ensure you have the pymodbus library installed. These programs were tested in
python 2 not python 3.
1. Start the server: `python dbServer.py`
2. Start either client, ie `python endpointClient.py`
3. Start the other client, ie `python mgmtClient.py`
4. Enter values into the window running the mgmtClient and the endpointClient
will read these in.
