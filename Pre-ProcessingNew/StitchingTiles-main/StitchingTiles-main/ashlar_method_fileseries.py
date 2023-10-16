import subprocess
import os
import glob
from PIL import Image
import pydicom
import shutil

def get_image_size(path):
    with Image.open(path) as tiff:
        return tiff.size

def convert_dicom_to_tiff(base_filename, dicom_path, output_dir, index):
    tiff_files = []
    try:
        ds = pydicom.dcmread(dicom_path)
        image = Image.fromarray(ds.pixel_array)

        width, height = image.size
        piece_width, piece_height = 1000, 1000
        for i in range(0, width, piece_width):
            for j in range(0, height, piece_height):
                piece = image.crop((i, j, i + piece_width, j + piece_height))
                row_no = j//piece_height + 1
                piece_name = f"{base_filename}_t00{row_no}_{index}.tif"
                piece_path = os.path.join(output_dir, f"cycle_{row_no}", piece_name)
                piece.save(piece_path)
                tiff_files.append(piece_path)

    except Exception as e:
        print(f"Error processing '{dicom_path}': {e}")
    return tiff_files

def merge_tiff_files(files_dir, output_dir, tiff_files, overlap=0.15, width=1000, height=1000):
    tiff_output = os.path.join(output_dir, "output.ome.tif")
    
    tiff_command = [
        "ashlar",
        "-o",
        tiff_output,
        f"fileseries|{files_dir}\\cycle_1" +  "|pattern=img4_t001_{series:1}.tif" + f"|overlap={overlap}|width={width}|height={height}|direction=horizontal",
        f"fileseries|{files_dir}\\cycle_2" +  "|pattern=img4_t002_{series:1}.tif" + f"|overlap={overlap}|width={width}|height={height}|direction=horizontal",
        f"fileseries|{files_dir}\\cycle_3" +  "|pattern=img4_t003_{series:1}.tif" + f"|overlap={overlap}|width={width}|height={height}|direction=horizontal",
        f"fileseries|{files_dir}\\cycle_4" +  "|pattern=img4_t004_{series:1}.tif" + f"|overlap={overlap}|width={width}|height={height}|direction=horizontal",
    ]
    tiff_command.extend(tiff_files)
    tiff_command.append("--filter-sigma")
    tiff_command.append("1")

    try:
        subprocess.run(tiff_command, check=True)
        convert_to_jpeg_and_save_output(output_dir, tiff_output)
        print("Merged image saved as JPEG successfully.")
    except subprocess.CalledProcessError as e:
        print("Error while running ashlar:", e)

def convert_to_jpeg_and_save_output(output_dir, tiff_output):
    with Image.open(tiff_output) as tiff_image:
        tiff_image_8bit = tiff_image.convert("L")
    jpeg_output = os.path.join(output_dir, "output_ashlar.jpg")
    tiff_image_8bit.save(jpeg_output, "JPEG")


input_dir = "res"
output_dir = ""
temp_dir = os.path.join(input_dir, "temp_tiff_output")
os.makedirs(temp_dir, exist_ok=True)

temp_cycle_dir = os.path.join(temp_dir, "cycle_1")
os.makedirs(temp_cycle_dir, exist_ok=True)
temp_cycle_dir = os.path.join(temp_dir, "cycle_2")
os.makedirs(temp_cycle_dir, exist_ok=True)
temp_cycle_dir = os.path.join(temp_dir, "cycle_3")
os.makedirs(temp_cycle_dir, exist_ok=True)
temp_cycle_dir = os.path.join(temp_dir, "cycle_4")
os.makedirs(temp_cycle_dir, exist_ok=True)

tiff_files = []

for index, dicom_file in enumerate(os.listdir(input_dir), start=1):
    if dicom_file.endswith(".dcm"):
        dicom_path = os.path.join(input_dir, dicom_file)
        base_filename = dicom_file.split("_")[0]
        tiff_files += convert_dicom_to_tiff(base_filename, dicom_path, temp_dir, index)

merge_tiff_files(temp_dir, output_dir, tiff_files, overlap=0.10)
# Clean up: Delete the temporary directory and its contents
shutil.rmtree(temp_dir)
