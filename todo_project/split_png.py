#!/usr/bin/env python
from PIL import Image
import os

# Load the 4x4 grid image
image_path = "icons.png"  # Replace with your file path
raw_image = Image.open(image_path)


# Define the area to crop (remove header and footer)
# Adjust these values based on how much space to remove
header_height = 40  # Adjust this value as needed
footer_height = 20  # Adjust this value as needed

# Calculate cropped area
left = 0
upper = header_height
right = raw_image.width
lower = raw_image.height - footer_height

# Crop the image
image = raw_image.crop((left, upper, right, lower))

# Define grid dimensions
rows, cols = 4, 4

cell_width = image.width // cols
cell_height = image.height // rows

# Create a directory to save individual images
output_dir = "./"
os.makedirs(output_dir, exist_ok=True)

# Split the image into 16 individual files

for row in range(rows):
    for col in range(cols):
        left = col * cell_width
        upper = row * cell_height
        right = left + cell_width
        lower = upper + cell_height

        # Crop the image
        cropped_image = image.crop((left, upper, right, lower))

        # Save each cropped image
        output_path = os.path.join(output_dir, f"icon_{row * cols + col + 1}.png")
        cropped_image.save(output_path)

print(f"Split the image into 16 individual files in {output_dir}")
