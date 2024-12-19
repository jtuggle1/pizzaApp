import json
import socket
import jsonFunctions as j

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
    with open("CurrentPizzas.json", "r") as f:
        pizzaData = json.load(f)
    with open("ToppingStock.json", "r") as j:
        toppingData = json.load(j)


conn, addr = server.accept()
jsonRefresh()
j.send_json(conn,toppingData)
j.send_json(conn,pizzaData)




toppingData = j.receive_json(conn)
with open("ToppingStock.json", "w") as file:
    json.dump(toppingData, file, indent=4)

pizzaData = j.receive_json(conn)
with open("CurrentPizzas.json", "w") as file:
    json.dump(pizzaData, file, indent=4)


conn.close()
