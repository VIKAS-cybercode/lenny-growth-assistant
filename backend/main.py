from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.users import router as users_router
from routes.conversations import router as conversations_router
from routes.agent import router as agent_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(conversations_router)
app.include_router(agent_router)
@app.get("/")
def root():
    return {"message": "Lenny Growth Assistant API is running"}