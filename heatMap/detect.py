from roboflow import Roboflow
import json
from data_config import Config
from pathlib import Path
import sys
import os

def load_model(api_key):
    # load roboflow workspace
    rf = Roboflow(api_key=api_key)

    # load model
    project = rf.workspace().project("valorant-heat-map")
    model = project.version(3).model

    return model

def predict_image(model, path_image, confidence=40, overlap=30):
    # Predict image
    prediction = model.predict(path_image, confidence=confidence, overlap=overlap)
    return prediction

def save_image(prediction, path_prediction):
    prediction.save(f"{path_prediction}.jpg")

def image_to_json(prediction):
    return prediction.json()
    

def detect(image_path, prediction_path):

    config = Config("config.yaml")

    # load model
    api_key_path = config.get_data_path("roboflow_api_path")
    model = load_model(config.get_api_key_from_file(api_key_path))

    # Ensure output folder exists
    Path(prediction_path).mkdir(parents=True, exist_ok=True)
    
    # Process each image in the input folder
    for image_file in os.listdir(image_path):

        image_path = os.path.join(image_path, image_file)
        
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Predict on the image
            prediction = predict_image(model, image_path)

            # Generate output file name
            prediction_name = os.path.splitext(image_file)[0]  # Extract the file name without extension
            json_output_path = os.path.join(prediction_path, f"{prediction_name}.json")
            
            # Convert prediction to JSON and save it
            prediction_json = image_to_json(prediction)
            with open(json_output_path, "w") as json_file:
                json.dump(prediction_json, json_file, indent=4)
            