from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"Status": "todo api is running"}