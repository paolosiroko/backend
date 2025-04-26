from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import query
import uvicorn

app = FastAPI(title="Travel Assistant API", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://travel-assistant-frontend.onrender.com","http://localhost:3000"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)

@app.get("/")
async def root():
    return {"message": "Travel Assistant API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)