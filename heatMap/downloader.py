import os
import cv2
from PIL import Image
import subprocess

def download_youtube_video(url,output_path, name, resolution):

    full_path = os.path.join(output_path, f'{name}.mp4')
    command = [
        'yt-dlp',
        '-f', f'bestvideo[height>={resolution[:-1]}][ext=mp4]/best[ext=mp4]',
        '-o', full_path,
        url
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Downloaded video: {full_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def download(url, output_path, resolution='1080p'):

    # will be deleted afterwards
    video_name = 'video'

    # Check if the directory exists, if not, create it
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    download_youtube_video(url, output_path, video_name ,resolution)

def extract_frames_from_video(video_path, output_folder, frame_rate=1):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load the video
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    fps = vidcap.get(cv2.CAP_PROP_FPS)  # Get frames per second of the video
    print(fps)
    interval = int(fps / frame_rate)  # Calculate the interval between frames to capture
    print(f"Video FPS: {fps}, Extracting every {interval} frame(s).")
    
    while success:
        # Save frame as JPEG file
        cv2.imwrite(os.path.join(output_folder, f"frame{count:04d}.jpg"), image)
        count += interval
        # Move the frame position to the next frame to capture
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, count)
        success, image = vidcap.read()

    vidcap.release()

def extract_map(image_path, output_path, left = 50, upper = 25, map_width = 550, map_height = 550):
    """
    Extracts the top-left map portion of an image and saves it as a new .jpg file.

    Parameters:
    - image_path (str): The file path of the input image.
    - output_path (str): The file path to save the extracted map.
    - map_width (int): The width of the map to be extracted.
    - map_height (int): The height of the map to be extracted.
    """
    # Open the image
    img = Image.open(image_path)
    
    # Define the box to extract (left, upper, right, lower)
    box = (left, upper, map_width, map_height)
    
    # Crop the image to the defined box
    map_img = img.crop(box)
    
    # Save the cropped map as a new image
    map_img.save(output_path, format='JPEG')
    print(f"Map saved to {output_path}")

def process_images(input_folder, output_folder):
    """
    Processes all images in a folder, extracts the top-left map portion, and saves it in another folder.

    Parameters:
    - input_folder (str): Path to the folder containing the input images.
    - output_folder (str): Path to the folder where processed images will be saved.
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is a .jpg image
        if filename.endswith('.jpg'):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)
            
            # for now we are going to hardcode the values
            extract_map(input_image_path,output_image_path,
                        left = 50, 
                        upper = 25, 
                        map_width = 550, 
                        map_height = 550)