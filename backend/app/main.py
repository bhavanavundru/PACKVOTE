from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, vote, recommend, plan

app = FastAPI(
    title="PACKVOTE API 🚀",
    description="AI-powered group travel planner backend",
    version="1.0.0"
)

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later: restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(chat.router)
app.include_router(vote.router)
app.include_router(recommend.router)
app.include_router(plan.router)

@app.get("/")
def root():
    return {"message": "PACKVOTE API is running successfully 🚀"}
