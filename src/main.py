from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# CAD loaders
from src.cad.step_loader import load_step
from src.cad.stl_loader import load_stl
from src.cad.dxf_loader import load_dxf

# Feature detection
from src.afr.feature_patterns import detect_features

# DFM
from src.dfm.thin_wall import check_thin_wall
from src.dfm.tool_access import check_tool_access
from src.dfm.deep_pocket import check_deep_pocket

# Planner
from src.planner.cam_planner import plan_operations
from src.planner.cycle_time import estimate_cycle_time

# Costing
from src.costing.ai_pricing import predict_price

# Report
from src.utils.report import generate_report


app = FastAPI(title="CNC Intelligence Engine")

# ✅ CORS FIX (CRITICAL for Lovable)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "CNC Intelligence Engine Running"}


@app.post("/analyze-part")
async def analyze_part(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        ext = file.filename.lower().split(".")[-1]

        shape = None

        # ✅ SAFE CAD LOADING
        if ext in ["step", "stp", "iges", "igs"]:
            shape = load_step(file_path)

        elif ext == "stl":
            shape = load_stl(file_path)

        elif ext == "dxf":
            shape = load_dxf(file_path)

        else:
            return {"error": "Unsupported file type"}

        # Feature detection
        features = detect_features(shape) if shape else {}

        # CAM planning
        operations = plan_operations(features)

        # Cycle time
        cycle_time = estimate_cycle_time(operations)

        # DFM checks
        dfm = {
            "thin_wall": check_thin_wall(1.2),
            "tool_access": check_tool_access(40, 10),
            "deep_pocket": check_deep_pocket(20, 10)
        }

        # ✅ SAFE FEATURE COUNT (prevents crash)
        feature_count = sum(features.values()) if isinstance(features, dict) else 1

        # Pricing
        price = predict_price(features, operations, cycle_time)

        # Report
        report = generate_report(features, operations, price)

        return {
            "features": features,
            "operations": operations,
            "dfm": dfm,
            "cycle_time": cycle_time,
            "price": price,
            "report": report
        }

    except Exception as e:
        return {"error": str(e)}