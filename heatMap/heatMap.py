import argparse
import sys
from downloader import *
from map_recognition import *
from detect import *
from data_config import Config

# Input : URL
# download video -> extract images -> Extract map
# Deal with edges cases ?? --> Image where there are no map on the top left corner
# Recognize map --> Prepare the right Baseline
# detect images --> Transpose to the right baseline
# Construct the Heat Map


# load config
config = Config('config.yaml')

def main(url, nameFolder, sample_size = 10):
    
    # Downloading
    print(f"Downloading URL: {url} ...")

    # Define the full path to save the video
    folder_path_raw_video = os.path.join(config.get_data_path("raw_video_data"), nameFolder)
    download(url, folder_path_raw_video)

    print(f"Downloaded URL: {url} in {folder_path_raw_video}")

    # Extracting
    print("Extracting frames ...")
    # Define the full path to extract images from the video
    folder_path_extracted_frames = os.path.join(config.get_data_path("extracted_image_data"), nameFolder)
    extract_frames_from_video(f"{folder_path_raw_video}\\video.mp4", folder_path_extracted_frames)

    print(f"Frames in Input folder: {folder_path_extracted_frames}")
        
    # Processing Images - Extract map
    print("Extracting map in the top left corner ...")

    # Define the full path to extract the map from the extracted images
    folder_path_processed_images = os.path.join(config.get_data_path("processed_image_data"), nameFolder)
    process_images(folder_path_extracted_frames, folder_path_processed_images)
    
    print(f"Maps in Output folder: {folder_path_processed_images}")

    # Run map recognition
    print("Run Map Recognition ...")

    # Define the full path of baseline to compare the images
    folder_path_baseline_maps = config.get_data_path("baseline_map")
    map_study = map_recognition(folder_path_baseline_maps,folder_path_processed_images, sample_size)

    print(f"Map recognized : {map_study}")

    return 0

if __name__ == "__main__":
    # Define the command-line argument parser
    parser = argparse.ArgumentParser(description="Process a URL with Name of video.")
    """ Ex : python heatMap.py -url "https://example.com/video" -nameF "myFolder" -n 5"""
    # Add command-line arguments
    parser.add_argument("-url", required=True, help="The URL to process")
    parser.add_argument("-nameF", required=True, help="Folder to store the results")
    parser.add_argument("-n", required=False, help="Sample size for the map recognition")

    # Parse the arguments
    args = parser.parse_args()

    # Extract the arguments
    url = args.url
    nameFolder = args.nameF
    sample_size = int(args.n)

    # Print a message to show it's working
    print("Working...")

    # Call the main function with the parsed arguments
    result = main(url, nameFolder, sample_size)
    
    print(f"Result: {result}")

