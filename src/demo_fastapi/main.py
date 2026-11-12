from fastapi import FastAPI

app = FastAPI(title="TaskHub")


@app.get("/health")
def health():
    return {"status": "ok"}
