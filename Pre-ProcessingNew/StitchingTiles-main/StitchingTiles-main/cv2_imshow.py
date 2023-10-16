# import cv2
# from PIL import Image

# def open_and_show_tiff(file_path):
#     try:
#         image = cv2.imread(file_path)
#         if image is not None:
#             print(image.shape)
#             screen_res = 1200, 600 
#             scale = min(screen_res[0] / image.shape[1], screen_res[1] / image.shape[0])

#             resized_image = cv2.resize(image, None, fx=scale, fy=scale)

#             img = Image.open(file_path)
#             # img.show()
#             cv2.imshow("TIFF Image", resized_image)
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()
#         else:
#             print("Unable to open or display the TIFF file.")
#     except Exception as e:
#         print(f"Error opening or displaying the TIFF file: {e}")

# tiff_file_path = "output/img_1_4.tif"
# # tiff_file_path = "output.ome.tif"
# # tiff_file_path = "res/temp_tiff_output/img4_1.tif"
# open_and_show_tiff(tiff_file_path)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Specify the path to your TIF image
# image_path = 'res/temp_tiff_output/cycle_4/img4_1.tif'
image_path = "output.ome.tif"

# Load the TIF image using matplotlib
img = mpimg.imread(image_path)
print(img.shape)
# Display the image using matplotlib
plt.imshow(img)
plt.axis('off')  # Turn off axis labels
plt.show()