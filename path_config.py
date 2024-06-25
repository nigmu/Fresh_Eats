import os

# Get the base directory (one level up from the current directory)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))

# Paths to your model files
TFIDF_ENCODINGS_PATH = os.path.join(BASE_DIR, 'recipe_recommendation', 'tfidf_encodings.pkl')
TFIDF_PATH = os.path.join(BASE_DIR, 'recipe_recommendation', 'tfidf.pkl')

# Path to your dataset
PARSED_DATA_PATH = os.path.join(BASE_DIR, 'dataset', 'parsed_data.csv')

# New paths for additional datasets and model files
NEW_DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'new_data.csv')
ANOTHER_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'another_model.pkl')

IMAGE_RECOG_MODEL = 'dataset/model_2.1.h5'