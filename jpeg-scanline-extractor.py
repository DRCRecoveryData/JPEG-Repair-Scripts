import os
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO)

def extract_scanlines(image_path, num_scanlines):
    try:
        # Open the image file
        image = Image.open(image_path)

        # Get image size
        image_width, image_height = image.size

        # Calculate MCU size (assuming standard JPEG with 8x8 MCU blocks)
        mcu_width = 8
        mcu_height = 8

        # Validate num_scanlines to be within image bounds
        max_scanlines = image_height // mcu_height
        if num_scanlines > max_scanlines:
            raise ValueError("Number of scanlines exceeds image height.")

        # Create a new image to store the extracted scanlines
        extracted_image = Image.new('RGB', (image_width, mcu_height * num_scanlines))

        # Extract the specified number of scanlines
        for i in range(num_scanlines):
            scanline_box = (0, i * mcu_height, image_width, (i + 1) * mcu_height)
            scanline_image = image.crop(scanline_box)
            extracted_image.paste(scanline_image, (0, i * mcu_height))

        # Generate output file name with the number of scanlines
        file_name = os.path.splitext(os.path.basename(image_path))[0]  # Extract filename without extension
        output_file_name = f"{file_name}_scanlines_{num_scanlines}.jpg"
        output_file_path = os.path.join(os.path.dirname(image_path), output_file_name)

        # Save the combined scanlines to a single file
        extracted_image.save(output_file_path)
        logging.info(f"{num_scanlines} scanlines have been extracted and saved to: {output_file_path}")
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)

def main():
    try:
        # Prompt user for JPEG file path
        jpeg_file_path = input("Enter the path to the JPEG file: ")

        # Prompt user for the number of scanlines to extract
        num_scanlines = int(input("Enter the number of scanlines to extract: "))

        # Validate input image file path
        if not os.path.isfile(jpeg_file_path):
            raise FileNotFoundError("Input image file not found.")

        # Extract scanlines and save them with auto-generated output file name
        extract_scanlines(jpeg_file_path, num_scanlines)
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)

if __name__ == "__main__":
    main()
