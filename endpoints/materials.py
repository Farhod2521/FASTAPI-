from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models import MaterialAds, Regions, Materials, MatVolumes, MatCategories, MatGroups, MMechanoAds, Techno, TechnoAds
from schemas import MaterialAdsSchema, MatVolumeSchema, MatCategorySchema, MatGroupSchema, MMechanoAdsSchema, AdsResponseModel, TechnoSchema, TechnoAdsSchema
from typing import List, Optional
import jwt
from datetime import datetime
import requests




materials_router = APIRouter()


from sqlalchemy import case
from sqlalchemy import func

@materials_router.get("/telegram_bot/search/", response_model=dict)
async def material_name_csr_code_search(
    name_value: Optional[str] = None,
    code_value: Optional[str] = None,
    page: int = 1,
    limit: int = 24,
    db: Session = Depends(get_db)
):
    query = (
        db.query(
            Materials,)
    )

    # Apply filters if the user has provided `name_value` or `code_value`
    if name_value:
        query = query.filter(Materials.material_name.ilike(f"%{name_value}%"))
    
    if code_value:
        query = query.filter(Materials.material_csr_code.ilike(f"%{code_value}%"))

    # Order results to prioritize matches that start with name_value
    if name_value:
        query = query.order_by(
            case(
                (Materials.material_name.ilike(f"{name_value}%"), 1),
                else_=2
            ),
            Materials.material_name
        )
    else:
        query = query.order_by(Materials.material_name)

    # Pagination
    offset = (page - 1) * limit
    material_data = query.offset(offset).limit(limit).all()
    count =  query.count()
    result = {
        "count": count,
        "materials": [
            {
                "material_csr_code": mat.material_csr_code,
                "material_name": mat.material_name,
                "material_measure": mat.material_measure,
            }
            for mat in material_data
        ]
    }
    return result

@materials_router.get("/material/search/", response_model=dict)
async def material_name_csr_code_search(
    name_value: Optional[str] = None,
    code_value: Optional[str] = None,
    page: int = 1,
    limit: int = 24,
    db: Session = Depends(get_db)
):
    query = (
        db.query(
            Materials,
            MatGroups.id.label("group_id"),
            MatGroups.group_name, 
            MatCategories.id.label("category_id"),
            MatCategories.category_name,
            MatVolumes.id.label("volume_id"),
            MatVolumes.volume_name
        )
        .join(MatGroups, Materials.material_group_id == MatGroups.id)
        .join(MatCategories, MatGroups.group_category_id == MatCategories.id)
        .join(MatVolumes, MatCategories.category_volume_id == MatVolumes.id)
    )

    # Apply filters if the user has provided `name_value` or `code_value`
    if name_value:
        query = query.filter(Materials.material_name.ilike(f"%{name_value}%"))
    
    if code_value:
        query = query.filter(Materials.material_csr_code.ilike(f"%{code_value}%"))

    # Order results to prioritize matches that start with name_value
    if name_value:
        query = query.order_by(
            case(
                (Materials.material_name.ilike(f"{name_value}%"), 1),
                else_=2
            ),
            Materials.material_name
        )
    else:
        query = query.order_by(Materials.material_name)

    # Pagination
    offset = (page - 1) * limit
    material_data = query.offset(offset).limit(limit).all()
    count =  query.count()
    result = {
        "count":count,
        "materials": [
            {
                "material_csr_code": mat.Materials.material_csr_code,
                "material_name": mat.Materials.material_name,
                "material_desc": mat.Materials.material_desc,
                "material_measure": mat.Materials.material_measure,
                "material_image": mat.Materials.material_image,
                "material_views_count": mat.Materials.material_views_count,
                "materil_gost": mat.Materials.materil_gost,
                "material_group_name": mat.group_name,
                "material_group_id": mat.group_id,
                "material_category_name": mat.category_name,
                "material_category_id": mat.category_id,
                "material_volume_name": mat.volume_name,
                "material_volume_id": mat.volume_id
            }
            for mat in material_data
        ]
    }
    return result




