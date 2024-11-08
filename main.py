import logging
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from sqlalchemy import select

from sqlalchemy.ext.asyncio import async_session, AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload, joinedload
from starlette.responses import HTMLResponse, JSONResponse


import database
from database import Session
from pereval.models import PerevalAdded, User, Coords, Level, Image, PerevalAddedPydantic, ErrorResponse, DetailItem, \
    UserPydantic, CoordsPydantic, LevelPydantic, ImagePydantic
from pereval.serializer import image_pydantic_to_sqlalchemy, perevaladded_pydantic_to_sqlalchemy, \
    level_pydantic_to_sqlalchemy, user_pydantic_to_sqlalchemy, coords_pydantic_to_sqlalchemy

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/Pereval", response_model=None)
async def create_pereval(pereval_data: PerevalAddedPydantic):
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
        await db.commit()

        return pereval
    except Exception as e:
        handle_db_error(db)
        return JSONResponse(status_code=500, content=ErrorResponse.dict())
    finally:
        await db.close()

def handle_db_error(db):
    db.rollback()
    error_height = 42

    if not isinstance(error_height, int):
        raise ValueError("Error: the 'height' value must be an integer")

    error_detail = ErrorResponse(
        detail=[
            DetailItem(loc="string", msg="Error while saving data", type="server_error", height=error_height)
        ]
    )


class PerevalResponse(BaseModel):
    id: int
    beauty_title: str
    title: str
    other_titles: str
    connect: str
    user: UserPydantic
    coords: CoordsPydantic
    level: LevelPydantic
    images: List[ImagePydantic]

Session: sessionmaker = sessionmaker(bind=database.engine, class_=AsyncSession)

logger = logging.getLogger(__name__)

@app.get("/pereval_id/{pereval_id}", response_model=PerevalResponse)
async def get_pereval_by_id(pereval_id: int) -> PerevalResponse:
    async with Session() as db:
        pereval = await db.execute(
            select(PerevalAdded)
            .options(
                selectinload(PerevalAdded.user),
                selectinload(PerevalAdded.coords),
                selectinload(PerevalAdded.level),
                selectinload(PerevalAdded.images)
            )
            .filter(PerevalAdded.id == pereval_id)
        )
        result = pereval.scalars().first()

        if not result:
            raise HTTPException(status_code=404, detail="Pereval with this ID not found")

        logger.debug(f"Retrieved PerevalAdded object with ID: {result.id}")

        images_data = []
        if result.images:
            images_data = [ImagePydantic(data=image_data['data'], title=image_data['title']) for image_data in result.images]

        logger.debug(f"Constructed images data: {images_data}")

        return PerevalResponse(
            id=result.id,
            beauty_title=result.beauty_title,
            title=result.title,
            other_titles=result.other_titles,
            connect=result.connect,
            user=UserPydantic(email=result.user.email, fam=result.user.fam, name=result.user.name, otc=result.user.otc, phone=result.user.phone),
            coords=CoordsPydantic(latitude=result.coords.latitude, longitude=result.coords.longitude, height=result.coords.height),
            level=LevelPydantic(winter=result.level.winter, summer=result.level.summer, autumn=result.level.autumn, spring=result.level.spring),
            images=images_data
        )





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
