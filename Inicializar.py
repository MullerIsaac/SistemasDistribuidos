import config as config
from Gateway import Gateway
from criarDispositivos import criarDispositivos

gateway = Gateway(config.server_udp_host,config.server_udp_port,config.server_tcp_host,config.server_tcp_port,config.disp_host,config.disp_port)

gateway.start()

criarDispositivos(config.disp_host,config.disp_port,config.server_udp_host,config.server_udp_port)