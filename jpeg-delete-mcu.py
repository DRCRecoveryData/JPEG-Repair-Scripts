import os
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO)

def delete_mcus_from_scanline(image_path, num_mcus_to_delete):
    try:
        # Open the image file
        image = Image.open(image_path)

        # Get image size
        image_width, image_height = image.size

        # Calculate MCU size (assuming standard JPEG with 8x8 MCU blocks)
        mcu_width = 8
        mcu_height = 8

        # Validate num_mcus_to_delete to be within image bounds
        max_mcus = image_width // mcu_width
        if num_mcus_to_delete > max_mcus:
            raise ValueError("Number of MCU blocks to delete exceeds image width.")

        # Calculate the width of the new image after deleting MCU blocks
        new_image_width = image_width - num_mcus_to_delete * mcu_width

        # Create a new image to store the modified image data
        new_image = Image.new('RGB', (new_image_width, image_height))

        # Copy MCU blocks to the new image, excluding the specified number of MCU blocks
        x_offset = 0
        for i in range(max_mcus):
            if i >= num_mcus_to_delete:
                mcu_box = (i * mcu_width, 0, (i + 1) * mcu_width, mcu_height)
                mcu_block = image.crop(mcu_box)
                new_image.paste(mcu_block, (x_offset, 0))
                x_offset += mcu_width

        # Generate output file name
        file_name = os.path.splitext(os.path.basename(image_path))[0]
        output_file_name = f"{file_name}_removed_mcus_{num_mcus_to_delete}.jpg"
        output_file_path = os.path.join(os.path.dirname(image_path), output_file_name)

        # Save the modified image
        new_image.save(output_file_path)

        logging.info(f"{num_mcus_to_delete} MCU blocks have been removed from the first scanline and the modified image has been saved to: {output_file_path}")
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)

def main():
    try:
        # Prompt user for JPEG file path
        jpeg_file_path = input("Enter the path to the JPEG file: ")

        # Prompt user for the number of MCU blocks to delete
        num_mcus_to_delete = int(input("Enter the number of MCU blocks to delete: "))

        # Validate input image file path
        if not os.path.isfile(jpeg_file_path):
            raise FileNotFoundError("Input image file not found.")

        # Delete MCU blocks from the first scanline
        delete_mcus_from_scanline(jpeg_file_path, num_mcus_to_delete)
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)

if __name__ == "__main__":
    main()
