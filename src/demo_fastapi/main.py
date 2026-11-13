from fastapi import FastAPI

from demo_fastapi.routers import projects, tags, tasks, users

app = FastAPI(title="TaskHub")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(users.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(tags.router, prefix="/tag")
