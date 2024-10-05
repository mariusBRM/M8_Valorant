from roboflow import Roboflow
import sys
import os

# import roboflow API
# rf = Roboflow(api_key="xEb6a3dXc9T0RuJ5Qnox")
# project = rf.workspace().project("valorant-heat-map")

# # m
# model = project.version(3).model

def load_model():
    # load API KEY
    api_key = os.getenv('API_KEY_ROBOFLOW')
    rf = Roboflow(api_key=api_key)

    # load model
    project = rf.workspace().project("valorant-heat-map")
    model = project.version(3).model

    return model

def predict_image(model, path_image):

    # Predict image
    
    return 0


def main():

    # load model
    model = load_model()

    # predict
    

if __name__ == "__main__":
    main()