import cv2
import matplotlib.pyplot as plt
import os

# Set the directory containing images and the output directory for histograms
image_directory = "input_images"
output_directory = "output_images"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Get all image files in the directory (you can adjust the extensions if needed)
image_files = [f for f in os.listdir(image_directory) if f.endswith((".png", ".jpg", ".jpeg"))]

# Loop over each image file
for image_file in image_files:
    # Read the image
    image_path = os.path.join(image_directory, image_file)
    image = cv2.imread(image_path)
    
    # Check if the image was loaded correctly
    if image is None:
        print(f"Could not load image: {image_file}")
        continue

    # Calculate the histogram for each color channel
    # b_histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
    # g_histogram = cv2.calcHist([image], [1], None, [256], [0, 256])
    r_histogram = cv2.calcHist([image], [2], None, [256], [0, 256])

    # Convert BGR to RGB for display
    r_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Set up the plot layout
    plt.rcParams["figure.figsize"] = [12, 3.8]
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.15, top=0.9)
    
    # Display the image
    plt.subplot(121)
    plt.imshow(r_image)
    plt.axis("off")
    
    # Display the histograms
    plt.subplot(122)
    # plt.plot(b_histogram, color='blue', label='blue')
    # plt.plot(g_histogram, color='green', label='green')
    plt.plot(r_histogram, color='red', label='red')
    plt.legend(loc=0)
    plt.xlabel('Brightness')
    plt.ylabel('Count')
    
    # Save the plot to the output directory with a unique name
    output_filename = os.path.join(output_directory, f"histogram_{os.path.splitext(image_file)[0]}.png")
    plt.savefig(output_filename)
    plt.close()  # Close the figure to manage memory

    print(f"Saved histogram for {image_file} as {output_filename}")
