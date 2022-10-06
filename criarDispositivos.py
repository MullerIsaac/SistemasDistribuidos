from SensorTemperatura import SensorTemperatura
from ArCondicionado import ArCondicionado

def criarDispositivos(disp_host,disp_port,server_host,server_port):

    lista = [
            SensorTemperatura(disp_host,disp_port,server_host,server_port,{},"Sensor_Temperatura_1"),
            ArCondicionado(disp_host,disp_port,server_host,server_port,{},"Ar_Condicionado")
            ]

    for i in range(0,len(lista)):
        lista[i].start()