import argparse
import sys
from downloader import *
from map_recognition import *
from detect import *

# Input : URL
# download video -> extract images -> Extract map
# Deal with edges cases ?? --> Image where there are no map on the top left corner
# Recognize map --> Prepare the right Baseline
# detect images --> Transpose to the right baseline
# Construct the Heat Map


import argparse
import sys

def main(url, input_folder, output_folder):
    # Your main logic goes here
    print(f"Processing URL: {url}")
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")
    # Simulate doing some work
    result = "Success"
    return result

if __name__ == "__main__":
    # Define the command-line argument parser
    parser = argparse.ArgumentParser(description="Process a URL with input and output folder paths.")

    # Add command-line arguments
    parser.add_argument("-url", required=True, help="The URL to process")
    parser.add_argument("-inputF", required=True, help="Path to the input folder")
    parser.add_argument("-o", required=True, help="Path to the output folder")

    # Parse the arguments
    args = parser.parse_args()

    # Extract the arguments
    url = args.url
    input_folder = args.inputF
    output_folder = args.o

    # Print a message to show it's working
    print("Working...")

    # Call the main function with the parsed arguments
    result = main(url, input_folder, output_folder)
    
    print(f"Result: {result}")

