import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os
import traceback # We are adding this for detailed error reports

def analyze_and_save():
    DATA_FOLDER = 'data'
    print("Starting Geo-AI Analysis (with advanced debugging)...")

    try:
        # Construct the full, absolute path to the files
        base_path = os.path.abspath(os.path.dirname(__file__))
        image_new_path = os.path.join(base_path, DATA_FOLDER, 'image_new.tif')
        image_old_path = os.path.join(base_path, DATA_FOLDER, 'image_old.tif')

        print(f"Attempting to open new image at: {image_new_path}")
        with rasterio.open(image_new_path) as src:
            nir_new = src.read(8).astype(float)
            red_new = src.read(4).astype(float)

        print(f"Attempting to open old image at: {image_old_path}")
        with rasterio.open(image_old_path) as src:
            nir_old = src.read(8).astype(float)
            red_old = src.read(4).astype(float)

        # --- The rest of the analysis code is the same ---
        np.seterr(divide='ignore', invalid='ignore')
        ndvi_new = (nir_new - red_new) / (nir_new + red_new)
        ndvi_old = (nir_old - red_old) / (nir_old + red_old)
        delta_ndvi = ndvi_new - ndvi_old
        deforestation_map = np.where(delta_ndvi < -0.2, 1, 0)

        h, w = deforestation_map.shape
        rgba_change = np.zeros((h, w, 4), dtype=np.uint8)
        rgba_change[deforestation_map == 1] = [255, 0, 0, 200]

        output_path = os.path.join(base_path, 'frontend', 'public', 'change_detection_overlay.png')
        plt.imsave(output_path, rgba_change)

        print(f"✅ Analysis complete! Overlay map saved to '{output_path}'")

    # IMPORTANT PART
    except Exception as e:
        print("\n--- CAUGHT THE REAL ERROR ---")
        print(f"The error is NOT a missing file. The actual error is: {type(e).__name__}")
        print(f"Error details: {e}")
        print("\n--- FULL ERROR TRACEBACK ---")
        traceback.print_exc()
        print("----------------------------")


if __name__ == '__main__':
    analyze_and_save()