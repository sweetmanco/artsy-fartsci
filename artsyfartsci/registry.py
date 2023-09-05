import os
import numpy as np
import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
from artsyfartsci.params import *
'''
loading from cloud
BQ -
artists df
artworks df
Bucket -
encoded images
model weights
image (by index)
'''

def load_artworks_info():
    # get table name
    full_table_name = f'{GCP_PROJECT}.{BQ_DATASET}.image_data_balanced_new_index'
    # write query
    query = f'''
            SELECT
                numeric_index,
                artwork_id,
                title,
                category,
                medium,
                date,
                height_cm,
                width_cm,
                image_url_template,
                collecting_institution,
                image_url_normalized
            FROM {full_table_name}
            '''
    # instantiate client
    client = bigquery.Client(project=GCP_PROJECT)
    # set up query job
    query_job = client.query(query)
    # run query
    result = query_job.result()
    # store results in df
    artworks_df = result.to_dataframe()
    return artworks_df

def load_artists_info():
    pass

#TODO create dir for the files to go to

def load_encoded_images():
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.get_blob('encoded/encoded_10000.npy')
    blob.download_to_filename('encoded_images.npy')
    encoded_images_np = np.load('encoded_images.npy')
    # put this file in a nicer place
    return encoded_images_np


def load_model_weights():
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.get_blob('model/modelweights_100.hdf5')
    blob.download_to_filename('model_weights.hdf5')
    #put this in a nice place too so it can be called elsewhere
    return 'model_weights.hdf5'

def load_image_jpg(image_index,artwork_id):
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="balanced"))
    blob_name = False
    for blob in blobs:
        if int(blob.name.replace('balanced/','').split('_')[0]) == image_index:
            blob_name = blob.name
    if blob_name:
        blob = bucket.get_blob(blob_name)
        blob.download_to_filename(f'{image_index}_{artwork_id}.jpg')
        return 'filename goes here'
    else:
        return 'image not found'
    
