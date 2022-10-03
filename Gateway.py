from threading import Thread, Timer, get_ident
import message_pb2
from random import *
from SendUDP import SendUDP
from ReceiveUDP import ReceiveUDP
from ReceiveTCP import ReceiveTCP

class Gateway(Thread):

    def __init__(self, s_udp_host, s_udp_port, s_tcp_host, s_tcp_port, disp_host, disp_port):
        Thread.__init__(self)
        self.lista = []
        self.server_udp_host = s_udp_host
        self.server_udp_port = s_udp_port
        self.server_tcp_host = s_tcp_host
        self.server_tcp_port = s_tcp_port
        self.disp_host = disp_host
        self.disp_port = disp_port

    def descobrir(self):
        print("Descobrindo dispositivos...")
        del self.lista[:]
        snd = SendUDP(self.disp_host, self.disp_port)
        msg = message_pb2.GatewayDispositivo()
        msg.tipo = message_pb2.GatewayDispositivo.Tipo.DESCOBERTA
        snd.send(msg.SerializeToString())
        t = Timer(randint(20,70)*0.02,self.descobrir)
        t.start()

    def iniciar(self):
        self.udp_receiver.start()
        self.tcp_receiver.start()
        self.descobrir()

    def run(self):
        self.server_id = str(get_ident())
        self.udp_receiver = ReceiveUDP(self.server_udp_host,self.server_udp_port,self.disp_host,self.disp_port,self.server_id,self.lista)
        self.tcp_receiver = ReceiveTCP(self.server_tcp_host,self.server_tcp_port,self.server_udp_host,self.server_udp_port,self.disp_host,self.disp_port,self.server_id,self.lista)
        self.iniciar()


