from fastapi import FastAPI

from app.api import router
app = FastAPI(title="ORGmind-agent")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Hello ORGmind-agent!!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}