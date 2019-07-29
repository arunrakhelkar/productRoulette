import pandas as pd
import numpy as np

from db import DB 
from user import User
from product import Product
from sklearn.metrics.pairwise import cosine_similarity
 
class Model:
 
    def __init__(self, persona, n = 5):

        self.n = n
        self.persona = persona
        self.users = User().list({'persona':persona})
        self.products = Product().list()
        self.user_ids = [ usr.get('email_id') for usr in self.users ]
        self.product_ids = [ str(prd.get('_id')) for prd in self.products ]
        self.matrix = self.get_matrix()

    def update_matrix_values(self, email_id, a, col):

        usr_fbs = list(DB().find(DB.USER_FB,{'email_id':email_id}))
        for fb in usr_fbs:
            index = self.product_ids.index(fb.get('product_id'))
            a[col][index] = fb.get('value')

    def get_matrix(self):

        a = np.zeros(shape = (len(self.users), len(self.products)))
        for i, usr in enumerate(self.users):
            self.update_matrix_values(usr.get('email_id'), a, i)
        df = pd.DataFrame(a, index = self.user_ids, columns = self.product_ids)
        return df
    
    def get_similar_users(self, email_id):

        cosim = cosine_similarity(self.matrix, self.matrix)
        index = self.user_ids.index(email_id)
        usrs = list(enumerate(cosim[index]))
        smlr_usrs = sorted(usrs, key=lambda x:x[1], reverse=True)[1:self.n]
        smlr_usrs = [x[0] for x in smlr_usrs]
        return smlr_usrs
    
    def get_recomended_product(self, email_id):
        
        smlr_usrs = self.get_similar_users(email_id)
        smlr_usrs = [self.user_ids[i] for i in smlr_usrs]
        candidates_prod = self.matrix.loc[smlr_usrs,:]
        mean_score = pd.Series(candidates_prod.mean(axis=0))
        mean_score = mean_score.sort_values(axis=0, ascending=False)
        recom_prod = list(mean_score.iloc[:].keys())
        index = self.user_ids.index(email_id)
        for i in recom_prod:
            if int(self.matrix.iloc[index][i]) != 0: continue
            return self.products[self.product_ids.index(i)] 
        #No product remaining
        return None
 
# Dev mode !!
# a = Model('Software Developer')
# a.get_recomended_product('arunrakhelkar@gmail.com')