from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import ask_route
from routes import documents_route

app = FastAPI(title="Nursing AI Learning Assistant API")

# Add CORS middleware so a React frontend can connect later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router in the FastAPI app
# Use prefix "/api"
app.include_router(ask_route.router, prefix="/api")
app.include_router(documents_route.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "backend running"}

if __name__ == "__main__":
    import uvicorn
    # The API must run on port 5000
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
