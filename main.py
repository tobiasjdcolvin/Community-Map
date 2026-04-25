from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

DATABASE = "./data/myapp.db"

app = FastAPI()

app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/")
def root():
    return FileResponse("public/index.html")
