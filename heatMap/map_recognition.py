import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.cluster import KMeans
import seaborn as sns

""" This file has all the function to recognize the map that is being studied !"""


def resize_img_to_baseline(baseline, img):

    # Step 1: Preprocessing
    # Resize the blurred image to match the baseline image size if necessary
    baseline_height, baseline_width = baseline.shape[:2]

    # Resize the blurred image to fit the baseline's width while maintaining aspect ratio
    blurred_image_resized = cv2.resize(img, (baseline_width, int(img.shape[0] * (baseline_width / img.shape[1]))))

    # If the resized blurred image height is larger than the baseline, adjust the height as well
    if blurred_image_resized.shape[0] > baseline_height:
        blurred_image_resized = cv2.resize(blurred_image_resized, (baseline_width, baseline_height))
    
    return blurred_image_resized

#region ORB methods : (Oriented FAST and Rotated BRIEF)

def compute_resemblance(baseline, img, resizing=True):
    """ Compute score based on the number of matches"""
    # Load images
    img1 = cv2.imread(baseline, 0)  # Query image (known map)
    img2 = cv2.imread(img, 0)  # Test image (image you uploaded)

    if resizing:
        img2_resized = resize_img_to_baseline(img1,img2)
    else:
        img2_resized = img2

    # Initiate ORB detector
    orb = cv2.ORB_create()

    # Find keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2_resized, None)

    # Create BFMatcher object with Hamming distance
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(des1, des2)

    # Sort matches by distance (optional, but helps if you want the best matches)
    matches = sorted(matches, key=lambda x: x.distance)

    # Get number of matches and similarity score
    num_matches = len(matches)  # Total number of matches
    total_keypoints = min(len(kp1), len(kp2))  # Take the minimum number of keypoints from both images

    # Ratio of matches to keypoints
    if total_keypoints > 0:
        similarity_ratio = num_matches / total_keypoints
    else:
        similarity_ratio = 0  # Avoid division by zero

    # Display results
    # print(f"Total Matches: {num_matches}")
    # print(f"Total Keypoints in Query Image: {len(kp1)}")
    # print(f"Total Keypoints in Test Image: {len(kp2)}")
    # print(f"Similarity Ratio: {similarity_ratio:.2f}")

    return similarity_ratio, baseline


def compute_adjusted_resemblance(baseline, img, resizing=True):
    """ Compute score based on the matched and the quality (the distance)"""
    # Load the images
    img1 = cv2.imread(baseline, 0)  # Query image (known map)
    img2 = cv2.imread(img, 0)  # Test image (image you uploaded)

    if resizing:
        img2_resized = resize_img_to_baseline(img1,img2)
    else:
        img2_resized = img2

    # Initiate ORB detector
    orb = cv2.ORB_create()

    # Find keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2_resized, None)

    # Create BFMatcher object (for KNN matcher)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    # Find the top 2 matches for each keypoint (KNN matching)
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test to find good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Number of good matches
    num_good_matches = len(good_matches)

    # Additional scoring metrics
    # Average distance of good matches
    if num_good_matches > 0:
        avg_distance = np.mean([m.distance for m in good_matches])
    else:
        avg_distance = float('inf')  # Handle case with no good matches

    # Similarity score based on good matches and average distance
    similarity_score = num_good_matches / (len(kp1) + len(kp2))  # Normalized score
    adjusted_score = similarity_score / (1 + avg_distance / 100)  # Adjust based on distance (tune the factor)

    # Display results
    # print(f"Total Keypoints in Query Image: {len(kp1)}")
    # print(f"Total Keypoints in Test Image: {len(kp2)}")
    # print(f"Good Matches: {num_good_matches}")
    # print(f"Average Distance of Good Matches: {avg_distance:.2f}")
    # print(f"Similarity Score: {similarity_score:.4f}")
    # print(f"Adjusted Similarity Score: {adjusted_score:.4f}")

    return adjusted_score, baseline


