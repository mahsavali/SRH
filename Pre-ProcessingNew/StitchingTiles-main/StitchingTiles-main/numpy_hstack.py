import os
import pydicom
import numpy as np
from PIL import Image

def read_dcm_images_from_directory(directory_path):
    image_files = [f for f in os.listdir(directory_path) if f.endswith(".dcm")]
    if not image_files:
        print("No DICOM files found in the directory.")
        return None

    dcm_images = []
    for file_name in image_files:
        file_path = os.path.join(directory_path, file_name)
        try:
            dataset = pydicom.dcmread(file_path)
            image_array = dataset.pixel_array
            dcm_images.append(image_array)
        except Exception as e:
            print(f"Error reading '{file_name}': {e}")
    return dcm_images

def merge_images(images):
    merged_image = np.hstack(images)
    return merged_image

def save_as_jpg(image, output_path):
    image_normalized = (image - np.min(image)) * (255.0 / (np.max(image) - np.min(image)))
    image_8bit = np.uint8(image_normalized)
    pil_image = Image.fromarray(image_8bit)
    pil_image.save(output_path, format='JPEG')


input_dir = "res"
output_path = "output_numpy.jpg"
dicom_images = read_dcm_images_from_directory(input_dir)
if dicom_images:
    merged_image = merge_images(dicom_images)
    
    save_as_jpg(merged_image, output_path)
    print("Merged image saved successfully as JPEG.")
