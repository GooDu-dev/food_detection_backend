"""
This file contains the code for the API endpoint that will be used to make predictions on the images.
"""

from django.http import JsonResponse
from rest_framework.decorators import api_view
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
from io import BytesIO
import os
import utils.errors as error
import utils.response as response

# Loading your pre-trained model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'backend', 'model.h5')
model = load_model(model_path)

@api_view(['POST'])
def predict_image(request): 
    if 'file' not in request.FILES:
        status, res = error.RequestMissingFieldError.get_error_resposne()
        return JsonResponse(res, status=status)
    file = request.FILES['file']
    if(file == None):
        status, res = error.RequestMissingFieldError.get_error_resposne()
        return JsonResponse(res, status=status)
    image = Image.open(file)

    if(image == None):
        status, res = error.RequestInvalidError.get_error_resposne()
        return JsonResponse(res, status=status)

    # Converting image to RGB format
    image = image.convert('RGB')

    # resize image into 256x256
    image = image.resize((256, 256))  

    # Converting image into numpy array
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)  
    img_array = img_array/255.0

    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction[0])
    result = 'fresh' if predicted_index < 6 else 'rotten'

    status, res = response.createStatusOK(data={
        "result": result,
        "prediction": predicted_index
    }, next="")

    return JsonResponse(res, status=status)