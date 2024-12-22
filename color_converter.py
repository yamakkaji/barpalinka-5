#%%
import cv2
import numpy as np
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("-i", "--image", type=str, required=True, default="assets/images/BarPalinkaCounter.png")

# args = vars(parser.parse_args())

img = cv2.imread("assets/images/BarPalinkaCounter.png")
img = img / 255
# 8bit color
img = (img * 254).astype(np.uint8) + 1

# Output the image
cv2.imwrite("assets/images/BarPalinkaCounter_8bit.png", img)
# %%
