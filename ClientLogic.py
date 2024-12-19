import json
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 65432))


#get JSON data from server

serverData = client.recv(1024).decode()
toppingData = json.loads(serverData)

print(toppingData)

#all functions related to toppings

def availableToppings():
    for i, j in toppingData.items():
        print(f"There are {j} {i} available")

def addToppings(k, v):
    if toppingData[k] is None:
        toppingData[k] = v
    else:
        c = toppingData[k]
        toppingData[k] = str(int(c) + int(v))

#all functions related to pizza creation
choice = input("at, ad,")

match choice:
    case 'at':
        availableToppings()
    case 'ad':
        k = input("What topping would you like to add?")
        v = input("How many would you like to add?")
        addToppings(k, v)


print(toppingData)

json_data = json.dumps(toppingData)


client.sendall(json_data.encode())


















#client.sendall(tes.encode())
client.close()


