from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from model import recommend, search_products
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistem Rekomendasi Produk", version="1.0.0")
templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(f"{request.method} {request.url.path} - {duration:.3f}s - {response.status_code}")
    return response


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/recommend/{keyword}")
def get_recommendation(keyword: str):
    result = recommend(keyword)
    return {"input": keyword, "recommendations": result}


@app.get("/search/{keyword}")
def search(keyword: str):
    return search_products(keyword)


@app.get("/products")
def get_all_products():
    from model import df
    return df["product"].tolist()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
