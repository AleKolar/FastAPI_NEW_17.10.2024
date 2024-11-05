from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import List

from sqlalchemy.ext.asyncio import async_session
from starlette.responses import HTMLResponse

import database
from database import Session
from pereval.models import PerevalAdded, User, Coords, Level, Image

app = FastAPI()




# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

@app.post("/Pereval", response_model=PerevalAdded)  # Указываем response_model для возврата созданного объекта
def create_pereval(pereval_data: PerevalAdded):
    db = Session()
    try:
        # Создаем новые объекты на основе полученных данных
        user = User(**pereval_data.user.dict())
        coords = Coords(**pereval_data.coords.dict())
        level = Level(**pereval_data.level.dict())

        db.add(user)
        db.add(coords)
        db.add(level)

        for image_data in pereval_data.images:
            image = Image(**image_data.dict())
            db.add(image)

        pereval = PerevalAdded(
            beauty_title=pereval_data.beauty_title,
            title=pereval_data.title,
            other_titles=pereval_data.other_titles,
            connect=pereval_data.connect,
            add_time=pereval_data.add_time,
            user=user,
            coords=coords,
            level=level,
            images=pereval_data.images
        )
        db.add(pereval)
        db.commit()

        return pereval  # Возвращаем созданный объект
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при сохранении данных")
    finally:
        db.close()

@app.get("/pereval_id/{pereval_id}", response_model=PerevalAdded)
async def get_pereval_by_id(pereval_id: int):
    async with async_session() as session:
        pereval = await session.get(database.pereval, pereval_id)
        if pereval is None:
            raise HTTPException(status_code=404, detail="Объект не найден")
        return pereval

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your Project Name",
        version="1.0.0",
        description="This is a fantastic project",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/docs", include_in_schema=False, response_class=HTMLResponse)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/redoc", include_in_schema=False, response_class=HTMLResponse)
async def redoc_html():
    return get_redoc_html(openapi_url="/openapi.json", title="redoc")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
