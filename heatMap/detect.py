from roboflow import Roboflow
from data_config import Config
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
    

def main():
    
    config = Config("config.yaml")
    # load model
    api_key_path = config.get_data_path("roboflow_api_path")
    model = load_model(config.get_api_key_from_file(api_key_path))

    # predict

    

if __name__ == "__main__":
    main()