import message_pb2
import socket
import config as config

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((config.server_tcp_host, config.server_tcp_port))

message = message_pb2.Request()
message.tipo = message_pb2.Request.Tipo.DESCOBERTA

client.sendall(message.SerializeToString())

print("Mensagem enviada")

msg = client.recv(4096)

print("Mensagem Recebida")

response = message_pb2.Response()
response.ParseFromString(msg)
print(response.dispositivos)

client.close()
