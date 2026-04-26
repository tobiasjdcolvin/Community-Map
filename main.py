from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import database as db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.build_countries()
    yield

app = FastAPI(lifespan=lifespan)

VALID_SYMPTOMS = {
    "cough_congestion", "nausea_vomiting", "difficulty_breathing",
    "sore_throat", "rash", "fever", "chills", "diarrhea",
    "attending_a_recent_mass_gathering", "history_of_travel"
}

class SymptomsIn(BaseModel):
    cough_congestion: bool
    nausea_vomiting: bool
    difficulty_breathing: bool
    sore_throat: bool
    rash: bool
    fever: bool
    chills: bool
    diarrhea: bool
    attending_a_recent_mass_gathering: bool
    history_of_travel: bool

app.mount("/static", StaticFiles(directory="public"), name="static")

@app.post("/api/symptoms")
def set_symptoms(symptoms: SymptomsIn, city: str, state: str = "", country: str = ""):
    valid_parameters = []
    for name, val in symptoms.model_dump().items():
        if val == True:
            print(f"{name}: {val}")
            valid_parameters.append(name)
    
    success = db.add_response(city=city, state=state, country=country, values=valid_parameters)
    
    if not success:
        raise HTTPException(status_code=400, detail="Could not save response")
    
    return {"received": symptoms.model_dump()}

@app.get("/")
def root():
    return FileResponse("public/index.html")

@app.get("/api/locations")
def get_locations(symptom: str = None):
    if symptom and symptom not in VALID_SYMPTOMS:
        raise HTTPException(status_code=400, detail="Invalid symptom")
    
    symptoms_filter = [symptom] if symptom else []
    rows = db.get_all_coordinates_and_response_counts_filtered_by_symptoms(symptoms_filter)
    return [{"lat": r[0], "lon": r[1], "count": r[2]} for r in rows]

@app.get("/test")
def loading_page():
    return FileResponse("public/test.html")