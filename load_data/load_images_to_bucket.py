
# imports
import requests
import os
from google.cloud import storage
import pandas as pd
import shutil
from google.cloud import bigquery

# params
GCP_PROJECT = os.environ.get('GCP_PROJECT')
BQ_DATASET = os.environ.get('BQ_DATASET')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')


def load_images_to_bucket():
    # get table name
    full_table_name = f'{GCP_PROJECT}.{BQ_DATASET}.image_data'
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

    # get image table from big query
    # instantiate client
    client = bigquery.Client(project=GCP_PROJECT)
    # set up query job
    query_job = client.query(query)
    # run query
    result = query_job.result()
    # store results in df
    artworks_df = result.to_dataframe()

    # create local folder to store the images
    path = './image_temp'
    if not os.path.exists(path):
        os.mkdir(path)
        print("Folder %s created!" % path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)
        print("Folder deleted and recreated")

    # upload 500 images to a separate folder
    for i in range(500,510):
        # get url of normalized image
        url = artworks_df.loc[i, 'image_url_normalized']
        # get file name from index
        file_name = f"image_temp/{i}_{artworks_df.loc[i,'numeric_index']}_{artworks_df.loc[i,'artwork_id']}.jpg"

        # get the image from the url
        data = requests.get(url).content

        # open a new file
        f = open(file_name, 'wb')

        # store the image to the file
        f.write(data)
        f.close()

        # now upload the image to the cloud
        # instantiate the storage client
        storage_client = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS, project=GCP_PROJECT)

        # get bucket
        bucket = storage_client.get_bucket(BUCKET_NAME)

        # create blob
        blob = bucket.blob('500/{}.jpg'.format(f"{i}_{artworks_df.loc[i,'numeric_index']}_{artworks_df.loc[i,'artwork_id']}"))

        # upload file
        with open(file_name, 'rb') as f:
            blob.upload_from_file(f)
        f.close()

        # delete file
        os.remove(file_name)

    shutil.rmtree(path)

    print('data loaded')

if __name__ == ('__main__'):
    load_images_to_bucket()
'''
# upload all to all folder
for i in range(2719,2730):
    # get url of normalized image
    url = artworks_df.loc[i, 'image_url_normalized']
    # get file name from index
    file_name = f"image_temp/{i}_{artworks_df.loc[i,'numeric_index']}_{artworks_df.loc[i,'artwork_id']}.jpg"

    # get the image from the url
    data = requests.get(url).content

    # open a new file
    f = open(file_name, 'wb')

    # store the image to the file
    f.write(data)
    f.close()

    # now upload the image to the cloud
    # instantiate the storage client
    storage_client = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS, project=GCP_PROJECT)

    # get bucket
    bucket = storage_client.get_bucket(BUCKET_NAME)

    # create blob
    blob = bucket.blob('all/{}.jpg'.format(f"{i}_{artworks_df.loc[i,'numeric_index']}_{artworks_df.loc[i,'artwork_id']}"))

    # upload file
    with open(file_name, 'rb') as f:
        blob.upload_from_file(f)
    f.close()

    # delete file
    os.remove(file_name)
'''
