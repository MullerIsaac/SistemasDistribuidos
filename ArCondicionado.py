from Dispositivo import Dispositivo
from threading import Thread, get_ident, Timer
from DispUDP import DispUDP
from SendUDP import SendUDP
import message_pb2
from random import *

class ArCondicionado(Dispositivo,Thread):

    def __init__(self,disp_host,disp_port,server_host,server_port,dict,nome):
        Dispositivo.__init__(self,dict,nome)
        Thread.__init__(self)
        self.disp_host = disp_host
        self.disp_port = disp_port
        self.server_host = server_host
        self.server_port = server_port
        ops = {
            'ler_temperatura' :  str(randint(0,30))+' C',
        }
        self.addDictOp(ops)   

    def anunciar(self):
        print("Anunciando "+self.nome+"...")
        snd = SendUDP(self.server_host,self.server_port)
        msg = message_pb2.GatewayDispositivo()
        msg.tipo = message_pb2.GatewayDispositivo.Tipo.ANUNCIO
        disp = message_pb2.Dispositivo()
        disp.id = self.id
        disp.nome = self.nome
        disp.operacoes.extend(self.getOps())
        msg.dispositivo.CopyFrom(disp)
        snd.send(msg.SerializeToString())

    def run(self):
        print("Iniciando dispositivo "+self.nome+" ...")
        self.id = str(get_ident())
        self.udp_receiver = DispUDP(self.disp_host,self.disp_port,self.server_host,self.server_port,self.id,self.getDict(),self.nome)
        self.udp_receiver.start()
        self.anunciar()