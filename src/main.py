from fastapi import FastAPI
from pydantic import BaseModel
import cadquery as cq
import random

app = FastAPI()

class PartInput(BaseModel):
    length: float
    width: float
    height: float
    holes: int = 0

@app.get("/")
def root():
    return {"status": "CNC backend running"}

@app.post("/analyze")
def analyze_part(data: PartInput):
    # Create part
    part = cq.Workplane("XY").box(data.length, data.width, data.height)

    # Add holes (simple simulation)
    for i in range(data.holes):
        part = part.faces(">Z").workplane().hole(5)

    # Feature extraction (basic)
    volume = data.length * data.width * data.height
    complexity = data.holes + 1

    # AI pricing logic (basic version)
    base_price = volume * 0.05
    complexity_cost = complexity * 10
    total_price = round(base_price + complexity_cost, 2)

    return {
        "volume": volume,
        "complexity": complexity,
        "estimated_price": total_price
    }