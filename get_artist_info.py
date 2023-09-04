# import requests
# import pandas as pd
# import numpy as np
# import time
# import os,sys,os.path
# from dotenv import load_dotenv
# load_dotenv()

# API_XAPP_TOKEN = os.environ.get('API_XAPP_TOKEN')

# artists_df = pd.DataFrame(columns=('artwork_id','id','slug','sortable_name','gender','birthday','deathday','hometown','location','nationality'))"
   
# params = {'size':'100',
# 'offset':offset,
# 'id':
# 'xapp_token':API_XAPP_TOKEN}

# url = f'https://api.artsy.net/api/artists/'

# response = requests.get(url,params=params).json()

# artists = response['_embedded']['artworks']
#     "#     artworks_ = []
    
#     for artist in artists:
#         artist_dict={}
        
# artist_dict["id"] = artist["id"],
# artist_dict["slug"] = artist["slug"],
# artist_dict["name"] = artist["sortable_name"],
# artist_dict["gender"] = artist["gender"],
# artist_dict["birthday"] = artist["birthday"],
# artist_dict["deathday"] = artist["deathday"],
# artist_dict["hometown"] = artist["hometown"],
# artist_dict["location"] = artist["location"],
# artist_dict["nationality"] = artist["nationality"],

# artists_df.append(artist_dict)

# artworks_temp = pd.DataFrame([artist_dict])
# artists_df = pd.concat([artists_df, artworks_temp], ignore_index=True)\n",

from google.cloud import bigquery
from google.oauth2 import service_account

# service_account_info = json.load(open('service_account.json'))
#     credentials = service_account.Credentials.from_service_account_info(
#         service_account_info)

# credentials = service_account.Credentials.from_service_account_file(r'C:\Users\sweet\Desktop\leafy-tuner-396605-186124437d5b.json')  
# from google.cloud import bigquery
# client = bigquery.Client.from_service_account_json(r'C:\Users\sweet\Desktop\leafy-tuner-396605-186124437d5b.json')

query = f'''
SELECT 
  artwork_id,
  title,
  category,
  medium,
  date,
  height_cm,
  width_cm,
  collecting_institution,
  image_url_template,
  image_url_normalized
FROM alert-passkey-392415.artsyfartscidata.image_data_balanced
'''

project_id = 'alert-passkey-392415'
client = bigquery.Client(project=project_id, location=any)


results = client.query(query).result()
# data = results.to_dataframe()

print(results)