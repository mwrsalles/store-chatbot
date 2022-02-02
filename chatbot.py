#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Product: #this class is related to each product from the store, it includes the product's name and its price
    def __init__(self, name, price):
        self.name = name
        self.price = price
        

class Stock: #this class is related to the Stock
    #it saves the products added for the store and makes changes according to users' choices
    def __init__(self):
        self.quantity = []
    
    def AddToStock(self, product, quantity):
        self.quantity.append((product, quantity)) 
        
    def RemoveFromStock(self, product, quantity): #this function removes items from the stock when they are added in the cart
        for tuple_p_and_q in self.quantity:
            if product in tuple_p_and_q:
                if tuple_p_and_q[1] - quantity >=0:
                    new_number = tuple_p_and_q[1] - quantity
                    new_tuple = (tuple_p_and_q[0],) + (new_number,)
                    self.quantity.remove(tuple_p_and_q)
                    self.quantity.append(new_tuple)
                    
                    
    def VerifyStock(self, product): #this fuction verifies if there are enough products available to be taken 
        for tuple_p_and_q in self.quantity:
            if product in tuple_p_and_q:    
                return int(tuple_p_and_q[1])

            
            
class Cart: #this class is related to the shopping cart
    #it includes a list if users's products, adds and removes products to the list, show what the user has on their list etc
    def __init__(self):
        self.shopping_list = []
        
    def AddToCart(self, product, clients_quantity, stock):  
        cart_quantity = 0
        if len(self.shopping_list) > 0: 
            for tuple_p_and_q in self.shopping_list:
                if product in tuple_p_and_q:
                    cart_quantity = tuple_p_and_q[1]
                    if stock.VerifyStock(product) >= (clients_quantity + cart_quantity):
                        new_number = tuple_p_and_q[1] + clients_quantity
                        new_tuple = (tuple_p_and_q[0],) + (new_number,)
                        self.shopping_list.remove(tuple_p_and_q) 
                        self.shopping_list.append(new_tuple)
                        stock.RemoveFromStock(new_tuple[0],new_tuple[1]) 
                        return
                    else:
                        print("Not enough products available.")
                else:
                    if stock.VerifyStock(product) >= (clients_quantity):
                        self.shopping_list.append((product,clients_quantity))
                        stock.RemoveFromStock(product,clients_quantity) 
                        return  
                    else:
                        print("Not enough products available.")
        else:
            self.shopping_list.append((product,clients_quantity))
            stock.RemoveFromStock(product,clients_quantity) 
     
            
    def RemoveFromCart(self,product,quantity_to_remove):
        if len(self.shopping_list) == 0:
            print('Empty cart.')
        elif len(self.shopping_list) > 0:
            for tuple_p_and_q in self.shopping_list:
                if product in tuple_p_and_q:
                    if quantity_to_remove <= tuple_p_and_q[1]:
                        new_number = tuple_p_and_q[1] - quantity_to_remove
                        new_tuple = (tuple_p_and_q[0],) + (new_number,)
                        self.shopping_list.remove(tuple_p_and_q)
                        if new_number == 0: 
                            return
                        else:
                            self.shopping_list.append(new_tuple)
                            return
                        stock.AddToStock(product, quantity_to_remove) 
                    else:
                        print('Sorry, could not continue with this operation.') 
                        
    def ShowCart(self): 
        if len(self.shopping_list) > 0:
            for tuple_p_and_q in self.shopping_list:
                if int(tuple_p_and_q[1]) == 1:
                    product = tuple_p_and_q[0].name 
                elif int(tuple_p_and_q[1]) > 1:
                    prod_name = tuple_p_and_q[0].name
                    prod_name = str(prod_name)
                    product = prod_name+"s" 
                num = str(tuple_p_and_q[1])
                print(num, product)     
        else:
            print('Empty cart.')
            
        
    def FinalValue(self, stock): #this fuction shows the final value of the payment bill and closes the cart
        if len(self.shopping_list) == 0:
            print("Empty cart... And now closed!")
        else:
            total = 0
            for tuple_p_and_q in self.shopping_list:
                total += tuple_p_and_q[0].price*tuple_p_and_q[1]
            print("The final cost of your purchase is US", "{0:4.2f}".format(total), ".\
            \nThank you for shopping with us.")
                                  
                
