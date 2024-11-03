import socket,threading

port_no="33000"         #port number on server where connection occurs

def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)         #setting up TCP stream
    
    #binding server to port and dynamic ip address (based on client i/p)
    server.bind('',port_no)     
    server.listen(2)    #queue  
    print("Server started listening at {}::{}".format(*server.getsockname()))

    while True:
        clent_port,client_addr=server.accept()


if _name_ == "_main_":
    main()