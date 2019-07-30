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

    def get_similar_users(self, email_id, mtrx, usr_idx):
        cosim = cosine_similarity(mtrx, mtrx)
        usrs = list(enumerate(cosim[usr_idx]))
        smlr_usrs = sorted(usrs, key=lambda x:x[1], reverse=True)[1:self.n]
        return [self.user_ids[x[0]] for x in smlr_usrs]

    def get_product_means(self, email_id, mtrx, usr_idx):
        smlr_usrs = self.get_similar_users(email_id, mtrx, usr_idx)
        usr_prod = mtrx.loc[smlr_usrs,:]
        return pd.Series(usr_prod.mean(axis=0))

    def get_ctgr_means(self, email_id, ctgr_mtrx, usr_idx):
        smlr_usrs = self.get_similar_users(email_id, ctgr_mtrx, usr_idx)
        usr_ctgr = ctgr_mtrx.loc[smlr_usrs, :]
        return pd.Series(usr_ctgr.mean(axis=0))

    def get_prdct_list(self, mtrx, prdct_mean, ctgr_mean, usr_idx):
        usr_val = mtrx.iloc[usr_idx]
        usr_val = usr_val[usr_val == 0]
        for (prdct, val) in usr_val.iteritems():
            prdc_idx = self.product_ids.index(prdct)
            ctgr = self.products[prdc_idx].get('category')
            usr_val[prdct] = (prdct_mean[prdct] + ctgr_mean[ctgr])/2
        return usr_val

    def get_recomended_product(self, email_id):
        
        mtrx = self.get_matrix()
        usr_idx = self.user_ids.index(email_id)
        prdct_mean = self.get_product_means(email_id, mtrx, usr_idx)
        ctgr_mtrx = self.get_ctgr_mtrx(mtrx)
        ctgr_mean = self.get_ctgr_means(email_id, ctgr_mtrx, usr_idx)
        prdt_lst = self.get_prdct_list(mtrx, prdct_mean, ctgr_mean, usr_idx)
        prdt_lst = prdt_lst.sort_values(axis=0, ascending=False)
        if prdt_lst.empty: return None
        prdct_idx = self.product_ids.index(prdt_lst.index[0])
        return self.products[prdct_idx]
 
# Dev mode !!
a = Model('Sales Person')
print(a.get_recomended_product('arun@g2.com'))