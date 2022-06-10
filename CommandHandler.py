# CommandHandler.py
#
# This is the Command Handler that will handle user input along with the logic and flow behind sending each command such as setting up the data connection and telling the client to send commands on the control connection
# The handlder depends on the ResponseCodeHandler in order to parse the response and response codes to respond appropiatly. 

import ReponseCodeHandler
import socket


# Set up the data connection in passive mode
# The connection information sent back from the FTP server is passed into this function
def passiveDataConnection(data, client):
    # Check if client is in extended mode (ipv4 vs ipv6)
    if (client.getExtended()):
        print("Not implemented.")
    else:
        # Client is not in extended mode

        # Expecting to be passed data of form "227 Entering Passive Mode (10,246,251,93,110,21)."
        # Parse data to get ip values and port number
        a, b, c, d, e, f = data.split()[4].replace("(", "").replace(")", "").replace(".", "").split(",")

        # Join ip values to create ipv4 address
        ip = ".".join([a, b, c, d])
        # Use (p1 * 256) + p2 formula to get port number
        port = (int(e) * 256) + int(f)

        # Create the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to ftp server
        sock.connect((ip, port))
        client.appendLogFile("Passive data connection to " + ip + " on port " + str(port))

        # Return the socket for use
        return sock


def activeDataConnection(port, client):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket Established")

    sock.bind((client.getIPv4(), port))
    print("Listening" + '' + " on port " + str(port))

    sock.listen(1)

    return sock


def ftpInput(client):
    # Create loop to contiounsly ask for input until a valid command is sent 
    while True:
        cmd_input = input("ftp> ").split()
        cmd = cmd_input[0].lower()

        # Command of help will print the menu of acceptable commands for this client
        if (cmd == "help"):
            print("ftp> help                      : Prints the help menu\n" +
                    "ftp> user <username>           : Sends username\n" +
                    "ftp> pass <password>           : Sends password\n" +             
                    "ftp> pwd                       : Displays current directory\n"
                    "ftp> cwd <directory path>      : Changes working directory to specified path\n" +
                    "ftp> list                      : Lists the directory contents\n" +
                    "ftp> download <filename>       : downloads file\n" +
                    "ftp> upload <filename>         : Uploads file\n"
                    "ftp> extended                  : Use IPv6\n" +
                    "ftp> passive                   : Enter passive mode\n" +
                    "ftp> system                    : Retrieve information of the server\n" +
                    "ftp> quit                      : Closes connection and exits program\n")
        
        # USER command sends username
        elif (cmd == "user"):
            if (len(cmd_input) != 2):
                print("Specify username\nftp> user <username>           : Changes user\n")
            else:
                username = cmd_input[1]
                client.sendUSER(username)
                break

        # PASS command sends password
        elif (cmd == "pass"):
            if (len(cmd_input) != 2):
                print("Specify password\nftp> pass <password>           : Sends password\n")
            else:
                password = cmd_input[1]
                client.sendPASS(password)
                break

        # PWD command displays the current working directory
        elif (cmd == "pwd"):
            client.sendPWD()
            break

        # CWD changes working directory
        elif (cmd == "cwd"):
            if (len(cmd_input) != 2):
                print("Specify directory path\nftp> cwd <directory path>      : Changes working directory to specified path\n")
            else:
                directory = cmd_input[1]
                client.sendCWD(directory)
                break

        # LIST prints the directory listing
        elif (cmd == "list"):
            # Checks if client in passive mode
            if (client.getPassive()):
                # Client sends PASV command and captures server response in data variable
                client.sendPASV()
                data = ReponseCodeHandler.recieveResponse(client)
                # Check for 227 response code
                if (data.split()[0] == "227"):
                    # Create passive data connection
                    passive_sock = passiveDataConnection(data, client)

                    client.sendLIST()

                    response = passive_sock.recv(4096)
                    r = response.decode()
                    print(r)
                    client.appendLogFile("Recieved: Directory Listings")

                    print(ReponseCodeHandler.recieveResponse(client))

                    passive_sock.close()
                # if not 227, send to handler to handle
                else:
                    ReponseCodeHandler.parseResponseCodes(data, client)
            # else create an active connection with the server
            else:
                print("Active connection is not set up for this client")
                ftpInput(client)
            break
        
        # DOWNLOAD downloads specified file onto client
        elif (cmd == "download"):
            if (len(cmd_input) != 2):
                print("Specify file name\nftp> download <filename>       : downloads file\n")
            else:
                # Checks for passive mode
                if (client.getPassive()):
                    # Client sends PASV and if successful creates a passive data connection
                    # If unseccessful sends to handler to handle
                    client.sendPASV()
                    data = ReponseCodeHandler.recieveResponse(client)
                    if (data.split()[0] == "227"):
                        passive_sock = passiveDataConnection(data, client)
                        client.sendRETR(cmd_input[1])

                        r = ReponseCodeHandler.recieveResponse(client)
                        
                        # Once open for data transfer open file for writing recieved data too
                        if (r.split()[0] == "150"):
                            f = open(cmd_input[1], "w")
                            while True:
                                d = passive_sock.recv(4096)
                                f.write(d.decode())
                                if not d:
                                    break
                            f.close()

                            #print(ReponseCodeHandler.recieveResponse(client))

                            passive_sock.close()
                        else:
                            ReponseCodeHandler.parseResponseCodes(r, client)
                    else:
                        ReponseCodeHandler.parseResponseCodes(data, client)
                # else create active server connection
                else:
                    print("Active connection is not set up for this client")
                    ftpInput(client)
                break

        # UPLOAD will upload specified file
        elif (cmd == "upload"):
            if (len(cmd_input) != 2):
                print("Specify file name\nftp> upload <filename>         : Uploads file\n")
            else:
                # Checks for passive mode
                if (client.getPassive()):
                    if (client.getExtended()):
                        client.sendEPSV()
                    else:
                        client.sendPASV()
                    data = ReponseCodeHandler.recieveResponse(client)
                    if (data.split()[0] == "227"):
                        passive_sock = passiveDataConnection(data, client)
                        try:
                            f = open(cmd_input[1], "rb")
                            
                            client.sendSTOR(cmd_input[1])

                            print(ReponseCodeHandler.recieveResponse(client))

                            if (r.split()[0] == "150"):
                                while True:
                                    bytes_read = f.read(4096)
                                    if not bytes_read:
                                        break
                                    passive_sock.sendall(bytes_read)
                                f.close()
                                passive_sock.close()

                                print(ReponseCodeHandler.recieveResponse(client))
                            else:
                                ReponseCodeHandler.parseResponseCodes(r, client)
                        except:
                            print("File cannot be opened")
                            passive_sock.close()
                    else:
                        ReponseCodeHandler.parseResponseCodes(data, client)
                else:
                    print("Active connection is not set up for this client")
                    ftpInput(client)

        # PASSIVE will make all future connections passive
        elif (cmd == "passive"):
            print("Passive mode enabled")
            client.setPassiveMode()
            ftpInput(client)
            break

        # EXTENDED command sets extended mode
        elif (cmd == "extended"):
            print("IPv6 routing not enabled")
            #print("Extended mode enabled")
            #client.setExtendedMode()
            ftpInput(client)
            break

        # SYSTEM retireves information of the system
        elif (cmd == "system"):
            client.sendSYST()
            break

        # QUIT quits program
        elif (cmd == "quit"):
            client.sendQUIT()
            break

        # All invalid commands 
        else:
            print("Invalid command")
