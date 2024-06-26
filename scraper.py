import os
import shutil
from PIL import Image
import imagehash

def create_category_folders(base_folder, categories):
    for category in categories:
        category_path = os.path.join(base_folder, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

def categorize_image(image_path, categories_hashes):
    image = Image.open(image_path)
    image_hash = imagehash.average_hash(image)

    for category, category_hash in categories_hashes.items():
        if image_hash - category_hash < 10:  # Threshold for similarity
            return category
    return "Uncategorized"

def move_image(file_path, category_folder):
    base_name = os.path.basename(file_path)
    destination_path = os.path.join(category_folder, base_name)

    # Handle conflict by renaming the file if it already exists
    if os.path.exists(destination_path):
        name, ext = os.path.splitext(base_name)
        counter = 1
        while os.path.exists(destination_path):
            new_name = f"{name}_{counter}{ext}"
            destination_path = os.path.join(category_folder, new_name)
            counter += 1

    shutil.move(file_path, destination_path)
    print(f"Moved {file_path} to {destination_path}")

def filter_images(base_folder, categories, categories_hashes):
    create_category_folders(base_folder, categories)

    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith(('jpg', 'jpeg', 'png', 'gif')):
                file_path = os.path.join(root, file)
                category = categorize_image(file_path, categories_hashes)
                category_folder = os.path.join(base_folder, category)
                move_image(file_path, category_folder)

if __name__ == "__main__":
    base_folder = 'images'  # Path to the base images folder
    categories = ['Category1', 'Category2', 'Category3', 'Uncategorized']
    
    # Define hashes for sample images representing each category
    categories_hashes = {
        'Category1': imagehash.hex_to_hash('0000000000000000'),  # Example hash
        'Category2': imagehash.hex_to_hash('ffffffffffffffff'),  # Example hash
        'Category3': imagehash.hex_to_hash('1111111111111111'),  # Example hash
    }

    filter_images(base_folder, categories, categories_hashes)
