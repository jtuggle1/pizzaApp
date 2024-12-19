import json
import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 65432))
server.listen(1)


#declaring global variables; these will both be based on the server's local JSON files
pizzaData = {}
toppingData = {}

#call this function to keep accurate data in the respective files
def jsonRefresh():
    global pizzaData
    global toppingData
    with open("CurrentPizzas.json","r") as f:
        pizzaData = json.load(f)
    with open("ToppingStock.json","r") as j:
        toppingData = json.load(j)

jsonRefresh()
print(pizzaData['PizzaCount'])

conn, addr = server.accept()
data = conn.recv(1024)
pizzaData['PizzaCount'] = data.decode()
with open("CurrentPizzas.json", "w") as file:
    json.dump(pizzaData, file, indent=4)
print(pizzaData['PizzaCount'])
#print(f"Received: {data.decode()}")
conn.close()