import io

import torch
from PIL import Image
from torchvision import transforms

from disease_classifier.custom_model import ResNet9

disease_classes = ['Apple___Apple_scab',
                   'Apple___Black_rot',
                   'Apple___Cedar_apple_rust',
                   'Apple___healthy',
                   'Blueberry___healthy',
                   'Cherry_(including_sour)___Powdery_mildew',
                   'Cherry_(including_sour)___healthy',
                   'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                   'Corn_(maize)___Common_rust_',
                   'Corn_(maize)___Northern_Leaf_Blight',
                   'Corn_(maize)___healthy',
                   'Grape___Black_rot',
                   'Grape___Esca_(Black_Measles)',
                   'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                   'Grape___healthy',
                   'Orange___Haunglongbing_(Citrus_greening)',
                   'Peach___Bacterial_spot',
                   'Peach___healthy',
                   'Pepper,_bell___Bacterial_spot',
                   'Pepper,_bell___healthy',
                   'Potato___Early_blight',
                   'Potato___Late_blight',
                   'Potato___healthy',
                   'Raspberry___healthy',
                   'Soybean___healthy',
                   'Squash___Powdery_mildew',
                   'Strawberry___Leaf_scorch',
                   'Strawberry___healthy',
                   'Tomato___Bacterial_spot',
                   'Tomato___Early_blight',
                   'Tomato___Late_blight',
                   'Tomato___Leaf_Mold',
                   'Tomato___Septoria_leaf_spot',
                   'Tomato___Spider_mites Two-spotted_spider_mite',
                   'Tomato___Target_Spot',
                   'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                   'Tomato___Tomato_mosaic_virus',
                   'Tomato___healthy']

disease_model_path = 'models/plant_disease_model.pth'
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(
    disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()

def predict_image(img, model=disease_model):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)

    yb = model(img_u)
    _, preds = torch.max(yb, dim=1)
    prediction = disease_classes[preds[0].item()]
    return prediction


# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.preprocessing import image
# import io
# from disease_classifier.disease_info import get_disease_recommendation


# # Load the saved model and class labels
# model = tf.keras.models.load_model('models/plant_disease_model.h5')
# with open('models/class_labels.txt', 'r') as f:
#     class_labels = f.read().splitlines()

# def predict_image(img_bytes):
#     try:
#         # Load and preprocess the image
#         image_data = image.load_img(io.BytesIO(img_bytes), target_size=(128, 128))
#         image_array = image.img_to_array(image_data)
#         image_array = np.expand_dims(image_array, axis=0)
#         image_array /= 255.0  # Rescale the pixel values

#         # Make predictions
#         predictions = model.predict(image_array)
#         predicted_class = class_labels[np.argmax(predictions)]
#         print("classpre",predicted_class)
#         # info = get_disease_recommendation(predicted_class)
#         # print(info)
#         print("preddddiction aa gyi",predicted_class)
#         return predicted_class
#     except Exception as e:
#         return {"error": str(e), "success": False}
