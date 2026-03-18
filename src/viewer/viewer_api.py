from fastapi import APIRouter
from viewer.step_to_stl import convert_step_to_stl

router = APIRouter()

@router.post("/generate-stl")
def generate_stl(file_path):

    stl_path = file_path.replace(".step", ".stl")

    convert_step_to_stl(file_path, stl_path)

    return {"stl": stl_path}