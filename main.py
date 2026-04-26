from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import database as db

DATABASE = "./data/myapp.db"

app = FastAPI()

class SymptomsIn(BaseModel):
    cough_congestion: bool
    nausea_vomiting: bool
    difficulty_breathing :bool
    sore_throat :bool
    rash :bool
    fever :bool
    chills :bool
    diarrhea :bool
    attending_a_recent_mass_gathering :bool
    history_of_travel: bool
    

app.mount("/static", StaticFiles(directory="public"), name="static")

@app.post("/api/symptoms")
def set_symptoms(symptoms: SymptomsIn):
    valid_parameters = []

    for name, val in symptoms.model_dump().items():
        if (val == True):
            print(f"{name}: {val}")
            valid_parameters.append(name)

    return {"received": symptoms.model_dump()}

@app.get("/")
def root():
    return FileResponse("public/index.html")

@app.get("/api/locations")
def get_locations():
    rows = db.get_all_coordinates_and_response_counts()
    return [{"lat": lat, "lon": lon, "count": count} for lat, lon, count in rows]
