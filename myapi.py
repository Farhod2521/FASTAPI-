from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import datetime
from datetime import datetime as dt

# MySQL bazaga ulanish
DATABASE_URL = "mysql+pymysql://{user}:{password}@{host}:{port}/{name}".format(
    user='tmsitiuz',
    password='pwd4catalogDB',
    host='localhost',
    port='3306',
    name='tmsitiuz_catalog'
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI ilovasini yaratish
app = FastAPI()

# MaterialAds modeli
class MaterialAds(Base):
    __tablename__ = 'material_ads'

    id = Column(Integer, primary_key=True, index=True)
    material_name_id = Column(String(20))
    material_description = Column(String(500), nullable=True)
    material_price = Column(Float)
    material_price_currency = Column(String(15), default="UZS")
    material_measure = Column(String(25))
    material_image = Column(String(100), nullable=True)
    material_amount = Column(Float)
    material_amount_measure = Column(String(25))
    material_status = Column(Boolean, default=True)
    material_created_date = Column(DateTime, default=dt.utcnow)
    material_updated_date = Column(DateTime, default=dt.utcnow)
    material_deactivated_date = Column(DateTime, nullable=True)
    sertificate_blank_num = Column(String(25))
    sertificate_reestr_num = Column(String(25))
    material_owner_id = Column(Integer, ForeignKey('users.id'))
    company_name = Column(String(255), nullable=True)
    company_stir = Column(String(10), nullable=True)
    material_region_id = Column(Integer, ForeignKey('uzb_regions.id'), nullable=True)
    material_district_id = Column(Integer, ForeignKey('districts.id'), nullable=True)

    region = relationship("Regions", backref="materials", lazy="joined")
    material_details = relationship("Materials", primaryjoin="Materials.material_csr_code == foreign(MaterialAds.material_name_id)", lazy="joined")

# Regions modeli
class Regions(Base):
    __tablename__ = 'uzb_regions'

    id = Column(Integer, primary_key=True, index=True)
    region_name = Column(String(1), nullable=True)
    region_name_uz = Column(String(30), nullable=False)
    region_name_en = Column(String(30), nullable=True)
    region_name_ru = Column(String(30), nullable=True)

# Materials modeli
class Materials(Base):
    __tablename__ = "material_resources"

    material_csr_code = Column(String(20), primary_key=True)
    material_name = Column(String(1500))
    material_desc = Column(String(255), nullable=True)
    material_measure = Column(String(25))
    material_group_id = Column(Integer, ForeignKey('mat_groups.id'))
    material_image = Column(String(255), nullable=True)
    material_views_count = Column(Integer, default=0)
    materil_gost = Column(String(255), nullable=True)


class MatVolumes(Base):
    __tablename__ = "material_volumes"

    id = Column(Integer, primary_key=True)
    volume_name = Column(String(255), unique=True)
    volume_logo = Column(String(255))
    volume_desc = Column(String(255), nullable=True)

# MatCategories modeli
class MatCategories(Base):
    __tablename__ = "material_categories"

    id = Column(Integer, primary_key=True)
    category_name = Column(String(255), unique=True)
    category_desc = Column(String(255), nullable=True)
    category_volume_id = Column(Integer, ForeignKey('material_volumes.id'))

    volume = relationship("MatVolumes", backref="categories")

# MatGroups modeli
class MatGroups(Base):
    __tablename__ = "material_groups"

    id = Column(Integer, primary_key=True)
    group_name = Column(String(255), unique=True)
    group_desc = Column(String(255), nullable=True)
    group_category_id = Column(Integer, ForeignKey('material_categories.id'))

    category = relationship("MatCategories", backref="groups")

# MatVolume filteri uchun Pydantic modeli
class MatVolumeSchema(BaseModel):
    id: int
    volume_name: str
    categories: List[str]

    class Config:
        from_attributes = True


# MatCategory filteri uchun Pydantic modeli
class MatCategorySchema(BaseModel):
    id: int
    category_name: str
    groups: List[str]

    class Config:
        from_attributes = True

# MatGroup filteri uchun Pydantic modeli
class MatGroupSchema(BaseModel):
    id: int
    group_name: str
    materials: List[str]

    class Config:
        from_attributes = True
# Pydantic modeli (FastAPI uchun)
class MaterialAdsSchema(BaseModel):
    id: int
    material_name_id: str
    material_name: Optional[str] = None
    material_description: Optional[str] = None
    material_price: float
    material_price_currency: str
    material_measure: str
    material_image: Optional[str] = None
    material_amount: float
    material_amount_measure: str
    material_status: bool
    material_created_date: datetime.datetime
    material_updated_date: datetime.datetime
    material_deactivated_date: Optional[datetime.datetime] = None
    sertificate_blank_num: str
    sertificate_reestr_num: str
    material_owner_id: int
    company_name: Optional[str] = None
    company_stir: Optional[str] = None
    material_region_name: Optional[str] = None
    material_district_id: Optional[int] = None

    class Config:
        from_attributes = True

# Ma'lumotlar bazasidan sessiya yaratish
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MaterialAds obyektlarini filterlash uchun API
@app.get("/materials/filter", response_model=dict)
async def filter_materials(
    region_name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MaterialAds)

    if region_name:
        query = query.join(Regions).filter(Regions.region_name_uz == region_name)
    
    if min_price is not None:
        query = query.filter(MaterialAds.material_price >= min_price)
    
    if max_price is not None:
        query = query.filter(MaterialAds.material_price <= max_price)

    materials = query.all()

    if not materials:
        raise HTTPException(status_code=404, detail="No materials found for the given filters")

    return {
        "count": len(materials),
        "materials": [
            MaterialAdsSchema(
                **material.__dict__,
                material_name=material.material_details.material_name if material.material_details else None,
                material_region_name=material.region.region_name_uz if material.region else None
            ) for material in materials
        ]
    }


# MaterialAds obyektlarini olish (pagination qo'shildi)
@app.get("/materials/", response_model=List[MaterialAdsSchema])
async def get_materials(page: int = 1, limit: int = 24, db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    materials = db.query(MaterialAds).offset(skip).limit(limit).all()

    material_list = []
    for material in materials:
        # `Materials` jadvalidan `material_name` ni olish
        material_details = db.query(Materials).filter(Materials.material_csr_code == material.material_name_id).first()
        material_name = material_details.material_name if material_details else None

        material_list.append(MaterialAdsSchema(
            **material.__dict__,
            material_name=material_name,
            material_region_name=material.region.region_name_uz if material.region else None
        ))
    
    return material_list

# MaterialVolume bo'yicha filterlash
@app.get("/materials/volume/{volume_id}", response_model=MatVolumeSchema)
async def get_volume_details(volume_id: int, db: Session = Depends(get_db)):
    volume = db.query(MatVolumes).filter(MatVolumes.id == volume_id).first()
    if not volume:
        raise HTTPException(status_code=404, detail="Volume not found")

    categories = [category.category_name for category in volume.categories]
    
    return MatVolumeSchema(
        id=volume.id,
        volume_name=volume.volume_name,
        categories=categories
    )

# MatCategory bo'yicha filterlash
@app.get("/materials/categories/{category_id}", response_model=MatCategorySchema)
async def get_category_details(category_id: int, db: Session = Depends(get_db)):
    category = db.query(MatCategories).filter(MatCategories.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    groups = [group.group_name for group in category.groups]
    
    return MatCategorySchema(
        id=category.id,
        category_name=category.category_name,
        groups=groups
    )

# MatGroup bo'yicha filterlash
@app.get("/materials/groups/{group_id}", response_model=MatGroupSchema)
async def get_group_details(group_id: int, db: Session = Depends(get_db)):
    group = db.query(MatGroups).filter(MatGroups.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    materials = [material.material_name for material in group.category.groups]
    
    return MatGroupSchema(
        id=group.id,
        group_name=group.group_name,
        materials=materials
    )

# Konsolga chiqarishni o'chirish
import logging
logging.getLogger('uvicorn.access').disabled = True