def compute_ransac_homographic_resemblance(baseline, img, resizing=True):
    """ Compute score based on the number of matches and the quality of the match with homographic transformation to be more robust"""
    similarity_score = 0
    # Load the images
    baseline_image = cv2.imread(baseline, cv2.IMREAD_COLOR)
    blurred_image = cv2.imread(img, cv2.IMREAD_COLOR)

    if resizing:
        # add preprocessing
        blurred_image_resized = resize_img_to_baseline(baseline_image,blurred_image)
    else:
        blurred_image_resized = blurred_image

    # Step 2: Feature Detection
    orb = cv2.ORB_create()
    kp_baseline, des_baseline = orb.detectAndCompute(baseline_image, None)
    kp_blurred, des_blurred = orb.detectAndCompute(blurred_image_resized, None)

    # Step 3: Feature Matching
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)  # Cross-check is false to use KNN
    matches = bf.knnMatch(des_baseline, des_blurred, k=2)

    # Step 4: Ratio test to filter good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:  # Lowe's ratio test
            good_matches.append(m)

    # Step 5: Geometric verification using RANSAC to find the homography
    if len(good_matches) >= 4:  # Need at least 4 matches to compute homography
        src_pts = np.float32([kp_baseline[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp_blurred[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Compute the homography
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # Step 6: Determine if the images match
        matches_mask = mask.ravel().tolist()
        num_good_matches = sum(matches_mask)
        similarity_score = num_good_matches / len(good_matches)  # Calculate a similarity score

        # print(f"Total Good Matches: {num_good_matches}")
        # print(f"Total Matches: {len(good_matches)}")
        # print(f"Similarity Score: {similarity_score:.2f}")
    
    return similarity_score, baseline

#endregion 

#region IOU with K-NN - To finish

def visualize_segmented_image_and_distribution(image, segmented_image, kmeans,k):

    # Visualize the original and segmented images
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].imshow(image)
    ax[0].set_title("Original Image")
    ax[0].axis("off")

    ax[1].imshow(segmented_image)
    ax[1].set_title(f"Segmented Image with {k} clusters")
    ax[1].axis("off")

    plt.show()

    # Create a seaborn plot of cluster distribution
    sns.countplot(x=kmeans.labels_)
    plt.title("Cluster Distribution")
    plt.show()

def segment_image_K_NN(study_img, k=3, visualize=False):
    """ Calculate the segmented image based on the image and the number of class k"""
    image = cv2.imread(study_img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to a 2D array of pixels
    pixels = image.reshape(-1, 3)

    # Perform k-means clustering to cluster pixels by color
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)

    # Replace each pixel's color with its corresponding cluster's centroid color
    segmented_image = kmeans.cluster_centers_[kmeans.labels_]
    segmented_image = segmented_image.reshape(image.shape)
    segmented_image = segmented_image.astype(np.uint8)

    if visualize:
        visualize_segmented_image_and_distribution(image, segmented_image, kmeans,k)

    return image, segmented_image

def get_mask(image, kmeans, cluster):
    """ Display only the mask of one cluster after K-NN is performed on image """

    pixels = image.reshape(-1, 3)
    
    # Create a mask where only 1 cluster is visible
    first_cluster_mask = (kmeans.labels_ == cluster)

    # Set all other pixels to black
    only_first_cluster = np.zeros_like(pixels)
    only_first_cluster[first_cluster_mask] = kmeans.cluster_centers_[0]

    # Reshape to the original image shape
    only_first_cluster_image = only_first_cluster.reshape(image.shape).astype(np.uint8)

    # Visualize the original and the first cluster image
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].imshow(image)
    ax[0].set_title("Original Image")
    ax[0].axis("off")

    ax[1].imshow(only_first_cluster_image)
    ax[1].set_title(f"Only Cluster {cluster})")
    ax[1].axis("off")

    plt.show()

#endregion

def find_map(baseline_folder, study_img, resizing = True, compute_type='Default'):
    """ Find the map under study based on resemblance
        compute_type can take 3 values : 'Default', 'Adjusted' or 'Homographic' """
    baseline_img_paths = []

    # Loop through all the files in the baseline folder
    for filename in os.listdir(baseline_folder):
        if filename.endswith(".jpg"):
            # Construct the full file path
            file_path = os.path.join(baseline_folder, filename)

            baseline_img_paths.append(file_path)

    if compute_type == 'Default':
        # compute resemblance and store each scores
        return [compute_resemblance(base_map, study_img, resizing) for base_map in baseline_img_paths]
    
    if compute_type == 'Adjusted':
        # compute resemblance and store each scores
        return [compute_adjusted_resemblance(base_map, study_img, resizing) for base_map in baseline_img_paths]
    
    if compute_type == 'Homographic':
        # compute resemblance and store each scores
        return [compute_ransac_homographic_resemblance(base_map, study_img, resizing) for base_map in baseline_img_paths]
    
def find_sample_of_maps(baseline_folder, study_folder, sample_size=1, resizing=True, compute_type='Default'):
    """
    Selects a sample of images from the study_folder, compares them with all the baseline images from the baseline_folder,
    and computes the average resemblance score for each baseline map based on the sample size.
    
    Parameters:
    - baseline_folder: Path to the folder containing baseline maps.
    - study_folder: Path to the folder containing study images.
    - sample_size: Number of images to sample from the study folder for comparison.
    
    Returns:
    - A dictionary where keys are the baseline maps and values are the average resemblance scores.
    """
    
    # Get list of all baseline and study images
    baseline_images = [os.path.join(baseline_folder, f) for f in os.listdir(baseline_folder) if f.endswith('.jpg')]
    study_images = [os.path.join(study_folder, f) for f in os.listdir(study_folder) if f.endswith('.jpg')]
    
    # Ensure sample size does not exceed number of study images
    sample_size = min(sample_size, len(study_images))
    
    # Randomly select study images for comparison
    sample_study_images = random.sample(study_images, sample_size)
    
    # Initialize a dictionary to store cumulative resemblance scores for each baseline map
    resemblance_scores = {os.path.basename(baseline_img): [] for baseline_img in baseline_images}
    
    # Go through the selected study images
    for study_img in sample_study_images:
        # Call find_map for each study image and get the resemblance scores for all baseline maps
        image_results = find_map(baseline_folder, study_img, resizing, compute_type)
        
        # Update the resemblance scores for each baseline map
        for adjusted_score, baseline_image in image_results:
            baseline_map_name = os.path.basename(baseline_image)  # Extract the map name
            resemblance_scores[baseline_map_name].append(adjusted_score)  # Add the score to the list
    
    # Compute the average resemblance score for each baseline map
    average_scores = {}
    for baseline_map, scores in resemblance_scores.items():
        if scores:  # Make sure there are scores to average
            average_scores[baseline_map] = sum(scores) / len(scores)
        else:
            average_scores[baseline_map] = None  # No comparison was made for this baseline map
    
    return average_scores

