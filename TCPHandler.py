from threading import Thread,get_ident
import message_pb2
from SendWaitUDP import SendWaitUDP
from SendUDP import SendUDP
import socket

class TCPHandler(Thread):

    def __init__(self,disp_host,disp_port,server_host,server_port,conn,server_id,lista):
        Thread.__init__(self)
        self.conn = conn
        self.disp_host = disp_host
        self.disp_port = disp_port
        self.server_host = server_host
        self.server_port = server_port
        self.server_id = server_id
        self.lista = lista

    def handleMsg(self):

        try:
            data = self.conn.recv(4096)
        except InterruptedError:
            print("Conexão interrompida")
        try:
            mensagem = message_pb2.GatewayClient()
            mensagem.ParseFromString(data)
            try:
                if(mensagem.tipo == message_pb2.GatewayClient.Tipo.DESCOBERTA):
                    # Manda mensagem UDP multicast para grupo de dispositivos
                    response = message_pb2.GatewayClient()
                    print("Lista de dispositivos: "+str(self.lista))
                    response.tipo = message_pb2.GatewayClient.Tipo.DISPOSITIVOS
                    response.dispositivos.extend(self.lista)
                    self.conn.send(response.SerializeToString())
                elif(mensagem.tipo == message_pb2.GatewayClient.Tipo.OPERACAO):
                    # Manda mensagem UDP multicast para grupo de dispositivo
                    reqmsg = message_pb2.GatewayDispositivo()
                    reqmsg.tipo = message_pb2.GatewayDispositivo.Tipo.OPERACAO
                    reqmsg.id_dispositivo = mensagem.id_dispositivo
                    reqmsg.operacao = mensagem.operacao
                    rcv = SendWaitUDP(self.disp_host,self.disp_port,self.server_host,self.server_port,reqmsg)
                    res = rcv.receive()
                    response = message_pb2.GatewayClient()
                    response.tipo = message_pb2.GatewayClient.Tipo.RESPOSTA
                    response.id_dispositivo = res.id_dispositivo
                    response.resposta = res.resposta
                    self.conn.send(response.SerializeToString())
            except InterruptedError :
                print("Conexão interrompida")
        except PermissionError:
            print("Erro: permissão de acesso ao arquivo negada")

        self.conn.close()

    def run(self):

        self.handleMsg()