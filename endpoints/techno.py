from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import TechnoVolumes, TechnoCategories, TechnoGroups, Techno, TechnoAds, Regions  # Import the techno models
from schemas import TechnoVolumesSchema, TechnoCategoriesSchema, TechnoGroupsSchema  # Import corresponding schemas
from database import get_db  # Dependency to get DB session
from typing import List, Optional
from sqlalchemy import func
from math import ceil
from datetime import datetime
techno_router = APIRouter(tags=["Techno"])


@techno_router.get("/techno_volume/", response_model=List[TechnoVolumesSchema])
async def get_techno_volumes(db: Session = Depends(get_db)):
    volumes = db.query(TechnoVolumes).all()
    return volumes


@techno_router.get("/techno_categories/{volume_id}", response_model=List[TechnoCategoriesSchema])
async def get_techno_categories(volume_id: int, db: Session = Depends(get_db)):
    categories = db.query(TechnoCategories).filter(TechnoCategories.category_volume_id == volume_id).all()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found for the given volume")
    return categories


@techno_router.get("/techno_groups/{category_id}", response_model=List[TechnoGroupsSchema])
async def get_techno_groups(category_id: int, db: Session = Depends(get_db)):
    groups = db.query(TechnoGroups).filter(TechnoGroups.group_category_id == category_id).all()
    if not groups:
        raise HTTPException(status_code=404, detail="No groups found for the given category")
    return groups


@techno_router.post("/techno_ads/", response_model=dict)
async def get_techno_ads(group_ids: List[int], db: Session = Depends(get_db)):
    technos = db.query(Techno).filter(Techno.techno_group_id.in_(group_ids)).all()
    if not technos:
        raise HTTPException(status_code=404, detail="No technos found for the given groups")

    ads = []
    for techno in technos:
        ads_for_techno = db.query(TechnoAds).filter(TechnoAds.techno_name_id == techno.techno_csr_code).all()
        ads.extend(ads_for_techno)

    if not ads:
        raise HTTPException(status_code=404, detail="No ads found for the given technos")

    return {
        "count": len(ads),
        "technos": [
            {
                "id": ad.id,
                "techno_name_id": ad.techno_name_id,
                "techno_description": ad.techno_description,
                "techno_price": ad.techno_price,
                "techno_price_currency": ad.techno_price_currency,
                "techno_measure": ad.techno_measure,
                "techno_image": ad.techno_image,
                "techno_amount": ad.techno_amount,
                "techno_amount_measure": ad.techno_amount_measure,
                "techno_status": ad.techno_status,
                "techno_created_date": ad.techno_created_date,
                "techno_updated_date": ad.techno_updated_date,
                "techno_deactivated_date": ad.techno_deactivated_date,
                "sertificate_blank_num": ad.sertificate_blank_num,
                "sertificate_reestr_num": ad.sertificate_reestr_num,
                "techno_owner_id": ad.techno_owner_id,
                "company_name": ad.company_name,
                "company_stir": ad.company_stir,
                "techno_region_name": ad.region.region_name_uz if ad.region and ad.region.region_name_uz else None,
                "techno_name": ad.techno_name.techno_name if ad.techno_name else None,
            }
            for ad in ads
        ]
    }



@techno_router.get("/techno-ads/filter", response_model=dict)
async def filter_techno_ads(
    region_name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    date: Optional[datetime] = None,
    page: int = 1,  # Default to page 1
    page_size: int = 12,  # Default to 12 items per page
    db: Session = Depends(get_db)
):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Page and page size must be positive integers.")

    query = db.query(TechnoAds)

    if region_name:
        query = query.join(Regions).filter(Regions.region_name_uz == region_name)
    if date:
        query = query.filter(func.date(TechnoAds.techno_updated_date) == date)
    if min_price is not None:
        query = query.filter(TechnoAds.techno_price >= min_price)
    if max_price is not None:
        query = query.filter(TechnoAds.techno_price <= max_price)

    total_items = query.count()  # Total number of records
    total_pages = ceil(total_items / page_size)

    if page > total_pages and total_items > 0:
        raise HTTPException(status_code=404, detail="Page out of range")

    # Apply pagination
    techno_ads = query.offset((page - 1) * page_size).limit(page_size).all()

    if not techno_ads:
        raise HTTPException(status_code=404, detail="No techno ads found for the given filters")

    return {
        "count": len(techno_ads),
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "techno_ads": [
            {
                "id": techno.id,
                "techno_name_id": techno.techno_name_id,
                "techno_description": techno.techno_description,
                "techno_price": techno.techno_price,
                "techno_price_currency": techno.techno_price_currency,
                "techno_measure": techno.techno_measure,
                "techno_image": techno.techno_image,
                "techno_amount": techno.techno_amount,
                "techno_amount_measure": techno.techno_amount_measure,
                "techno_status": techno.techno_status,
                "techno_created_date": techno.techno_created_date,
                "techno_updated_date": techno.techno_updated_date,
                "techno_deactivated_date": techno.techno_deactivated_date,
                "sertificate_blank_num": techno.sertificate_blank_num,
                "sertificate_reestr_num": techno.sertificate_reestr_num,
                "techno_owner_id": techno.techno_owner_id,
                "company_name": techno.company_name,
                "company_stir": techno.company_stir,
                "techno_region_name": techno.region.region_name_uz if techno.region else None,
                "techno_district_id": techno.techno_district_id,
                "techno_name": techno.techno_name.techno_name if techno.techno_name else None
            }
            for techno in techno_ads
        ]
    }
