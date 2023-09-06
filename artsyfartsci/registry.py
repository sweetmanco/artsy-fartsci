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



def load_encoded_images():
    encoded_path = os.path.join(os.path.dirname(__file__),'.','encoded_images','encoded_images.npy')
    print(encoded_path)
    encoded_images_np = np.load(encoded_path)
    # put this file in a nicer place
    return encoded_images_np


def load_model_weights():
    return os.path.join(os.path.dirname(__file__),'.','models','weights0018.hdf5')



if __name__ == '__main__':
    encoded_images = load_encoded_images()
    print('images_loaded')
