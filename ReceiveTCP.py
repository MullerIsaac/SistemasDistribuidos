import socket
from threading import Thread
from TCPHandler import TCPHandler

class ReceiveTCP(Thread):
    def __init__(self,s_tcp_host,s_tcp_port,s_udp_host,s_udp_port,disp_host,disp_port,s_id,lista):
        Thread.__init__(self)
        self.server_tcp_host = s_tcp_host
        self.server_tcp_port = s_tcp_port
        self.server_udp_host = s_udp_host
        self.server_udp_port = s_udp_port
        self.disp_host = disp_host
        self.disp_port = disp_port
        self.server_id = s_id
        self.lista = lista
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def receive(self):
        print("Aguardando conexões")

        try:
            self.socket.bind((self.server_tcp_host, self.server_tcp_port))
            self.socket.listen()
            print("Socket TCP criado")
        except OSError:
            print("Erro na criação do scoket")
        
        while True:
            try:
                conn, addr = self.socket.accept()
                handler = TCPHandler(self.disp_host, self.disp_port, self.server_udp_host, self.server_udp_port, conn, self.server_id, self.lista)
                handler.start()
            except InterruptedError:
                print("Conexão Interrompida")

    def run(self):
        self.receive()

