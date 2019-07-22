import json

from user       import User
from model      import Model
from db         import DB
from persona    import Persona
from product    import Product


def show_products(user):
    product = Product().get_recomended_product(user)
    if not product: 
        print("You have viewed all the products")
        return False
    print(product.get('name'))
    inp = input("Is this product relevant: Y/N: ")
    Product().update(user, inp, product)
    return True

def main():
    email_id = input("enter email_id:").strip()
    user = User(email_id).get()
    if user: 
        while(True):
            r = show_products(user)
            if not r: break
    else:
        #add user to db
        personae = Persona().list()
        for i, persona in enumerate(personae):
            print(i, persona.get('name'))
        index = input("Pick persona id: ")
        index = int(index)
        if(index>=len(personae)):
            print("invalid id")
            return
        persona = personae[index]
        User(email_id).add(persona.get('name'))
        while(True):
            r = show_products(user)
            if not r: break


if __name__ == "__main__":
    main()

