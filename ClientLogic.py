import json
import socket
import jsonFunctions as j

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 65432))

#get JSON data from server

toppingData = j.receive_json(client)
pizzaData = j.receive_json(client)






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

def deleteTopping(t):
    del toppingData[t]



choice = "s"

while choice != "q":
    choice = input("'l' for all available toppings, 'a' to add a topping, 'd' to delete a topping, 'u' to update a "
                   "topping, 'q' to quit")
    match choice:
        case 'l':
            availableToppings()
        case 'a':
            k = input("What topping would you like to add?")
            v = input("How many would you like to add?")
            addToppings(k, v)
        case 'd':
            t = input("What topping would you like to delete?")
            deleteTopping(t)
        case 'u':
            k = input("What topping would you like to update?")
            v = input("How many would you like to add?")
            addToppings(k, v)





j.send_json(client, toppingData)

j.send_json(client, pizzaData)



client.close()