@materials_router.get("/material/name_group_category/", response_model=dict)
async def material_name_group_category(
    material_name: Optional[str] = None,
    material_csr: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = (
        db.query(
            Materials,
            MatGroups.group_name,
            MatCategories.category_name,
            MatVolumes.volume_name
        )
        .join(MatGroups, Materials.material_group_id == MatGroups.id)
        .join(MatCategories, MatGroups.group_category_id == MatCategories.id)
        .join(MatVolumes, MatCategories.category_volume_id == MatVolumes.id)
    )

    if material_csr:
        query = query.filter(Materials.material_csr_code == material_csr)
    if material_name:
        query = query.filter(Materials.material_name == material_name)

    material_data = query.all()

    result = {
        "materials": [
            {
                "material_csr_code": mat.Materials.material_csr_code,
                "material_name": mat.Materials.material_name,
                "material_desc": mat.Materials.material_desc,
                "material_measure": mat.Materials.material_measure,
                "material_image": mat.Materials.material_image,
                "material_views_count": mat.Materials.material_views_count,
                "materil_gost": mat.Materials.materil_gost,
                "material_group_name": mat.group_name,
                "material_category_name": mat.category_name,
                "material_volume_name": mat.volume_name
            }
            for mat in material_data
        ]
    }
    return result











# MaterialAds obyektlarini filterlash uchun API
@materials_router.get("/materials/filter", response_model=dict)
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
@materials_router.get("/materials/", response_model=List[MaterialAdsSchema])
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



@materials_router.get("/all/ads/", response_model=AdsResponseModel)
async def get_all_ads(request: Request, page: int = 1, limit: int = 24, db: Session = Depends(get_db)):
    try:
        skip = (page - 1) * limit

        # Ads query
        ads_query = db.query(MMechanoAds).filter(
            MMechanoAds.mmechano_status == True,
            MMechanoAds.company_stir == 310037819
        )
        mmechano_count = ads_query.count()

        # Material query
        material_query = db.query(MaterialAds).filter(
            MaterialAds.material_status == True,
            MaterialAds.company_stir == 310037819
        )
        material_count = material_query.count()

        # techno_query = db.query(TechnoAds).filter(
        #     TechnoAds.techno_status == True,
        #     TechnoAds.company_stir == 310037819
        # )
        # techno_count = techno_query.count()

        # Sorting logic
        mmechno_sort_by = request.query_params.get('sort_by', '-mmechano_updated_date')
        if mmechno_sort_by.startswith('-'):
            ads_query = ads_query.order_by(getattr(MMechanoAds, mmechno_sort_by[1:]).desc())
        else:
            ads_query = ads_query.order_by(getattr(MMechanoAds, mmechno_sort_by))
        
        material_sort_by = request.query_params.get('sort_by', '-material_updated_date')
        if material_sort_by.startswith('-'):
            material_query = material_query.order_by(getattr(MaterialAds, material_sort_by[1:]).desc())
        else:
            material_query = material_query.order_by(getattr(MaterialAds, material_sort_by))

        # Apply pagination
        all_ads = ads_query.offset(skip).limit(limit).all()
        all_materials = material_query.offset(skip).limit(limit).all()
      
        # Combine results
        combined_results = []
        combined_results.extend([MaterialAdsSchema.from_orm(mat).dict() for mat in all_materials])
        combined_results.extend([MMechanoAdsSchema.from_orm(ad).dict() for ad in all_ads])
        
        

        return AdsResponseModel(
            Material_soni=material_count,
            Mashina_va_mexanizlar_soni=mmechano_count,
            Kichik_mexnizimlar_soni= 0,
            Uskuna_va_qurilmalar = 0,
            combined_results=combined_results
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# MaterialVolume bo'yicha filterlash
@materials_router.get("/materials/volume/{volume_id}", response_model=MatVolumeSchema)
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
@materials_router.get("/materials/categories/{category_id}", response_model=MatCategorySchema)
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
@materials_router.get("/materials/groups/{group_id}", response_model=MatGroupSchema)
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

from elasticsearch import Elasticsearch
from pydantic import BaseModel
es = Elasticsearch(["https://localhost:9200"], verify_certs=False)


# Material modelini belgilash uchun Pydantic modelini yaratamiz
class MaterialSearch(BaseModel):
    material_name: str

# Elasticsearchdan ma'lumot qidirish uchun API endpoint
@materials_router.post("/materials/search/")
async def search_materials(query: MaterialSearch):
    # Elasticsearch qidiruv so'rovi
    search_query = {
        "query": {
            "match": {
                "material_name": query.material_name
            }
        }
    }
    response = es.search(index="materials_index", body=search_query)
    
    # Qidiruv natijalarini formatlash
    results = [
        {
            "material_csr_code": hit["_source"]["material_csr_code"],
            "material_name": hit["_source"]["material_name"],
            "material_desc": hit["_source"].get("material_desc"),
            "material_measure": hit["_source"].get("material_measure")
        }
        for hit in response["hits"]["hits"]
    ]
    return {"results": results}