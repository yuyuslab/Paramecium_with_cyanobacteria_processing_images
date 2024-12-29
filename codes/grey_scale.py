import cv2

# black = "../input_images/red_grey_scale/red_black.png"
# red = "../input_images/red_grey_scale/red_bright.png"
# middle = "../input_images/red_grey_scale/red_middle.png"


# black_image = cv2.imread(black)
# red_image = cv2.imread(red)
# middle_image = cv2.imread(middle)


# black_channel = black_image[:, :, 2]
# red_channel = red_image[:, :, 2]
# middle_channel = middle_image[:, :, 2]

# print(black_channel)
# print(red_channel)
# print(middle_channel)

import cv2
import numpy as np

# File paths for the cropped images
cropped_img1_path = "../input_images/zourimushi_data/1029_cropped/6803/0.1/画像_12037.jpg"
cropped_img2_path = "../input_images/zourimushi_data/1029_cropped/6803/0.1/画像_12037.png"

# Load the images and extract the red channel
cropped_img1 = cv2.imread(cropped_img1_path)[:, :, 2]
# cropped_img2 = cv2.imread(cropped_img2_path)[:, :, 2]
filtered_img1 = cropped_img1[cropped_img1 != 0]
# File path for the output text file
# output_txt_path1 = "../outputs_csv/cropped_img1_full.txt"
# output_txt_path2 = "../outputs_csv/cropped_img2_full.txt"
output_txt_path3 = "../outputs_csv/filtered_img1_full.txt"

# Save the full data to text files
# np.savetxt(output_txt_path1, cropped_img1, fmt="%d", delimiter=",")
# np.savetxt(output_txt_path2, cropped_img2, fmt="%d", delimiter=",")
np.savetxt(output_txt_path3, filtered_img1, fmt="%d", delimiter=",")

# print(f"Full results saved to {output_txt_path1} and {output_txt_path2}")