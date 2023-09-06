import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile
import io
from PIL import Image
from artsyfartsci.ml_logic.preprocess import preprocess
from artsyfartsci.ml_logic.model import encode, similarities
#from artsyfartsci.registry import load_artists_info, load_artworks_info


app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/top_5_similar")
async def top_5_similar(image:UploadFile):
    image_data = await image.read()
    print('image loaded')
    input_image = Image.open(io.BytesIO(image_data))
    print('image opened')
    input_prep = preprocess(input_image)
    print('image processed')
    input_encoded = encode(input_prep)
    print('image encoded')
    top_5_indices = similarities(input_encoded)
    print(top_5_indices.tolist())
    results = {'top_5':top_5_indices.tolist()}
    return results


'''
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
'''
