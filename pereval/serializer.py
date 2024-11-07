from pereval.models import User, Coords, Level, Image, PerevalAdded
from pereval.models import UserPydantic, CoordsPydantic, LevelPydantic, ImagePydantic, PerevalAddedPydantic

def user_pydantic_to_sqlalchemy(user_pydantic: UserPydantic) -> User:
    user_data = user_pydantic.dict()
    if not all(user_data.values()):
        raise ValueError("Missing required fields in UserPydantic")
    return User(email=user_data['email'], fam=user_data['fam'], name=user_data['name'], otc=user_data['otc'], phone=user_data['phone'])

def coords_pydantic_to_sqlalchemy(coords_pydantic: CoordsPydantic) -> Coords:
    coords_data = coords_pydantic.dict()
    if not all(coords_data.values()):
        raise ValueError("Missing required fields in CoordsPydantic")
    return Coords(latitude=coords_data['latitude'], longitude=coords_data['longitude'], height=coords_data['height'])

def level_pydantic_to_sqlalchemy(level_pydantic: LevelPydantic) -> Level:
    level_data = level_pydantic.dict()
    if not all(level_data.values()):
        raise ValueError("Missing required fields in LevelPydantic")
    return Level(winter=level_data['winter'], summer=level_data['summer'], autumn=level_data['autumn'], spring=level_data['spring'])

def image_pydantic_to_sqlalchemy(image_pydantic: ImagePydantic) -> Image:
    image_data = image_pydantic.dict()
    if not all(image_data.values()):
        raise ValueError("Missing required fields in ImagePydantic")
    return Image(data=image_data['data'], title=image_data['title'])

def perevaladded_pydantic_to_sqlalchemy(perevaladded_pydantic: PerevalAddedPydantic) -> PerevalAdded:
    user = user_pydantic_to_sqlalchemy(perevaladded_pydantic.user)
    coords = coords_pydantic_to_sqlalchemy(perevaladded_pydantic.coords)
    level = level_pydantic_to_sqlalchemy(perevaladded_pydantic.level)
    images = [image_pydantic_to_sqlalchemy(image_data) for image_data in perevaladded_pydantic.images]

    # Создание объекта PerevalAdded
    pereval = PerevalAdded(
        beauty_title=perevaladded_pydantic.beauty_title,
        title=perevaladded_pydantic.title,
        other_titles=perevaladded_pydantic.other_titles,
        connect=perevaladded_pydantic.connect,
        user=user,
        coords=coords,
        level=level
    )

    # Привязка каждого изображения к объекту PerevalAdded
    for image in images:
        # Проверка, что изображение не уже связано с объектом PerevalAdded
        if image.pereval is None:
            image.pereval = pereval

    return pereval


