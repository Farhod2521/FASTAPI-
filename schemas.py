from pydantic import BaseModel
from typing import List, Optional
import datetime










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
