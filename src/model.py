import json
import pandas as pd
import numpy as np
import warnings

from db import DB 
from user import User
from product import Product
from sklearn.metrics.pairwise import cosine_similarity
 
warnings.filterwarnings('ignore')
 
class Model:
 
    def __init__(self, persona, top_users = 3):
        self.top_users = top_users
        self.persona = persona
        self.db = DB()
        self.users = User().list({'persona':persona})
        self.products = Product().list()
        self.users_list = [usr.get('email_id') for usr in self.users]
        self.products_list = [str(prd.get('_id')) for prd in self.products]
        self.matrix = self.get_matrix()   

    def get_dict(self):
        d = {}
        for i, prod in enumerate(self.products):
            d[str(prod.get('_id'))] = i
        return d

    def get_matrix(self):
        d = self.get_dict()
        self.d = d
        prod_cnt = len(self.products)
        filter = { 'persona': self.persona }
        user_fb = list(self.db.find(DB.USER_FB,filter,{'_id':False}))
        df = pd.DataFrame.from_records(user_fb)
        n_rows = len(self.users)
        n_col = len(self.products)
        a = np.zeros(shape = (n_rows,n_col))
        for i, usr in enumerate(self.users):
            usr_fbs = list(DB().find(DB.USER_FB,{'email_id':usr.get('email_id')}))
            for fb in usr_fbs:
                prod_id = fb.get('product_id')
                index = d[prod_id]
                a[i][index] = fb.get('value')
        df = pd.DataFrame(a, index = self.users_list, columns = self.products_list)
        return df
    
    def get_similar_users(self, email_id):
        cosim = cosine_similarity(self.matrix, self.matrix)
        index = self.users_list.index(email_id)
        sim_list = list(enumerate(cosim[index]))
        most_sim_users = sorted(sim_list, key=lambda x: x[1], reverse=True)
        most_sim_users = most_sim_users[1:]
        sim_users = [x[0] for x in most_sim_users]
        return sim_users
    
    def get_recomended_product(self, email_id):
        
        sim_users = self.get_similar_users(email_id)
        sim_users = [self.users_list[i] for i in sim_users]
        candidates_prod = self.matrix.loc[sim_users,:]
        mean_score = pd.Series(candidates_prod.mean(axis=0))
        mean_score = mean_score.sort_values(axis=0, ascending=False)
        recom_prod = list(mean_score.iloc[:].keys())
        index = self.users_list.index(email_id)
        for i in recom_prod:
            if int(self.matrix.iloc[index][i]) == 0: 
                return self.products[self.products_list.index(i)] 
        #No product remaining
        return None
 
# Dev mode !!
# a = Model('Software Developer')
# a.get_recomended_product('arunrakhelkar@gmail.com')