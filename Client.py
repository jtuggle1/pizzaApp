import json
import socket
import jsonFunctions as j
import sys

#connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    host = sys.argv[1]
    port = sys.argv[2]
except:
    host = 'localhost'
    port = 65432

client.connect((host, port))

#get JSON data from server
toppingData = j.receive_json(client)
pizzaData = j.receive_json(client)
pc = int(pizzaData["PizzaCount"])

#the connection will stay open until the user ends the session
connOpen = True
while connOpen:

    role = input("Are you the store owner or the pizza chef? 'o' for owner, 'c' for chef, 'q' to close connection: ").lower()

    #all functions allocated to chef

    #helper function for list pizzas.concatenates list into string
    def lphelper(l):
        s = ""
        if not l:
            return ""
        for i in l:
            s = s + i + " "
        return s[:-1]

    #list all existing pizzas
    def listPizzas():
        for i, j in pizzaData.items():
            if i != "PizzaCount":
                a = lphelper(j).lower()
                if a != "":
                    print(f"{i} has {a} for toppings. \n")
                else:
                    print(f"{i} has no toppings. \n")
            else:
                continue

    #gather all requested toppings to add to pizza
    def pizzaToppingsList():
        a = "d"
        l = []
        while (a != "q"):
            a = input("Please enter toppings for pizza. Enter 'q' to stop adding toppings: ").lower()
            if a in toppingData and a not in l and int(toppingData[a]) > 0:
                toppingData[a] = str(int(toppingData[a]) - 1)
                l.append(a)
            elif a == 'q':
                continue
            else:
                print("Topping is not available. Please choose another topping.")
        return l

    #create pizza (will automatically be named based on pizza counter's current position)
    def createPizza(l):
        global pc
        if l not in pizzaData.values():
            pc = pc + 1
            n = "Pizza" + str(pc)
            pizzaData[n] = l
        else:
            print("No duplicate pizzas!")

    #delete pizza
    def delPizza(p):
        try:
            del pizzaData[p]
        except:
            print("Pizza already does not exist.")

    #adding toppings to existing pizza
    def updateAdd():
        p = input("Which pizza would you like to add toppings to? ").lower()
        if p in pizzaData:
            l1 = pizzaData[p]
            l2 = pizzaToppingsList()
            for x in l2:
                if x in l1:
                    toppingData[x] = str(int(toppingData[x]) + 1)
                else:
                    l1.append(x)
            pizzaData[p] = l1
        else:
            print("Please enter an existing pizza!")

    #removing toppings from existing pizza
    def updateRemove():
        p = input("Which pizza would you like to remove toppings from? ").lower()
        if p in pizzaData:
            c = "d"
            l = pizzaData[p]
            while c != "q":
                print(f"The toppings on this pizza are {l}")
                c = input("Which would you like to remove? enter 'q' to stop").lower()
                if c in l:
                    l.remove(c)
                    toppingData[c] = str(int(toppingData[c]) + 1)
                else:
                    print("Please enter an existing topping")
            pizzaData[p] = l

        else:
            print("Please enter an existing pizza!")

    #all functions allocated to store owner

    #List out all available toppings
    def availableToppings():
        for i, j in toppingData.items():
            print(f"There are {j} {i} available")

    #add toppings to stock
    def addToppings(k, v):
        if k not in toppingData:
            toppingData[k] = v
        else:
            c = toppingData[k]
            toppingData[k] = str(int(c) + int(v))

        if int(toppingData[k]) <= 0:
            deleteTopping(k)


    #delete topping from stock
    def deleteTopping(t):
        del toppingData[t]

    #chef role
    if role == 'c':
        choice = "s"

        while choice != "q":
            choice = input("'l' for all existing pizzas, 'c' to create a pizza, 'd' to delete a pizza, 'u' to update a "
                           "pizza, 'q' to quit: ").lower()
            match choice:
                case 'l':
                    listPizzas()
                case 'c':
                    l = pizzaToppingsList()
                    createPizza(l)
                case 'd':
                    t = input("What pizza would you like to delete? ").lower()
                    delPizza(t)
                case 'u':
                    k = input("Would you like to add or remove toppings from a pizza? choose 'a' or 'r': ").lower()
                    if k == 'a':
                        updateAdd()
                    elif k == 'r':
                        updateRemove()

    # owner role
    elif role == 'o':
        choice = "s"

        while choice != "q":
            choice = input(
                "'l' for all available toppings, 'a' to add a topping, 'd' to delete a topping, 'u' to update a "
                "topping, 'q' to quit: ").lower()
            match choice:
                case 'l':
                    availableToppings()
                case 'a':
                    k = input("What topping would you like to add? ").lower()
                    v = input("How many would you like to add? ")
                    #add isdigit checks everywhere
                    if v.isdigit():
                        addToppings(k, v)
                    else:
                        print("Please enter a valid value.")
                case 'd':
                    t = input("What topping would you like to delete? ")
                    deleteTopping(t)
                case 'u':
                    k = input("What topping would you like to update? ")
                    if k in toppingData.keys():
                        v = input("How many would you like to add or remove? Use negative number to remove: ")
                        if v.isdigit():
                            addToppings(k, v)
                        else:
                            print("Please enter a valid value.")
                    else:
                        print("That is not an existing topping; Please consider adding it! ")

    #quitting session
    elif role == 'q':
        print("Goodbye.")
        connOpen = False

#sending json data back to server once session is over
pizzaData["PizzaCount"] = pc
j.send_json(client, toppingData)
j.send_json(client, pizzaData)

#close connection
client.close()
