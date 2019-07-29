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
        self.product_ids = [ str(prd.get('_id')) for prd in self.products ]
        self.user_ids = [ usr.get('email_id') for usr in self.users ]

    def update_matrix_values(self, email_id, a, col):
        usr_fbs = list(DB().find(DB.USER_FB,{'email_id':email_id}))
        for fb in usr_fbs:
            index = self.product_ids.index(fb.get('product_id'))
            a[col][index] = fb.get('value')

    def get_matrix(self):
        a = np.zeros(shape = (len(self.users), len(self.products)))
        for i, usr in enumerate(self.users):
            self.update_matrix_values(usr.get('email_id'), a, i)
        return pd.DataFrame(a, index=self.user_ids, columns=self.product_ids)

    def get_ctgr_mtrx(self, mtrx):
        ctgrs = [prd.get('category') for prd in self.products]
        ctgr_mtrx = mtrx.copy()
        ctgr_mtrx.columns = ctgrs
        return ctgr_mtrx.groupby(level=0, axis=1).mean()

    def get_similar_users(self, email_id, mtrx):
        cosim = cosine_similarity(mtrx, mtrx)
        index = self.user_ids.index(email_id)
        usrs = list(enumerate(cosim[index]))
        smlr_usrs = sorted(usrs, key=lambda x:x[1], reverse=True)[1:self.n]
        return [self.user_ids[x[0]] for x in smlr_usrs]

    def get_product_means(self, email_id, mtrx):
        smlr_usrs = self.get_similar_users(email_id, mtrx)
        usr_prod = mtrx.loc[smlr_usrs,:]
        return pd.Series(usr_prod.mean(axis=0))
        #normalise mean scores

    def get_ctgr_means(self, email_id, ctgr_mtrx):
        smlr_usrs = self.get_similar_users(email_id, ctgr_mtrx)
        usr_ctgr = ctgr_mtrx.loc[smlr_usrs, :]
        return pd.Series(usr_ctgr.mean(axis=0))

    def get_recomended_product(self, email_id):
        
        mtrx = self.get_matrix()
        prod_mean = self.get_product_means(email_id, mtrx)
        ctgr_mtrx = self.get_ctgr_mtrx(mtrx)
        ctgr_mean = self.get_ctgr_means(email_id, ctgr_mtrx)
        return None
 
# Dev mode !!
# a = Model('Developer')
# a.get_recomended_product('arunrakhelkar@gmail.com')