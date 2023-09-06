from tensorflow import convert_to_tensor, expand_dims
from tensorflow.image import grayscale_to_rgb
'''
Prep function
'''

def preprocess(input_image):
    img = input_image.resize((224,224))
    img_tensor = convert_to_tensor(img)/255
    if len(img_tensor.shape) < 3:
        img_tensor = grayscale_to_rgb(expand_dims(img_tensor,axis=2))
    return img_tensor
