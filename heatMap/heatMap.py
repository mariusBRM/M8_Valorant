import argparse
import sys
from downloader import *
from map_recognition import *
from detect import *
from data_config import Config


def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def get_json_files_from_folder(folder_path):
    """Retrieve all JSON file paths from a given folder."""
    json_files = []
    
    # Loop through all files in the directory
    for file_name in os.listdir(folder_path):
        # Check if the file is a .json file
        if file_name.endswith(".json"):
            # Construct the full path to the file and add it to the list
            full_path = os.path.join(folder_path, file_name)
            json_files.append(full_path)
    
    return json_files

# Function to accumulate heat for each object in the heatmap
def add_to_heatmap(heatmap, positions):
    for (x, y, w, h) in positions:
        # Add a Gaussian kernel around the object's position
        center = (int(x), int(y))
        radius = int(max(w, h) / 2)
        cv2.circle(heatmap, center, radius, 1, -1)  # Add heat in a circular region around the object

def run_heatMap_analysis(predictions_path, base_map):

    # Assuming you have a list of JSON file paths
    json_files = get_json_files_from_folder(predictions_path)

    # Prepare containers to store the positions for each class (DFS, ATK, etc.)
    positions_DFS = []
    positions_ATK = []

    # Parse each JSON file
    for json_file in json_files:
        data = load_json(json_file)
        predictions = data['predictions']
        
        for pred in predictions:
            if pred['class'] == 'DFS':
                # Store DFS object positions
                positions_DFS.append((pred['x'], pred['y'], pred['width'], pred['height']))
            elif pred['class'] == 'ATK':
                # Store ATK object positions
                positions_ATK.append((pred['x'], pred['y'], pred['width'], pred['height']))


    # Load the baseline image (the size of the heatmap will match the baseline)
    baseline = cv2.imread(base_map)
    height, width = baseline.shape[:2]

    # Create empty heatmaps (one for each class)
    heatmap_DFS = np.zeros((height, width), dtype=np.float32)
    heatmap_ATK = np.zeros((height, width), dtype=np.float32)

    # Accumulate positions for DFS
    add_to_heatmap(heatmap_DFS, positions_DFS)

    # Accumulate positions for ATK
    add_to_heatmap(heatmap_ATK, positions_ATK)


    # Normalize heatmaps to range [0, 255]
    heatmap_DFS = np.uint8(255 * heatmap_DFS / np.max(heatmap_DFS))
    heatmap_ATK = np.uint8(255 * heatmap_ATK / np.max(heatmap_ATK))

    # Apply color maps (e.g., cv2.COLORMAP_JET for better visualization)
    color_map_DFS = cv2.applyColorMap(heatmap_DFS, cv2.COLORMAP_JET)
    color_map_ATK = cv2.applyColorMap(heatmap_ATK, cv2.COLORMAP_HOT)


    # Overlay DFS heatmap with some transparency (e.g., alpha blending)
    overlayed_DFS = cv2.addWeighted(baseline, 0.7, color_map_DFS, 0.3, 0)

    # Overlay ATK heatmap (you can do both separately or combine them)
    overlayed_ATK = cv2.addWeighted(baseline, 0.7, color_map_ATK, 0.3, 0)

    # Optionally, combine DFS and ATK into a single image
    combined_heatmap = cv2.addWeighted(color_map_DFS, 0.5, color_map_ATK, 0.5, 0)
    overlayed_combined = cv2.addWeighted(baseline, 0.7, combined_heatmap, 0.3, 0)

    # Save or display the final heatmap overlay on the baseline image
    cv2.imwrite('heatmap_DFS.jpg', overlayed_DFS)
    cv2.imwrite('heatmap_ATK.jpg', overlayed_ATK)
    cv2.imwrite('heatmap_combined.jpg', overlayed_combined)

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

    # Aligning with Baseline
    print(f"Aligning with {map_study} format.")

    align_maps(map_study, folder_path_processed_images)

    print(f"All maps in {folder_path_processed_images} aligned with {map_study} format.")

    # Run detection
    print("Run detection...")

    detect(folder_path_processed_images, f"{config.get_data_path("prediction_data")}\\{nameFolder}")

    print("Prediction Completed.")

    # Run HeatMap Analysis
    print("Run HeatMap Analysis ...")

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

