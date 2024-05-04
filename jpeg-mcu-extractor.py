import os
import sys
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO)

def extract_mcus_from_scanline(image_path, num_mcus):
    try:
        # Open the image file
        image = Image.open(image_path)

        # Get image size
        image_width, image_height = image.size

        # Calculate MCU size (assuming standard JPEG with 8x8 MCU blocks)
        mcu_width = 8
        mcu_height = 8

        # Validate num_mcus to be within image bounds
        max_mcus = image_width // mcu_width
        if num_mcus > max_mcus:
            raise ValueError("Number of MCU blocks exceeds image width.")

        # Create a new image to store the extracted MCU blocks
        mcu_image = Image.new('RGB', (num_mcus * mcu_width, mcu_height))

        # Extract the specified number of MCU blocks from the first scanline
        for i in range(num_mcus):
            mcu_x = i * mcu_width
            mcu_box = (mcu_x, 0, mcu_x + mcu_width, mcu_height)
            mcu_block = image.crop(mcu_box)
            mcu_image.paste(mcu_block, (mcu_x, 0))

        # Generate output file name with the number of MCU blocks
        file_name = os.path.splitext(os.path.basename(image_path))[0]  # Extract filename without extension
        output_file_name = f"{file_name}_mcus_{num_mcus}.JPG"
        output_file_path = os.path.join(os.path.dirname(image_path), output_file_name)

        # Save the combined MCU blocks to a single file in the same directory as the input image
        mcu_image.save(output_file_path)
        logging.info(f"{num_mcus} MCU blocks from the first scanline have been extracted and saved to: {output_file_path}")
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)

def main():
    try:
        # Prompt user for JPEG file path
        jpeg_file_path = input("Enter the path to the JPEG file: ")

        # Prompt user for the number of MCU blocks to extract
        num_mcus = int(input("Enter the number of MCU blocks to extract: "))

        # Validate input image file path
        if not os.path.isfile(jpeg_file_path):
            raise FileNotFoundError("Input image file not found.")

        # Extract MCU blocks from the first scanline and save them in the same directory as the input image
        extract_mcus_from_scanline(jpeg_file_path, num_mcus)
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)

if __name__ == "__main__":
    main()
