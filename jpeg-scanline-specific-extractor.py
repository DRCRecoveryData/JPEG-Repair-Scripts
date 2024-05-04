import os
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO)

def extract_scanline(image_path, scanline_index):
    try:
        # Open the image file
        image = Image.open(image_path)

        # Get image size
        image_width, image_height = image.size

        # Calculate MCU size (assuming standard JPEG with 8x8 MCU blocks)
        mcu_width = 8
        mcu_height = 8

        # Validate scanline_index to be within image bounds
        max_scanlines = image_height // mcu_height
        if scanline_index >= max_scanlines:
            raise ValueError("Scanline index exceeds image height.")

        # Calculate the starting and ending y-coordinates of the scanline
        scanline_start = scanline_index * mcu_height
        scanline_end = (scanline_index + 1) * mcu_height

        # Crop the scanline
        scanline_box = (0, scanline_start, image_width, scanline_end)
        scanline_image = image.crop(scanline_box)

        # Generate output file name with the index of the scanline
        file_name = os.path.splitext(os.path.basename(image_path))[0]  # Extract filename without extension
        output_file_name = f"{file_name}_scanline_{scanline_index}.jpg"
        output_file_path = os.path.join(os.path.dirname(image_path), output_file_name)

        # Save the extracted scanline to a new file
        scanline_image.save(output_file_path)
        logging.info(f"Scanline {scanline_index} has been extracted and saved to: {output_file_path}")
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)

def main():
    try:
        # Prompt user for JPEG file path
        jpeg_file_path = input("Enter the path to the JPEG file: ")

        # Prompt user for the index of the scanline to extract
        scanline_index = int(input("Enter the index of the scanline to extract: "))

        # Validate input image file path
        if not os.path.isfile(jpeg_file_path):
            raise FileNotFoundError("Input image file not found.")

        # Extract the specified scanline and save it to a new file in the same directory as the input file
        extract_scanline(jpeg_file_path, scanline_index)
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)

if __name__ == "__main__":
    main()
