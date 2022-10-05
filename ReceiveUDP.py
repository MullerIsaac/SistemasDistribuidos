import socket
import struct
from threading import Thread, get_ident
import message_pb2
import sys

class ReceiveUDP(Thread):

    def __init__(self,server_host,server_port,disp_host,disp_port,server_id,lista):
        Thread.__init__(self)
        self.server_host = server_host
        self.server_port = server_port
        self.disp_host = disp_host
        self.disp_port = disp_port
        self.lista = lista
        self.server_id = server_id
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)

    def configurar(self):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("Antes de dar erro")
            self.socket.bind((self.server_host,self.server_port))
            print("Socket ReceiveUDP criado")
        except OSError:
            print("Erro na criação do socket. Verifique se a porta ReceiveUDP"+str(self.server_port)+" já está sendo utilizada")
        try:
            group = socket.inet_aton(self.server_host)
            mreq = struct.pack("4sl",group,socket.INADDR_ANY)
            self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except OSError:
            print("Endereço de host inválido. Verifique se o formato está correto")
            sys.exit()

    def receive(self):

        self.configurar()

        while True:
            try:
                msg, addr = self.socket.recvfrom(1024)
            except InterruptedError:
                print("Execução interrompida")
            else:
                try:
                    ret = message_pb2.GatewayDispositivo()
                    ret.ParseFromString(msg)
                    if( ret.tipo == message_pb2.GatewayDispositivo.Tipo.ANUNCIO or ret.tipo == message_pb2.GatewayDispositivo.Tipo.DISPOSITIVO ):
                        if( ret.tipo == message_pb2.GatewayDispositivo.Tipo.DISPOSITIVO ):
                            print("Servidor descobrindo dispositivo: "+ret.dispositivo.id)
                        else:
                            print("Servidor recebendo anuncio: "+ret.dispositivo.id)
                        c = False
                        for j in range(0,len(self.lista)):
                            if( self.lista[j].id == ret.dispositivo.id ):
                                c = True
                                break
                        if(c == False):
                            self.lista.append(ret.dispositivo)
                except PermissionError:
                    print("Erro: permissão de acesso ao arquivo negada")



    def run(self):
        print("Tentando criar o ReceiveUDP")
        self.receive()