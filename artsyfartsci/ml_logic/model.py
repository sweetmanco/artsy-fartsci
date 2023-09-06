
import numpy as np
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity
from artsyfartsci.registry import load_model_weights, load_encoded_images

'''
Build model and load weights
Encode function
'''


def create_model():
    # Encoder
    input_img = Input(shape=(224, 224, 3))
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)

    # Decoder
    x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    # Autoencoder
    autoencoder = Model(input_img, decoded)
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')


    # load model with pretrained weights
    model_weights_path = load_model_weights()
    autoencoder.load_weights(model_weights_path)

    # Extracting image representation using the encoder
    encoder = Model(input_img, encoded)

    return encoder

def encode(input_tensor):

    encoder = create_model()
    return encoder.predict(np.expand_dims(np.array(input_tensor),axis=0),verbose=0)

def similarities(input_encoded):
    # get all encoded images
    encoded_all = load_encoded_images()

    print('encoded data loaded')
    # Define batch size
    batch_size = 500

    # Calculate number of batches
    num_batches = int(encoded_all.shape[0] / batch_size)

    # Initialize an empty array for results
    results = np.zeros((1,1))
    # Calculate cosine similarity in batches
    for i in range(num_batches):
        start = i * batch_size
        end = (i + 1) * batch_size
        results_temp = cosine_similarity(input_encoded.reshape(1, -1),
                                               encoded_all[start:end].reshape(len(encoded_all[start:end]),-1))
        results = np.concatenate((results,results_temp),axis=1)

    results = results[:,1:]

    top_5_indices = np.argsort(results[0])[-5:][::-1]

    return top_5_indices
