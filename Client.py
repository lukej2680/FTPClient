# CLient.py
#
# This is the Client class module used to create a client object in order to pass to the command and response code handlers
# This classe depends on the socket and datetime modules
# It's purpose is to hold information regarding the specific client connection, such as local ip's, logfile name, extended mode and whether to use a passive or active connection
# This class is responsible for directly sending all commands to the server. The logic is defined in CommandHandler.py
# This class isolates the log file to the specific instance of the class having methods to create and append the logfile

import socket
import datetime


class Client:
    ipv4 = None
    ipv6 = None
    extended = False
    passive = False
    logfile_name = "FtpClientv2_log.txt"

    def __init__(self, socket):
        self.socket = socket  
        self.ipv4 = self._setIPv4()      

    def sendUSER(self, username):
        send_cmd = "USER " + username + "\r\n"
        self.socket.sendall(send_cmd.encode())
        self.appendLogFile("Sent: " + send_cmd)

    def sendPASS(self, password):
        send_cmd = "PASS " + password + "\r\n"
        self.socket.sendall(send_cmd.encode())
        self.appendLogFile("Sent: " + send_cmd)

    def sendPWD(self):
        send_cmd = "PWD\r\n"
        self.socket.sendall(send_cmd.encode())
        self.appendLogFile("Sent: " + send_cmd)

    def sendCWD(self, directory):
        send_cmd = "CWD " + directory + "\r\n"
        self.socket.sendall(send_cmd.encode())
        self.appendLogFile("Sent: " + send_cmd)

    def sendLIST(self):
        send_cmd = "LIST\r\n"
        self.socket.sendall(send_cmd.encode())
        self.appendLogFile("Sent: " + send_cmd)

    def sendPORT(self, port):
        a, b, c, d = self.ipv4.split('.')
        send_cmd = "PORT ("+a+","+b+","+c+","+d+","+"200,108)\r\n"
        self.socket.sendall(send_cmd.encode())

    def sendEPRT(self):
        send_cmd = "EPSV\r\n"
        self.socket.sendall(send_cmd.encode())
        self.appendLogFile("Sent: " + send_cmd)

    def sendPASV(self):
        send_cmd = "PASV\r\n"
        self.socket.sendall(send_cmd.encode())
        self.appendLogFile("Sent: " + send_cmd)

    def sendEPSV(self):
        None
    
    def sendRETR(self, file_name):
        send_cmd = "RETR " + file_name + "\r\n"
        self.socket.sendall(send_cmd.encode())
        self.appendLogFile("Sent: " + send_cmd)

    def sendSTOR(self, file_name):
        send_cmd = "STOR " + file_name + "\r\n"
        self.socket.sendall(send_cmd.encode())
        self.appendLogFile("Sent: " + send_cmd)

    def sendSYST(self):
        send_cmd = "SYST\r\n"
        self.socket.sendall(send_cmd.encode())
        self.appendLogFile("Sent: " + send_cmd)

    def sendQUIT(self):
        send_cmd = "QUIT\r\n"
        self.socket.sendall(send_cmd.encode())
        self.appendLogFile("Sent: " + send_cmd)

    def getSocket(self):
        return self.socket
        
    def _setIPv4(self):
        return self.socket.getsockname()[0]

    def getIPv4(self):
        return self.ipv4

    def setExtendedMode(self):
        self.extended = True
        self.appendLogFile("Entering Extended Mode")

    def getExtended(self):
        return self.extended

    def createLogFile(self, logfile_name):
        self.logfile_name = logfile_name
        logfile = open(self.logfile_name, 'w')
        logfile.write('FtpClientv2 Logfile:\n')
        logfile.close()

    def appendLogFile(self, log):
        logfile = open(self.logfile_name, 'a')
        logfile.write(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        logfile.write(' ' + log + '\n')
        logfile.close()

    def setPassiveMode(self):
        self.passive = True
        self.appendLogFile("Entering Passive Mode")

    def getPassive(self):
        return self.passive
