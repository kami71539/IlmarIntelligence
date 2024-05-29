#!/usr/bin/env python
# coding: utf-8

# In[1]:


def clean_data(source_dir, processed_dir):

    os.makedirs(processed_dir, exist_ok=True) # Create directory if it does not exists.
    
    for filename in os.listdir(source_dir):
        
        filepath = source_dir + filename
        
        df = pd.read_csv(filepath, encoding = 'utf-8')
    
        df, na_df = treat_missing_values(df) #Treating missing values

        na_df.to_csv(processed_dir + filename.split('.')[0] + 'na_values.bad', index = False)
        
        df_good, df_bad = expected_rates(df)

        df_good.to_csv(processed_dir + filename.split('.')[0] + '.out')

        df_bad.to_csv((processed_dir + filename.split('.')[0] + ' rates_defective.bad'))


# In[2]:


# This function will poppulate the missing values with nan or 0 to ensure that the pipeline does not break in the further steps.
# Of course there are better approaches for treating missing values such as using mode or any specific meaningful value. 
# Also, perfoming EDA will help us understand better what value to use.

def treat_missing_values(data):
    
    cat_columns = ['url', 'address', 'name', 'online_order', 'book_table', 'rate', 'location','rest_type','dish_liked', 'cuisines',
                   'reviews_list',	'menu_item',	'listed_in(type)',	'listed_in(city)']
    
    numeric_columns = ['votes', 'phone', 'approx_cost(for two people)']

    missing_values_count = data.isna().sum().sum()
    
    if missing_values_count > 0:
        print(f"There are {missing_values_count} missing values in the data.")
        filtered_df = data[data.isna().any(axis=1)]

    # missing values to be replaced with 'Missing' the mod of that column
    for col in cat_columns:
        data[col].fillna('NA', inplace = True)
    
    for col in numeric_columns:
        data[col].fillna(0, inplace = True)

    return data, filtered_df


# In[3]:


def expected_rates(data):
    data = data[data['rate'].str.contains('/', na = False)]
    data[['review_given', 'review_total']] = data['rate'].str.split('/', expand=True).astype(float)
    
    # Filter data where left side <= 5 and right side is 5
    data_filtered = data[(data['review_given'] <= 5) & (data['review_total'] == 5)]

    data_filtered_bad = data[~((data['review_given'] <= 5) & (data['review_total'] == 5))]
    
    data_filtered.drop(columns = ['review_given', 'review_total'], inplace = True)
    data_filtered_bad.drop(columns = ['review_given', 'review_total'], inplace = True)

    return data_filtered, data_filtered_bad


# In[ ]:


import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

source_dir = r"K:\Ilmar intelligence\pre_processed\\"
processed_dir = r"K:\Ilmar intelligence\processed\\"

clean_data(source_dir, processed_dir)

input('Press Enter to continue')


# In[ ]:




