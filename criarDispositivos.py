from SensorTemperatura import SensorTemperatura

def criarDispositivos(disp_host,disp_port,server_host,server_port):

    lista = [
            SensorTemperatura(disp_host,disp_port,server_host,server_port,{},"Sensor_Temperatura_1"),
            ]

    for i in range(0,len(lista)):
        lista[i].start()