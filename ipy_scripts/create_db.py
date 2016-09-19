
# coding: utf-8

# In[2]:

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from antipark import *
from antipark.models import Product, Category


# In[3]:

import json

with open('../antipark/db.json', encoding='utf=8', mode='r') as fo:
    data = json.load(fo)

d = {}
for k,v in data['products'].items():
    d[k] = v


# In[4]:

db.create_all()


# In[29]:

# if smth was wrong
# db.session.rollback()


# In[5]:

for category, values in d.items():
    
    description = values['desc']
    
    cat = Category(category=category,
                   description=description,
                  )
    db.session.add(cat)
    db.session.commit()


# In[6]:

categories = Category.query.all()
categories


# In[23]:

from collections import namedtuple

Cat = namedtuple('Cat', ['category', 'idx'])
cats = []
for category in categories:
    cat = Cat(category.category, category.id)
    cats.append(cat)


# In[ ]:

for category, values in d.items():
    
    for cat in cats:
        if category == cat.category:
            category_id = cat.idx
            break
    
    all_vars = values['variations']
    
    for var in all_vars:
        # prices
        prices = all_vars[var]['prices'].strip('[]').split(', ')
            
        # stage_prices
        stage_prices = all_vars[var]['stage'].strip('[]').split(', ')
            
        # names
        names = all_vars[var]['names'].strip('[]').split(', ')
        
        # subcategory
        subcategory = all_vars[var]['general']
        
        # specs
        chars = all_vars[var]['chars'].strip('[]').split(', ')
        char_values_str = all_vars[var]['values'].split('], [')
        char_values_temp = []
        for ch_v in char_values_str:
            char_values_temp.append(ch_v.strip('[]').split(', '))
                
        specs = []
        print(chars)
        for ch_v in char_values_temp:
            print(ch_v)
            print()
            char_values_dict = {}
            for i, ch in enumerate(ch_v):
                char_values_dict[chars[i]] = ch
            specs.append(str(char_values_dict))
            
        # images
        images_str = all_vars[var]['imgs'].strip('[]').split(', ')
        images = []
        for img in images_str:
            image = all_vars[var]['dest'] + img + ".jpg"
            images.append(image)
            
        
        # commit rec to db
        for i, title in enumerate(names):
            prod = Product(category=category_id,
                           subcategory=subcategory,
                           title=title,
                           specs=specs[i],
                           price=prices[i],
                           stage_price=stage_prices[i],
                           image=images[i],
                           )
            db.session.add(prod)
            db.session.commit()

