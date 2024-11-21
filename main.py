from fastapi import FastAPI
from database import Base, engine
from endpoints.materials import materials_router
from endpoints.techno import techno_router
from fastapi.middleware.cors import CORSMiddleware
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


origins = [
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "https://backend-market.tmsiti.uz",  # Sizning veb-saytingiz yoki kerakli domenlar
    "http://localhost:3000",
    "https://new-catalog.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(materials_router)
app.include_router(techno_router)
