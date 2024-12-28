import cv2
import os
from ultralytics import YOLO

def detect_and_crop(image_path, output_dir):
    # Load YOLOv5 model (pre-trained on COCO dataset or your custom model)
    model = YOLO("yolov5s")  # Replace "yolov5s" with your trained model if needed

    # Perform object detection
    results = model(image_path)

    # Read the original image
    image = cv2.imread(image_path)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Counter for cropped images
    cropped_count = 0

    # Iterate through detected objects and crop
    for result in results:
        for box in result.boxes:  # Iterate over detected boxes
            # Get the bounding box coordinates (x1, y1, x2, y2)
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Ensure they are integers

            # Crop the image using the bounding box
            cropped_image = image[y1:y2, x1:x2]

            # Save the cropped image
            cropped_path = os.path.join(output_dir, f"cropped_{cropped_count}.jpg")
            cv2.imwrite(cropped_path, cropped_image)
            cropped_count += 1

            print(f"Cropped image saved: {cropped_path}")

    print(f"Total objects cropped: {cropped_count}")

# Input image path
image_path = "/mnt/data/Group 37.jpeg"

# Directory to save cropped images
output_dir = "./cropped_objects"

# Detect and crop rounded objects
detect_and_crop(image_path, output_dir)