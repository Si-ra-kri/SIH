import rasterio
import numpy as np
import os

DATA_FOLDER = 'data'
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# --- Image Parameters ---
width = 256
height = 256
# We need 8 bands for the geo_analysis script to work
count = 8 
# Define a generic Coordinate Reference System (CRS) and transform
crs = 'EPSG:32644' # A common CRS for India
transform = rasterio.transform.from_origin(79.0, 23.0, 0.01, 0.01)

profile = {
    'driver': 'GTiff',
    'height': height,
    'width': width,
    'count': count,
    'dtype': np.uint16,
    'crs': crs,
    'transform': transform,
}

print("Generating dummy satellite images...")

try:
    # --- Create image_old.tif ---
    # This represents a healthy forest. NIR band (8) is high, Red band (4) is low.
    with rasterio.open(os.path.join(DATA_FOLDER, 'image_old.tif'), 'w', **profile) as dst:
        for i in range(1, count + 1):
            band_data = np.random.randint(500, 1000, (height, width), dtype=np.uint16)
            if i == 4: # Red band
                band_data = np.random.randint(200, 400, (height, width), dtype=np.uint16)
            if i == 8: # NIR band
                band_data = np.random.randint(3500, 4500, (height, width), dtype=np.uint16)
            dst.write(band_data, i)

    print("✅ Successfully created 'image_old.tif'")

    # --- Create image_new.tif ---
    # This represents the same forest, but with a patch of deforestation.
    with rasterio.open(os.path.join(DATA_FOLDER, 'image_new.tif'), 'w', **profile) as dst:
        for i in range(1, count + 1):
            band_data = np.random.randint(500, 1000, (height, width), dtype=np.uint16)
            if i == 4: # Red band
                band_data = np.random.randint(200, 400, (height, width), dtype=np.uint16)
            if i == 8: # NIR band
                band_data = np.random.randint(3500, 4500, (height, width), dtype=np.uint16)

            # Create a square patch of "deforestation" (low NIR, high Red)
            band_data[100:200, 100:200] = np.random.randint(1500, 2000, (100, 100), dtype=np.uint16) if i == 4 else band_data[100:200, 100:200]
            band_data[100:200, 100:200] = np.random.randint(800, 1200, (100, 100), dtype=np.uint16) if i == 8 else band_data[100:200, 100:200]

            dst.write(band_data, i)

    print("✅ Successfully created 'image_new.tif'")
    print("\nImage generation complete. You can now run the main analysis.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you have run 'pip install rasterio numpy' in your active venv.")