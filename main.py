from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message": "We are ready to build green tool"}