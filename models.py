from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime as dt
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