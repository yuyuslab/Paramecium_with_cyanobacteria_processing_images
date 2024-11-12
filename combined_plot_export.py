import cv2
import matplotlib.pyplot as plt
import os
import math

# Set the directory containing images and the output directory for histograms
image_directory = "input_images"
output_directory = "output_images"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Get all image files in the directory (you can adjust the extensions if needed)
image_files = [f for f in os.listdir(image_directory) if f.endswith((".png", ".jpg", ".jpeg"))]

# Set up the number of rows and columns for the grid
num_images = len(image_files)
cols = 2  # One column for the image and one for its histogram
rows = math.ceil(num_images)  # One row per image

# Create a new figure for all images and histograms
plt.figure(figsize=(10, 5 * num_images))  # Adjust height for more images

# Loop over each image file
for idx, image_file in enumerate(image_files):
    # Read the image
    image_path = os.path.join(image_directory, image_file)
    image = cv2.imread(image_path)
    
    # Check if the image was loaded correctly
    if image is None:
        print(f"Could not load image: {image_file}")
        continue

    # Calculate the red channel histogram
    r_histogram = cv2.calcHist([image], [2], None, [256], [0, 256])

    # Convert BGR to RGB for display
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Plot the image
    plt.subplot(num_images, cols, idx * 2 + 1)
    plt.imshow(rgb_image)
    plt.axis("off")
    plt.title(f"Image: {image_file}")

    # Plot the histogram
    plt.subplot(num_images, cols, idx * 2 + 2)
    plt.plot(r_histogram, color='red', label='Red Channel')
    plt.legend(loc='upper right')
    plt.xlabel('Brightness')
    plt.ylabel('Count')
    plt.title("Red Channel Histogram")

# Save the combined plot to the output directory
output_filename = os.path.join(output_directory, "combined_histograms.png")
plt.tight_layout()
plt.savefig(output_filename)
plt.close()  # Close the figure to free up memory

print(f"Saved combined histograms as {output_filename}")
