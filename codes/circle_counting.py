import cv2
import numpy as np

def count_cyanobacteria(image_path):
  # Read the image
  img = cv2.imread(image_path)

  # Convert the image to grayscale
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Apply thresholding to isolate the red circles
  _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

  # Find contours of the red circles
  contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Count the number of contours
  num_cyanobacteria = len(contours)

  return num_cyanobacteria

# Example usage:
image_path = "/Users/yujirokisu/Documents/devs/processing_images/cyanos/画像_13101.jpg"
count = count_cyanobacteria(image_path)
print("Number of cyanobacteria:", count)