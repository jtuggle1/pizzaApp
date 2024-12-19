import json
import socket

tes = input("how many pizzas are currently created?")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 65432))
client.sendall(tes.encode())
client.close()


