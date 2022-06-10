# ResponseCodeHandler.py
#
# This is the Reponse Code Handler which handles the servers responses and codes. 
# It logs all the responses to the client and will break out of the main loop if recieved certain response codes. 
# Will also sometimes give prompts to user for certain responses


from Client import Client


def recieveResponse(client):
    response = client.getSocket().recv(4096)
    r = response.decode()
    client.appendLogFile("Recieved: " + r)
    return r

def parseResponseCodes(response, client):
    code = response.split()[0]

    # Definition : File status ok, about to open data connection
    # Action : None. 
    if (code == "150"):
        None
    # Definition : NAME system type
    # Action : None.
    elif (code == "215"):
        return True

    # Definition: Service ready for new user
    # Action: Send username
    elif (code == "220"):
        None
        print("Send username:")

    # Definition : Goodbye
    # Action : End loop
    elif (code == "221"):
        print("Closing connection...")
        None
        return False

    # Definition : Closing data connection. Requested file action successful
    # Action : None.
    elif (code == "226"):
        None

    # Definition : Entering passive mode
    # Action : Return address and port to connect to
    elif (code == "227"):
        None
        return response

    # Definition: Login Successful
    # Action: Call input function
    elif (code == "230"):
        None

    # Definition : Requested file action okay, completed
    # Action : None. Ask for another command
    elif (code == "250"):
        None

    # Definition : "PATHNAME" created
    # Action : None. Ask for input
    elif (code == "257"):
        None
    
    # Definition: Username ok, need password
    # Action: Send password
    elif (code == "331"):
        print("Send password:")

    # Definition : Service not availible
    # Action : None. Ask for input
    elif(code == "421"):
        None

    # Definition : Can't open data connection
    # Action : None. Ask for input
    elif(code == "425"):
        None

    # Definition: Unknown command
    # Action: Print error message
    elif(code == "500"):
        print("Unrecognized command.\nType 'Help' for list's of availible commands.")

    # Definition: Login incorrect
    # Action: Terminate Program
    elif (code == "530"):
        return False

    # Definition : Failed to change directory
    # Action : None
    elif (code == "550"):
        None

    else:
        print("Unrecognized response code\nTerminating connection")
        client.sendQUIT()
        return False