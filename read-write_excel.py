
import pandas as pd
from antipark import *
from antipark.models import Product, Category
from collections import defaultdict


# Save Db to Excel

products = Product.query.all()
price_cols = ['id', 'title', 'price', 'stage_price']

prods = defaultdict(list)
for col in price_cols:
    for product in products:
        prods[col].append(getattr(product, col))    

df = pd.DataFrame(prods)
df.set_index('id', inplace=True)
df.to_excel('cur_base.xlsx')


# Read Excel and Update Db

df_new = pd.read_excel('cur_base.xlsx', index_col='id')

for prod in df_new.itertuples():
    upd_product = Product.query.get(prod.Index)
    for field in prod._fields[1:]:
        setattr(upd_product, field, getattr(prod, field))
    db.session.commit()
