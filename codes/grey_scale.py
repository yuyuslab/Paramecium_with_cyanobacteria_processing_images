import cv2

black = "../input_images/red_grey_scale/red_black.png"
red = "../input_images/red_grey_scale/red_bright.png"
middle = "../input_images/red_grey_scale/red_middle.png"


black_image = cv2.imread(black)
red_image = cv2.imread(red)
middle_image = cv2.imread(middle)


black_channel = black_image[:, :, 2]
red_channel = red_image[:, :, 2]
middle_channel = middle_image[:, :, 2]

print(black_channel)
print(red_channel)
print(middle_channel)
