import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ipdb import set_trace
from dateutil import parser
from artsyfartsci.ml_logic.preprocess import preprocess
from artsyfartsci.ml_logic.model import encode, similarities
from artsyfartsci.registry import load_image_jpg, load_artists_info, load_artworks_info


app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/top5similar")
def top5similar(input_image):
    input_prep = preprocess(input_image)
    input_encoded = encode(input_prep)
    top_5_indices = similarities(input_encoded)
    return top_5_indices.tolist()

@app.get("/image")
def image(image_index,artwork_id):
    image_file_name = load_image_jpg(image_index,artwork_id)
    return image_file_name
# this isn't finished

@app.get("/artwork_info")
def artwork_info(image_indices):
    artworks_df = load_artworks_info()
    response = []
    for i in image_indices:
        artwork_dict = artworks_df[artworks_df['image_index'] == i].to_dict(orient='records')[0]
        # get artist records and combine into one dict
        # artwork_dict | artist_dict
        # if there are any shared keys, right will overwrite left
    # then streamlit will grab the artwork_id and image_index 
