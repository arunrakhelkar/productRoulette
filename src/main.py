import json

from user       import User
from model      import Model
from db         import DB
from persona    import Persona
from product    import Product


    

def main():
    email_id = input("enter email_id:").strip()
    user = User(email_id).get()
    if user: 
        product = Product().get(user)
        print(product.get('name'))
        inp = input("Is this product relevant: Y/N")
        product.update(user, inp, product)
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


if __name__ == "__main__":
    main()

