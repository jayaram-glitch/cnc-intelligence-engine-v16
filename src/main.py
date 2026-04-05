from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import cadquery as cq
import os

app = FastAPI()

# -------------------------------
# 📦 INPUT MODEL (PARAMETRIC PART)
# -------------------------------
class PartInput(BaseModel):
    length: float
    width: float
    height: float
    holes: int = 0


# -------------------------------
# 🟢 ROOT ENDPOINT
# -------------------------------
@app.get("/")
def root():
    return {"status": "CNC backend running"}


# -------------------------------
# ⚙️ PARAMETRIC ANALYSIS API
# -------------------------------
@app.post("/analyze")
def analyze_part(data: PartInput):
    try:
        # Create 3D box
        part = cq.Workplane("XY").box(data.length, data.width, data.height)

        # Add holes
        for _ in range(data.holes):
            part = part.faces(">Z").workplane().hole(5)

        # Basic feature extraction
        volume = data.length * data.width * data.height
        complexity = data.holes + 1

        # Pricing logic (basic model)
        material_cost = volume * 0.05
        machining_cost = complexity * 10
        total_price = round(material_cost + machining_cost, 2)

        return {
            "type": "parametric",
            "volume": volume,
            "complexity": complexity,
            "estimated_price": total_price
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------------
# 📁 STEP FILE UPLOAD + ANALYSIS
# -------------------------------
@app.post("/upload-step")
async def upload_step(file: UploadFile = File(...)):
    try:
        # Save file temporarily
        file_path = f"/tmp/{file.filename}"
        contents = await file.read()

        with open(file_path, "wb") as f:
            f.write(contents)

        # Import STEP file using CadQuery
        model = cq.importers.importStep(file_path)

        # Bounding box
        bbox = model.val().BoundingBox()

        length = bbox.xlen
        width = bbox.ylen
        height = bbox.zlen

        volume = length * width * height

        # Simple complexity estimation
        complexity = 1  # can improve later

        # Pricing model
        material_cost = volume * 0.05
        machining_cost = complexity * 20
        total_price = round(material_cost + machining_cost, 2)

        return {
            "type": "step_file",
            "filename": file.filename,
            "dimensions": {
                "length": round(length, 2),
                "width": round(width, 2),
                "height": round(height, 2)
            },
            "volume": round(volume, 2),
            "complexity": complexity,
            "estimated_price": total_price
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)