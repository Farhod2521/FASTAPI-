from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime,BigInteger
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime as dt




###################################################           ###################################################
###################################################   TECHNO  ###################################################
###################################################           ###################################################
class TechnoVolumes(Base):
    __tablename__ = "techno_volumes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    volume_name = Column(String(255), unique=True, nullable=False)
    volume_logo = Column(String(255), nullable=False, default="static/categories/technos/volume_logo.png")
    volume_desc = Column(String(255), nullable=True)

    # Relationship to TechnoCategories
    categories = relationship("TechnoCategories", back_populates="volume")

    def __repr__(self):
        return f"<TechnoVolumes(name={self.volume_name})>"


class TechnoCategories(Base):
    __tablename__ = "techno_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255), unique=True, nullable=False)
    category_desc = Column(String(255), nullable=True)
    category_volume_id = Column(Integer, ForeignKey("techno_volumes.id"), nullable=False, default=1)

    # Relationship to TechnoVolumes
    volume = relationship("TechnoVolumes", back_populates="categories")

    # Relationship to TechnoGroups
    groups = relationship("TechnoGroups", back_populates="category")

    def __repr__(self):
        return f"<TechnoCategories(name={self.category_name})>"



class TechnoGroups(Base):
    __tablename__ = "techno_groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(255), unique=True, nullable=False)
    group_desc = Column(String(255), nullable=True)
    group_category_id = Column(Integer, ForeignKey("techno_categories.id"), nullable=False, default=1)

    # Relationship to TechnoCategories
    category = relationship("TechnoCategories", back_populates="groups")

    def __repr__(self):
        return f"<TechnoGroups(name={self.group_name})>"




class Techno(Base):
    __tablename__ = "techno_resources"

    techno_csr_code = Column(String(20), primary_key=True, nullable=False)  # Texnikaning klassifikatordagi kodi
    techno_name = Column(String(500), unique=True, nullable=False)  # Texnika nomi
    techno_desc = Column(String(255), nullable=True)  # Texnika tavsifi
    techno_measure = Column(String(25), nullable=False, default='kg')  # Texnika o‘lchov birligi
    techno_group_id = Column(BigInteger, ForeignKey("techno_groups.id"), nullable=True)  # Gruppaga bog'lanish
    techno_image = Column(String, nullable=True)  # Texnika uchun rasm
    techno_views_count = Column(Integer, nullable=False, default=0) 

class TechnoAds(Base):
    __tablename__ = "techno_ads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    techno_name_id = Column(String(20), ForeignKey("techno_resources.techno_csr_code"), nullable=False)
    techno_name = relationship("Techno", primaryjoin="Techno.techno_csr_code == foreign(TechnoAds.techno_name_id)", lazy="joined")

    techno_description = Column(String(500), nullable=True)
    techno_price = Column(Float, nullable=False)
    techno_price_currency = Column(String(15), nullable=False, default='UZS')
    techno_measure = Column(String(25), nullable=False)
    techno_image = Column(String, nullable=True)
    techno_amount = Column(Float, nullable=False)
    techno_amount_measure = Column(String(25), nullable=False)
    techno_status = Column(Boolean, default=True)
    techno_created_date = Column(DateTime, default=dt.utcnow)
    techno_updated_date = Column(DateTime, default=dt.utcnow)
    techno_deactivated_date = Column(DateTime, nullable=True)

    sertificate_blank_num = Column(String(10), nullable=False)
    sertificate_reestr_num = Column(String(10), nullable=False)

    techno_owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String(255), nullable=True)
    company_stir = Column(String(9), nullable=True)

    techno_region_id = Column(Integer, ForeignKey('uzb_regions.id'), nullable=True)  # Region (FK)
    region = relationship("Regions", backref="technos", lazy="joined")

    techno_district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)

###################################################            ###################################################
###################################################   MMECHNO  ###################################################
###################################################            ###################################################

class MMechanoCategories(Base):
    __tablename__ = "mmechano_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(255), unique=True, nullable=False, index=True)
    category_logo = Column(String(255), nullable=False, default='categories/m-mechano/category_logo.png')
    category_desc = Column(String(255), nullable=True)


class MMechanoGroups(Base):
    __tablename__ = "mmechano_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(255), unique=True, nullable=False)
    group_desc = Column(String(255), nullable=True)
    group_category_id = Column(Integer, ForeignKey('mmechano_categories.id', ondelete='SET DEFAULT'), nullable=True, default=1)
    
    group_category = relationship("MMechanoCategories", backref="mmechano_groups", lazy="joined")
class MMechano(Base):
    __tablename__ = "mmechano_resources"
    
    mmechano_csr_code = Column(String(20), primary_key=True, index=True)
    mmechano_name = Column(String(500), unique=True, nullable=False)
    mmechano_measure = Column(String(25), nullable=False, default='kg')
    mmechano_group_id = Column(Integer, ForeignKey('mmechano_groups.id', ondelete='SET DEFAULT'), nullable=True, default=1)


    # mmechano_group = relationship("MMechanoGroups", backref="mmechano_resources", lazy="joined")

class MMechanoAds(Base):
    __tablename__ = 'mmechano_ads'

    id = Column(Integer, primary_key=True, index=True)
    mmechano_name_id = Column(Integer, ForeignKey('mmechano.id'), nullable=False)  # Assuming 'mmechano.id' is the foreign table
    mmechano_description = Column(String(500), nullable=True)
    mmechano_rent_price = Column(Float)
    mmechano_rent_price_currency = Column(String(15), default='UZS')
    mmechano_measure = Column(String(25), default='kg')
    mmechano_image = Column(String(255), nullable=True)  # Image path stored as string
    mmechano_amount = Column(Float)
    mmechano_amount_measure = Column(String(25), default='kg')
    mmechano_status = Column(Boolean, default=True)
    mmechano_created_date = Column(DateTime, default=dt.utcnow)
    mmechano_updated_date = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow)
    mmechano_deactivated_date = Column(DateTime, nullable=True)
    sertificate_blank_num = Column(String(10))
    sertificate_reestr_num = Column(String(10))
    mmechano_owner_id = Column(Integer, ForeignKey('users.id'))  
    company_stir = Column(String(9), nullable=True)

    # Relationships
    mmechano_name = relationship("MMechano",primaryjoin="MMechano.mmechano_csr_code == foreign(MMechanoAds.mmechano_name_id)", lazy="joined")  # 'ads' is an example relationship name
  
###################################################             ###################################################
###################################################   MATERIAL  ###################################################
###################################################             ###################################################
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