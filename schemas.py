from pydantic import BaseModel
from typing import List, Optional, Dict
import datetime





class AdsResponseModel(BaseModel):
    Material_soni: int
    Mashina_va_mexanizlar_soni: int
    Kichik_mexnizimlar_soni: int
    Uskuna_va_qurilmalar: int
    combined_results: List[Dict] 

###################################################             ###################################################
###################################################   MATERIAL  ###################################################
###################################################             ###################################################

# MatVolume filteri uchun Pydantic modeli
class MatVolumeSchema(BaseModel):
    id: int
    volume_name: str
    # categories: List[str]

    class Config:
        from_attributes = True


# MatCategory filteri uchun Pydantic modeli
class MatCategorySchema(BaseModel):
    id: int
    category_name: str
    # groups: List[str]

    class Config:
        from_attributes = True

# MatGroup filteri uchun Pydantic modeli
class MatGroupSchema(BaseModel):
    id: int
    group_name: str
    # materials: List[str]

    class Config:
        from_attributes = True


class MaterialsSchema(BaseModel):
    material_name: str
    material_csr_code: str
    class Config:
        from_attributes = True
class MaterialAdsSchema(BaseModel):
    id: int
    material_name_id: str
    material_name: Optional[MaterialsSchema] = None 
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


###################################################            ###################################################
###################################################   MMECHNO  ###################################################
###################################################            ###################################################
class MMechanoCategoriesSchema(BaseModel):
    id: int
    category_name: str


    class Config:
        from_attributes = True

class MMechanoGroupsSchema(BaseModel):
    id: int
    group_name: str


    class Config:
        from_attributes = True

class MMechanoSchema(BaseModel):
    mmechano_name: str

    class Config:
        from_attributes = True

class MMechanoAdsSchema(BaseModel):
    id: int
    mmechano_name_id: str  # Changed to str if it's not an integer
    mmechano_name: Optional[MMechanoSchema] = None  # Nested schema for mmechano_name
    mmechano_description: Optional[str] = None
    mmechano_rent_price: float
    mmechano_rent_price_currency: str
    mmechano_measure: str
    mmechano_image: Optional[str] = None
    mmechano_amount: float
    mmechano_amount_measure: str
    mmechano_status: bool
    mmechano_created_date: datetime.datetime
    mmechano_updated_date: datetime.datetime
    mmechano_deactivated_date: Optional[datetime.datetime] = None
    sertificate_blank_num: str
    sertificate_reestr_num: str
    mmechano_owner_id: int
    company_name: Optional[str] = None
    company_stir: Optional[str] = None

    class Config:
        from_attributes = True



###################################################           ###################################################
###################################################   TECHNO  ###################################################
###################################################           ###################################################
class TechnoVolumesSchema(BaseModel):
    id: int
    volume_name: str
    volume_logo: str
    volume_desc: Optional[str]

    class Config:
        from_attributes = True 




class TechnoCategoriesSchema(BaseModel):
    id: int
    category_name: str
    category_desc: Optional[str]
    # category_volume_id: int

    class Config:
        from_attributes = True 


class TechnoGroupsSchema(BaseModel):
    id: int
    group_name: str
    group_desc: Optional[str]
    # group_category_id: int

    class Config:
        from_attributes = True 
class TechnoSchema(BaseModel):
 
    techno_name: str
    techno_csr_code : str

    class Config:
        # from_attributes = True   # Pydantic 1.x uchun
        from_attributes = True  # Pydantic 2.x uchun






class TechnoAdsSchema(BaseModel):
    id: int
    techno_name: TechnoSchema  # Nested schema uchun
    techno_description: Optional[str]
    techno_price: float
    techno_price_currency: str
    techno_measure: str
    techno_image: Optional[str]
    techno_amount: float
    techno_amount_measure: str
    techno_status: bool
    techno_created_date: datetime.datetime
    techno_updated_date: datetime.datetime
    techno_deactivated_date: Optional[datetime.datetime] = None
    sertificate_blank_num: str
    sertificate_reestr_num: str
    techno_owner: int  # ForeignKey uchun user id
    company_name: Optional[str]
    company_stir: Optional[str]
    techno_region: Optional[int]  # ForeignKey uchun id
    techno_district: Optional[int]  # ForeignKey uchun id

    class Config:
        # orm_mode = True  # Pydantic 1.x uchun
        from_attributes = True  # Pydantic 2.x uchun