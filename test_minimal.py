"""Minimal test to check if routes work"""
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/")
async def root():
    return {"message": "Root works!"}

@app.get("/test")
async def test_page(request: Request):
    return templates.TemplateResponse("api_test.html", {"request": request})

@app.get("/demo")
async def demo_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/setup")
async def setup_page(request: Request):
    return templates.TemplateResponse("setup.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
