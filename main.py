from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import List

from sqlalchemy.ext.asyncio import async_session
from starlette.responses import HTMLResponse, JSONResponse

import database
from database import Session
from pereval.models import PerevalAdded, User, Coords, Level, Image, PerevalAddedPydantic, ErrorResponse, DetailItem
from pereval.serializer import image_pydantic_to_sqlalchemy, perevaladded_pydantic_to_sqlalchemy, \
    level_pydantic_to_sqlalchemy, user_pydantic_to_sqlalchemy, coords_pydantic_to_sqlalchemy

app = FastAPI()




@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/Pereval", response_model=None)
def create_pereval(pereval_data: PerevalAddedPydantic):
    db = Session()
    try:
        user = user_pydantic_to_sqlalchemy(pereval_data.user)
        coords = coords_pydantic_to_sqlalchemy(pereval_data.coords)
        level = level_pydantic_to_sqlalchemy(pereval_data.level)

        db.add(user)
        db.add(coords)
        db.add(level)

        images = [image_pydantic_to_sqlalchemy(image_data) for image_data in pereval_data.images]

        for image in images:
            db.add(image)

        pereval = perevaladded_pydantic_to_sqlalchemy(pereval_data)

        db.add(pereval)
        db.commit()

        return pereval
    except Exception as e:
        db.rollback()
        error_height = 42

        if not isinstance(error_height, int):
            raise ValueError("Error: the 'height' value must be an integer")

        error_detail = ErrorResponse(
            detail=[
                DetailItem(loc="string", msg="Error while saving data", type="server_error", height=error_height)
            ]
        )
        return JSONResponse(status_code=500, content=error_detail.dict())
    finally:
        db.close()

@app.get("/pereval_id/{pereval_id}", response_model=None)
async def get_pereval_by_id(pereval_id: int):
    async with async_session() as session:
        pereval = await session.get(database.pereval, pereval_id)
        if pereval is None:
            error_detail = ErrorResponse(
                detail=[
                    DetailItem(loc=["string", 0], msg="Объект не найден", type="not_found")
                ]
            )
            return JSONResponse(status_code=404, content=error_detail.dict())
        return pereval

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI_Project",
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
    import webbrowser

    # Открываем браузер с URL для документации при запуске
    webbrowser.open('http://127.0.0.1:8000/docs')

    uvicorn.run(app, host="127.0.0.1", port=8000)
