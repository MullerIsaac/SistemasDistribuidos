import socket
import struct
import datetime
from SendUDP import SendUDP
from threading import Thread, get_ident, Timer
import message_pb2
import sys
from random import *

class DispUDP(Thread):

    def __init__(self,disp_host,disp_port,server_host,server_port,id,ops,nome,is_continuo = False):
        Thread.__init__(self)
        self.disp_host = disp_host
        self.disp_port = disp_port
        self.server_host = server_host
        self.server_port = server_port
        self.id = id
        self.ops = ops
        self.nome = nome
        self.is_continuo = is_continuo
        self.disponivel = True
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)

    def configurar(self):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.disp_host, self.disp_port))
            print("Socket DispUDP criado")
        except OSError:
            print("Erro na criação do socket. Verifique se a porta DispUDP"+str(self.disp_port)+" já está sendo utilizada")
        try:
            group = socket.inet_aton(self.disp_host)
            mreq = struct.pack("4sl",group,socket.INADDR_ANY)
            self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except OSError:
            print("Endereço de host inválido. Verifique se o formato está correto")
            sys.exit()

    def sumir(self):
        print("Sumindo...")
        self.disponivel = False
        t = Timer(randint(50,100)*0.5,self.aparecer)
        t.start()

    def aparecer(self):
        print("Aparecendo...")
        self.disponivel = True
        t = Timer(randint(50,100)*0.5,self.sumir)
        t.start()

    def receive(self):

        self.configurar()

        while True:
                try:
                    msg, addr = self.socket.recvfrom(1024)
                except InterruptedError:
                    print("Execução interrompida")
                else:
                    try:

                        # Desfaz a serialização da mensagem
                        ret = message_pb2.GatewayDispositivo()
                        ret.ParseFromString(msg)

                        # Checa se é do tipo DESCOBERTA
                        if( ret.tipo == message_pb2.GatewayDispositivo.Tipo.DESCOBERTA ):
                            if(self.disponivel == True):
                                # Constroi e envia a mensagem de resposta
                                response = message_pb2.GatewayDispositivo()
                                response.tipo = message_pb2.GatewayDispositivo.Tipo.DISPOSITIVO
                                disp = message_pb2.Dispositivo()
                                disp.nome = self.nome
                                disp.id = self.id
                                disp.operacoes.extend(self.ops)
                                response.dispositivo.CopyFrom(disp)
                                snd = SendUDP(self.server_host,self.server_port)
                                snd.send(response.SerializeToString())
                        # Checa se é do tipo OPERACAO
                        elif( ret.tipo == message_pb2.GatewayDispositivo.Tipo.OPERACAO ):
                            if( ret.id_dispositivo == self.id ):
                                # Constroi e envia a mensagem de resposta
                                response = message_pb2.GatewayDispositivo()
                                response.tipo = message_pb2.GatewayDispositivo.Tipo.RESPOSTA
                                response.id_dispositivo = ret.id_dispositivo
                                response.operacao = ret.operacao
                                response.resposta = "Erro: operação inexistente"
                                if(self.disponivel == True):
                                    for i in range(0,len(self.ops.keys())):
                                        if(list(self.ops.keys())[i] == ret.operacao):
                                            response.resposta = self.ops[list(self.ops.keys())[i]]
                                print(str(self.id)+" recebendo requisição:")
                                print("    operação: "+str(ret.operacao))
                                print("    resultado: "+str(response.resposta))
                                snd = SendUDP(self.server_host,self.server_port)
                                snd.send(response.SerializeToString())
                    except PermissionError:
                        print("Erro: permissão de acesso ao arquivo negada")



    def run(self):
        if(self.is_continuo == False):
            t = Timer(randint(50,100)*0.5,self.sumir)
            t.start()
        print("Tentando criar o DispDUP")
        self.receive()