from fastapi import FastAPI, UploadFile, File
import shutil
import os

# CAD loaders
from cad.step_loader import load_step
from cad.stl_loader import load_stl
from cad.iges_loader import load_iges
from cad.dxf_loader import load_dxf

# AFR
from afr.feature_patterns import detect_features

# DFM
from dfm.thin_wall import check_thin_wall
from dfm.tool_access import check_tool_access
from dfm.deep_pocket import check_deep_pocket

# Planner
from planner.cam_planner import plan_operations
from planner.cycle_time import estimate_cycle_time

# Costing
from costing.ai_pricing import predict_price

# Utils
from utils.report import generate_report


app = FastAPI(title="CNC Intelligence Engine V16")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "CNC Intelligence Engine Running"}


@app.post("/analyze-part")
async def analyze_part(file: UploadFile = File(...)):

    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Detect file type
        ext = file.filename.lower().split(".")[-1]

        shape = None
        raw_data = None

        # Load CAD based on type
        if ext in ["step", "stp"]:
            shape = load_step(file_path)

        elif ext in ["iges", "igs"]:
            shape = load_iges(file_path)

        elif ext == "stl":
            shape = load_stl(file_path)

        elif ext == "dxf":
            raw_data = load_dxf(file_path)

        else:
            return {"error": "Unsupported file type"}

        # Feature detection
        if shape:
            features = detect_features(shape)
        else:
            features = {"info": "2D or unsupported for AFR"}

        # CAM planning
        operations = plan_operations(features if isinstance(features, dict) else {})

        # Cycle time
        cycle_time = estimate_cycle_time(operations)

        # DFM checks (example values for now)
        dfm_results = {
            "thin_wall": check_thin_wall(1.2),
            "tool_access": check_tool_access(40, 10),
            "deep_pocket": check_deep_pocket(20, 10)
        }

        # AI pricing
        feature_count = sum(features.values()) if isinstance(features, dict) else 1
        price = predict_price(feature_count, len(operations))

        # Report
        report = generate_report(features, operations, price)

        return {
            "features": features,
            "operations": operations,
            "dfm": dfm_results,
            "cycle_time_min": cycle_time,
            "price": price,
            "report": report
        }

    except Exception as e:
        return {
            "error": str(e)
        }