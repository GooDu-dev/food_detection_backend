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
from utils.sample import FruitManager, FruitItem
import json

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
    }, next="")

    return JsonResponse(res, status=status)

@api_view(['GET'])
def get_items_all(request):
    manager = FruitManager()
    result = manager.get_all().get_data()
    if not result:
        status, res = response.createStatusOK({
            "result": []
        }, next="/item")
        return JsonResponse(res, status=status)
    else:
        status, res = response.createStatusOK({
            "result": result
        }, next="/item/id")
        return JsonResponse(res, status=status)
@api_view(['GET'])
def get_item_by_id(request):
    id = int(request.GET.get('product_id', 0))
    if id <= 0:
        status, res = error.RequestMissingFieldError.get_error_resposne()
        return JsonResponse(res, status=status)
    
    manager = FruitManager()
    result = manager.get_by_id(id).get_data()

    if not result:
        status, res = response.createStatusOK({
            "result": []
        }, next="/item")
        return JsonResponse(res, status=status) 
    else:
        status, res = response.createStatusOK({
            "result": result
        }, next="")
        return JsonResponse(res, status=status)

@api_view(['GET'])
def get_items_by_date(request):
    date = request.GET.get('d', "")
    if not date:
        status, res = error.RequestMissingFieldError.get_error_resposne()
        return JsonResponse(res, status=status)
    
    manager = FruitManager()
    result = manager.get_by_date(options={
        "date": date,
        "operator": ""
    }).get_data()
    
    if not result:
        status, res = response.createStatusOK({
            "result": []
        }, next="/item")
        return JsonResponse(res, status=status)
    else:
        status, res = response.createStatusOK({
            "result": result
        }, next="")
        return JsonResponse(res, status=status)

@api_view(['GET'])
def get_items_by_name(request):
    name = request.GET.get('name', "")
    if not name:
        status, res = error.RequestMissingFieldError.get_error_resposne()
        return JsonResponse(res, status=status)
    
    manager = FruitManager()
    result = manager.get_by_name(name).get_data()
    
    if not result or result == []:
        status, res = response.createStatusOK({
            "result": []
        }, next="/item")
        return JsonResponse(res, status=status)
    else:
        status, res = response.createStatusOK({
            "result": result
        }, next="")
        return JsonResponse(res, status=status)

@api_view(['POST'])
def create_new_item(request):
    data = json.loads(request.body)
    name = data.get('name', "")
    date_add = data.get('date', "")
    
    if not name or not date_add :
        print("no name or date_add", name, date_add)
        status, res = error.RequestMissingFieldError.get_error_resposne()
        return JsonResponse(res, status=status)
    
    item = FruitItem(name=name, date_add=date_add, status="waiting")

    manager = FruitManager()
    index, err = manager.create_item(item)

    if err :
        if isinstance(err, error.Error):
            status, res = err.get_error_resposne()
            return JsonResponse(res, status=status)
        else:
            status, res = error.new_server_error(err)
            return JsonResponse(res, status=status)
    if not index:
        status, res = error.new_server_error("Cannot get item index")
        return JsonResponse(res, status=status)

    status, res = response.createStatusCreated({
        "id": index
    }, next=f"/item?product_id={index}")
    return JsonResponse(res, status=status)
