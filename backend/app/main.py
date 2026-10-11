from fastapi import FastAPI

app = FastAPI(title="ORGmind-agent")

@app.get("/")
def root():
    return {"message": "Hello ORGmind-agent!!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}