import tensorflow as tf
import numpy as np
from PIL import Image



class_map = {0: 'Apple', 1: 'Banana', 2: 'Broccoli', 3: 'Carrots', 4: 'Cauliflower', 5: 'Chili', 6: 'Coconut', 
             7: 'Cucumber', 8: 'Custard apple', 9: 'Dates', 10: 'Dragon', 11: 'Egg', 12: 'Garlic', 13: 'Grape', 
             14: 'Green Lemon', 15: 'Jackfruit', 16: 'Kiwi', 17: 'Mango', 18: 'Okra', 19: 'Onion', 20: 'Orange', 
             21: 'Papaya', 22: 'Peanut', 23: 'Pineapple', 24: 'Pomegranate', 25: 'Star Fruit', 26: 'Strawberry', 
             27: 'Sweet Potato', 28: 'Watermelon', 29: 'White Mushroom'}

# Load the model
model = tf.keras.models.load_model('C:/NPersonal/Projects/fresh_eats/Django_backend/django_backend/image_upload/utils/model_2.1.h5')



def predict_image_class(image_path):

    try:
        # Load and preprocess the image
        img = Image.open(image_path).resize((240, 240))
        img_arr = np.array(img) / 255.0
        img_input = img_arr[np.newaxis, ...]  # Add batch dimension

        # Predict the label
        predicted_label = np.argmax(model.predict(img_input))
        predicted_class = class_map[predicted_label]

        return predicted_class

    except Exception as e:
        print(f"Error predicting image: {e}")
        return None
