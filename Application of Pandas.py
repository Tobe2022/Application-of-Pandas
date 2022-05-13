#!/usr/bin/env python
# coding: utf-8

# importing libraries
# 
# 

# In[1]:


import pandas as pd
import os


# Task 1: Merge 12 months of data into a single csv file

# In[2]:


files = [file for file in os.listdir('C:\\Users\\Tobechukwu\\Downloads\\Pandas-Data-Science-Tasks-master\Pandas-Data-Science-Tasks-master\\SalesAnalysis\Sales_Data')]

all_months_data = pd.DataFrame()


for file in files:
    df = pd.read_csv('C:\\Users\\Tobechukwu\\Downloads\\Pandas-Data-Science-Tasks-master\Pandas-Data-Science-Tasks-master\\SalesAnalysis\Sales_Data\\' + file)
    all_months_data = pd.concat([all_months_data, df])
    
all_months_data.to_csv('all_data.csv',index=False)
    


# read in updated dataframe

# In[3]:


all_data = pd.read_csv('all_data.csv')
all_data.head()


# Clean up the Data
# 
# drop rows of nan

# In[4]:


nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()

all_data = all_data.dropna(how = 'all')
all_data.head()


# Find 'Or' values and delete it

# In[5]:


all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
all_data.head()


# convert columns to correct type

# In[6]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data.head()


# In[ ]:





# In[ ]:





# Augment data with additional column
# 
# Task 2: Add month column

# In[7]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# Task 3: Add a sales column

# In[8]:


all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head()


# ### Q1) what was the best month for sales? How much was earned that month?

# In[9]:


results = all_data.groupby('Month').sum()
results


# In[10]:


#making a quick visualization
import matplotlib.pyplot as plt
months = range(1, 13)
plt.bar(months, results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month Number (January - December)')
plt.show()


# ### Q2) What city had the highest number of sales?

# Task 4: Add a city column

# In[11]:


#using the apply() function

def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f'{get_city(x)} ({get_state(x)})')
all_data.head()


# ### Now city with the highest number of Sales

# In[12]:


results = all_data.groupby('City').sum()
results


# In[13]:


cities = [city for city, df in all_data.groupby('City')]
plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation = 'vertical', size = 8)
plt.ylabel('Sales in USD ($)')
plt.xlabel('City Name')
plt.show()


# ### Q3 what time do we dispaly advertisements to maximize likelihood of customers buyig products

# In[14]:


all_data.head()


# In[15]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data.head()


# In[16]:


all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data.head()


# In[17]:


hours = [hour for hour, df in all_data.groupby('Hour')]

plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.grid()
plt.ylabel('Number of Orders Made')
plt.xlabel('Time Order was Made')
plt.show()


# from the chart, my recommendation will be around 11am or 7pm.


# ### Q4: What products are most often sold together

# In[18]:


df = all_data[all_data['Order ID'].duplicated(keep = False)]

df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df =df[['Order ID', 'Grouped']].drop_duplicates()
df.head()


# In[19]:


from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
    
for key, value in count.most_common(10):
    print(key, value)
    


# ### Q5: What product sold the most, and why  do I think it sold the most?

# In[20]:


product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']

products = [product for product, df in product_group]

plt.bar(products, quantity_ordered)
plt.ylabel('Quantity Ordered')
plt.xlabel('Products')
plt.xticks(products, rotation = 'vertical', size = 8)
plt.show()


# In[ ]:


product

