from fastapi import FastAPI
from database import Base, engine
from endpoints.materials import materials_router

# Ma'lumotlar bazasini yaratish
Base.metadata.create_all(bind=engine)

# FastAPI ilovasini yaratish
app = FastAPI(
    title="KLASSIFIKATOR",
    description="This is a project for managing materials with FastAPI.",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "url": "http://yourwebsite.com",
        "email": "yourname@domain.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)
# Routerlarni qo'shish
app.include_router(materials_router)
