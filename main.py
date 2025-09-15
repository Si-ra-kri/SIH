import re
import pytesseract
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# This is the crucial line that creates the web application
app = FastAPI()

# Allow the frontend (running on localhost:3000) to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process_claim/")
async def process_claim(file: UploadFile = File(...)):
    try:
        # Read the uploaded image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Use Tesseract to get text from the image
        extracted_text = pytesseract.image_to_string(image)

        # Use rules to find the details
        name = re.search(r"Claimant Name: (.*)", extracted_text)
        village = re.search(r"Village: (.*)", extracted_text)
        area = re.search(r"Claimed Area: (.*)", extracted_text)

        # Prepare the JSON data to send back
        details = {
            "name": name.group(1).strip() if name else "Not Found",
            "village": village.group(1).strip() if village else "Not Found",
            "area": area.group(1).strip() if area else "Not Found",
        }

        # Add placeholder analysis data for the dashboard
        details["analysis"] = {
            "forest_cover_percent": 78.5,
            "flagged_as_anomaly": True,
            "change_map_url": "/change_detection_overlay.png",
        }

        return details
    except Exception as e:
        return {"error": str(e)}