class ChatBot: #this class is related to the Bot, it takes users' answers
    __open_cart = True
    __start_message = print("Welcome to our store!\nHere is a set list of what you can do:")
    def opening_cart(self, cart, stock):
        ChatBot.__open_cart = True 
        while ChatBot.__open_cart:
            print("\n1- add products to your shopping cart\n2- remove products from your shopping cart\
            \n3- see what you have in your shopping cart\n4- close your shopping cart")
            clients_choice = str(input("\nPlease, type the number corresponding to your choice: "))
            if clients_choice == "1" or clients_choice == "2" or clients_choice == "3" or clients_choice == "4":
                clients_choice = int(clients_choice)
                print("\n=====================================================")
            else:
                while clients_choice not in ["1", "2", "3", "4"]:
                    clients_choice = str(input("\nInvalid value!\ 
                    Please, type the number corresponding to your choice: "))
                clients_choice = int(clients_choice)
                print("\n=====================================================")
            
            if clients_choice == 1: #adds products to user's list
                product, quantity = self.ClientChoice(stock) 
                if product and quantity:
                    cart.AddToCart(product,quantity,stock)
                else:
                    print("Error")

                more_products = input('\nWould you like to add something else? Y/N ')
                while more_products != "N":
                    if more_products == "Y":
                        product, quantity = self.ClientChoice(stock)
                        if product and quantity:
                            cart.AddToCart(product,quantity,stock)
                        more_products = input('\nWould you like to add something else? Y/N ')
                    else:
                        while more_products not in ["Y", "N"]:
                            print('I could not understand you. Please, type "Y" for yes or "N" for no!')
                            more_products = input('\nWould you like to add something else? Y/N ')
                print("\n=================================")
                print("\nWhat else would you like to do?") 

            elif clients_choice == 2: #removes products from user's list
                product, quantity = self.ClientChoice(stock)
                if product and quantity:
                    cart.RemoveFromCart(product,quantity)
                else:
                    print("Error")

                more_products = input('\nWould you like to remove something else? Y/N ')
                while more_products != "N":
                    if more_products == "Y":
                        product, quantity = self.ClientChoice(stock)
                        if product and quantity:
                            cart.RemoveFromCart(product,quantity)
                        more_products = input('\nWould you like to add something else? Y/N ')
                    else:
                        while more_products not in ["Y", "N"]:
                            print('I could not understand you. Please, type "Y" for yes or "N" for no!')
                            more_products = input('\nWould you like to remove something else? Y/N ')
                print("\n=================================")
                print("\nWhat else would you like to do?")

                
            elif clients_choice == 3: #show what the user has in their cart
                print("\nThis is what you currently have in your shopping cart:\n")
                cart.ShowCart()
                print("\n=================================")
                print("\nWhat else would you like to do?")
                
            elif clients_choice == 4: #gives the final value and closes cart
                cart.FinalValue(stock)
                ChatBot.__open_cart = False
                

                          
    def ClientChoice(self,stock): #related to choices 1 and 2, takes the product and the quantity wanted by the user
        clients_product = input('Type the product you want to add or remove: ')
        print("\nHow many", str(clients_product).lower()+"s", "would you like to add or remove? ")
        clients_quantity = int(input("Please, only type the number: "))
        product_in_stock=False

        if clients_quantity and clients_product:
            for number in stock.quantity:
                if clients_product.lower() == number[0].name:
                    return number[0],clients_quantity
            if not product_in_stock:
                print ('Product not found.')
                return self.ClientChoice(stock)
            
        else:
            print("Error.")
            return self.ClientChoice(stock)
                        
                          
#here are some products to test the program:
    
testing_product1 = Product("carrot", 0.4)
testing_product2 = Product("cookie", 4.56)
testing_product3 = Product("icecream", 19.79)
testing_product4 = Product("bike", 559.99)
testing_product5 = Product("toy", 50.88)
testing_product6 = Product("tv", 800.00)
testing_product7 = Product("bread", 2.59)
testing_product8 = Product("apple", 0.89)
testing_product9 = Product("soda", 2.19)
testing_product10 = Product("book", 9.99)

stock_test = Stock()
stock_test.AddToStock(testing_product1, 28)
stock_test.AddToStock(testing_product2, 50)
stock_test.AddToStock(testing_product3, 10)
stock_test.AddToStock(testing_product4, 3)
stock_test.AddToStock(testing_product5, 5)
stock_test.AddToStock(testing_product6, 1)
stock_test.AddToStock(testing_product7, 6)
stock_test.AddToStock(testing_product8, 8)
stock_test.AddToStock(testing_product9, 100)
stock_test.AddToStock(testing_product10, 40)



testing_cart = Cart()
testing_bot = ChatBot()

testing_bot.opening_cart(testing_cart, stock_test)

