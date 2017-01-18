
# coding: utf-8

# In[155]:

from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
from bson import json_util, ObjectId
from pandas.io.json import json_normalize
import json
import numpy as np
import seaborn as sns
import pylab
get_ipython().magic(u'matplotlib inline')


# In[250]:

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    pipeline = [{"$match":{"address.postcode":{"$exists":1}}}, 
                {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}},
                {"$sort":{"count":-1}}]#,{"$limit":10}
    return pipeline
    
    
def aggregate(db, pipeline):
    return db.sample.aggregate(pipeline)

def find(db):
    return db.sample.find("")

def main():
    db = get_db('test')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    #result = find(db)
    #print list(result)
    #pprint(list(result))
    
    sanitized = json.loads(json_util.dumps(result))
    normalized = json_normalize(sanitized)
    df = pd.DataFrame(normalized)
    """ 
    Reference:
    http://stackoverflow.com/questions/33347906/getting-nested-data-from-mongodb-into-a-pandas-data-frame
    """
    return df
    


df = main()
df.head()


# In[251]:

df[['_id']] = df[['_id']].astype(int)
df[['count']] = df[['count']].astype(int)


# In[253]:

a = df['_id']
b = df['count']
sns.plt.scatter(a,b)
axes = plt.gca()
axes.set_xlim([60000,60800])
axes.set_ylim([0,500000])
sns.plt.title('Postcode Distribution')
sns.plt.ylabel('Count')
sns.plt.xlabel('Postcode')
sns.set_style("whitegrid")

