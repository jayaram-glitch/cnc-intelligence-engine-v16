from fastapi import FastAPI, UploadFile
import shutil, os

from cad.step_loader import load_step
from afr.feature_patterns import detect_features
from dfm.thin_wall import check_thin_wall
from dfm.tool_access import check_tool_access
from planner.cam_planner import plan_operations
from costing.ai_pricing import predict_price
from utils.report import generate_report

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze-part")
async def analyze(file: UploadFile):

    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    shape = load_step(path)

    features = detect_features(shape)

    operations = plan_operations(features)

    dfm = {
        "thin_wall": check_thin_wall(1.2),
        "tool_access": check_tool_access(40, 10)
    }

    price = predict_price(len(features), len(operations))

    report = generate_report(features, operations, price)

    return {
        "features": features,
        "operations": operations,
        "dfm": dfm,
        "price": price,
        "report": report
    }