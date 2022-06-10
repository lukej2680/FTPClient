# FtpClientv2.py
#
# This is the main client program for the ftp client
# Dependencies;
#   Client.py
#   Commandhandler.py
#   ResponseCodeHandler.py

# import required modules
import sys, argparse, socket
from Client import Client
import ReponseCodeHandler
import CommandHandler

if (len(sys.argv) < 3):
    print("Missing Arguments")
    exit(1)
ip = sys.argv[1]
logfile = sys.argv[2]
if (len(sys.argv) > 3):
    port = sys.argv[3]
else:
    port = 21
print(ip, logfile, port)

# Create the control socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Established")

# Create the client object
client = Client(sock)

# Set the log file
client.createLogFile(logfile)
try:
    client.getSocket().connect((ip, port))
    client.appendLogFile("Connected to " + ip + " on port " + str(port))
except:
    client.appendLogFile("Error: Exiting program")
    client.getSocket().close()
    print("Error exiting program")
    exit(1)

r = ReponseCodeHandler.recieveResponse(client)
print(r)

while True:
    if (ReponseCodeHandler.parseResponseCodes(r, client) == False): break
    else: CommandHandler.ftpInput(client)

    r = ReponseCodeHandler.recieveResponse(client)
    print(r)

client.getSocket().close()
client.appendLogFile("Connection closed.")
