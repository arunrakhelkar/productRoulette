import json
import pandas as pd
import numpy as np
import warnings

from db import DB 
from user import User
from sklearn.metrics.pairwise import cosine_similarity
 
warnings.filterwarnings('ignore')
 
class Model:
 
    def __init__(self, persona, top_users = 3):
        self.top_users = top_users
        self.persona = persona
        self.db = DB()
        self.users = list(self.db.find(DB.USERS_CLXN,{'persona':persona}))
        #self.personae = self.db.find(DB.PERSONA_CLXN)
        self.products = list(self.db.find(DB.PROD_CLXN))
        self.get_matrix()   

    def get_matrix(self):
        prod_cnt = len(self.products)
        #print(self.persona)
        filter = { 'persona': self.persona }
        user_fb = list(self.db.find(DB.USER_FB,filter,{'_id':False}))
        users_list = [usr.get('email_id') for usr in self.users]
        products_list = [str(prd.get('_id')) for prd in self.products]
        df = pd.DataFrame.from_records(user_fb)
        # matrix = df.pivot_table(index = users_list, columns = products_list, 
        #                          values = 'value', fill_value = 0)
        # a = np.zeros(shape = (len(self.users), len(self.products)))
        # m1 = pd.DataFrame(a, index=users_list,
        #                         columns=products_list)
        # fl = pd.DataFrame(matrix.to_records())
        print(df)
    
    def get_similar_users(self, user_id):
        cosim = cosine_similarity(self.matrix, self.matrix)
        index = self.users.index(user_id)
        sim_list = list(enumerate(cosim[index]))
        most_sim_users = sorted(sim_list, key=lambda x: x[1], reverse=True)
        most_sim_users = most_sim_users[1:]
        sim_users = [x[0] for x in most_sim_users]
        print(sim_users)
        return sim_users
    
 
    def get_recomended_product(self, user_id):
        
        sim_users = self.get_similar_users(user_id)
        sim_users = [self.users[i] for i in sim_users]
        candidates_prod = self.matrix.loc[sim_users,:]
        mean_score = pd.Series(candidates_prod.mean(axis=0))
        mean_score = mean_score.sort_values(axis=0, ascending=False)
        recom_prod = list(mean_score.iloc[:].keys())
        print(recom_prod)
        index = self.users.index(user_id)
        for i in recom_prod:
            print(self.matrix.iloc[index][i])
            if self.matrix.iloc[index][i] == 0: 
                print(self.products[i])
                return self.products[i] 
        #No product remaining
        return None
 
#usr = User('test@g2.com').get_user()
a = Model('Software Developer')

#a.get_recomended_product('arunrakhelkar@gmail.com')