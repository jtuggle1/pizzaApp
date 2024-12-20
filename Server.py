import json
import socket
import jsonFunctions as j

while True:
    try:
        #server listening
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 65432))
        server.listen(1)

        #declaring global variables; these will both be based on the server's local JSON files
        pizzaData = {}
        toppingData = {}


        #json data is pulled from local logs
        def jsonRefresh():
            global pizzaData
            global toppingData
            with open("CurrentPizzas.json", "r") as f:
                pizzaData = json.load(f)
            with open("ToppingStock.json", "r") as j:
                toppingData = json.load(j)

        #connection is accepted and json data is transferred to client
        conn, addr = server.accept()

        jsonRefresh()
        j.send_json(conn,toppingData)
        j.send_json(conn,pizzaData)

        #recieving json data from client session
        toppingData = j.receive_json(conn)
        with open("ToppingStock.json", "w") as file:
            json.dump(toppingData, file, indent=4)

        pizzaData = j.receive_json(conn)
        with open("CurrentPizzas.json", "w") as file:
            json.dump(pizzaData, file, indent=4)

        #closing connection
        conn.close()
    except:
        print("An error occurred")