import requests
import os

# --- Configuration ---
# We are using new, reliable links for the sample images.
DATA_FOLDER = 'data'
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# New dictionary of files to download {url: filename}
files_to_download = {
    "https://s3.amazonaws.com/rasterio-sample-data/rgb_pan.tif": "image_old.tif",
    "https://s3.amazonaws.com/rasterio-sample-data/example.tif": "image_new.tif"
}

# --- Download Logic ---
print("Starting image download with new links...")

for url, filename in files_to_download.items():
    file_path = os.path.join(DATA_FOLDER, filename)
    
    if os.path.exists(file_path):
        print(f"'{filename}' already exists. Skipping.")
        continue

    try:
        print(f"Downloading '{filename}'...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Successfully saved '{filename}' to '{DATA_FOLDER}' folder.")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {filename}: {e}")

print("\nDownload process finished.")