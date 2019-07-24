import json

from user       import User
from model      import Model
from db         import DB
from persona    import Persona
from product    import Product


def show_products(user):
    while(True):
        email_id = user.get('email_id')
        user_persona = user.get('persona')
        product = Model(user_persona).get_recomended_product(email_id)
        if not product: 
            print("You have viewed all the products")
            return
        print(product.get('name'))
        inp = input("Is this product relevant: Y/N: ")
        Product().update(user, inp, product)

def main():
    email_id = input("enter email_id:").strip()
    user = User().get(email_id)
    if user: 
        show_products(user)
    else:
        #add user to db
        personae = Persona().list()
        for i, persona in enumerate(personae):
            print(i, persona.get('name'))
        index = int(input("Pick persona id: "))
        if(index>=len(personae)):
            print("invalid id")
            return
        persona = personae[index]
        User().add(persona.get('name'), email_id)
        user = User().get(email_id)
        show_products(user)


if __name__ == "__main__":
    main()

