import os
import glob
import pydicom
import ashlar
from PIL import Image

dcm_files = glob.glob(os.path.join("res", "*.dcm"))
dcm_files.sort()


dcm_images = [pydicom.dcmread(file) for file in dcm_files]


pil_images = [Image.fromarray(image.pixel_array) for image in dcm_images]


# merged_image = ashlar.....

widths, heights = zip(*(i.size for i in pil_images))

total_width = sum(widths)
max_height = max(heights)

new_image = Image.new('RGB', (total_width, max_height))

x_offset = 0
for image in pil_images:
    new_image.paste(image, (x_offset, 0))
    x_offset += image.width

new_image.save('output_basic.jpg')
