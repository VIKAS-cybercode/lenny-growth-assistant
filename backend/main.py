from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Lenny Growth Assistant API is running"}