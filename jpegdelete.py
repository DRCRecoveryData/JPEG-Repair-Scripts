import sys
import math
from PIL import Image

def delete_mcu(image, dest_row, dest_col, n):
    width, height = image.size
    block_size = 8  # Assuming block size of 8x8 for simplicity
    
    dest_x = dest_col * block_size
    dest_y = dest_row * block_size
    
    # Calculate the coordinates of the block to delete
    block_x = dest_x + (n * block_size)
    block_y = dest_y + (n * block_size)
    
    # Ensure the block coordinates are within the image bounds
    if block_x >= width or block_y >= height:
        print("Error: Block position is out of bounds.")
        return
    
    # Calculate the range of pixels to delete
    x_range = range(block_x, min(block_x + block_size, width))
    y_range = range(block_y, min(block_y + block_size, height))
    
    # Replace the block with the next block in the same row
    for y in y_range:
        for x in x_range:
            next_block_x = block_x + block_size
            if next_block_x < width:
                pixel = image.getpixel((next_block_x, y))
                image.putpixel((x, y), pixel)
            else:
                # If the next block is out of bounds, just set the pixel to black
                image.putpixel((x, y), (0, 0, 0))
                
def main():
    if len(sys.argv) < 6:
        print("Usage: python jpegrepair.py infile.jpg outfile.jpg dest dest_row dest_col delete N")
        sys.exit(1)
    
    infile = sys.argv[1]
    outfile = sys.argv[2]
    dest_row = int(sys.argv[4])
    dest_col = int(sys.argv[5])
    n = int(sys.argv[7])
    
    try:
        image = Image.open(infile)
    except FileNotFoundError:
        print("Error: Input file not found.")
        sys.exit(1)
    
    delete_mcu(image, dest_row, dest_col, n)
    
    try:
        image.save(outfile)
    except:
        print("Error: Failed to save output file.")
        sys.exit(1)
        
    print("MCU deleted successfully.")

if __name__ == "__main__":
    main()
