from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Optional
from math import ceil
from datetime import datetime
from models import MMechanoCategories, MMechanoGroups, MMechano, MMechanoAds, Regions
from schemas import MMechanoCategoriesSchema, MMechanoGroupsSchema
from database import get_db

mmechano_router = APIRouter(tags=["MMechano"])


@mmechano_router.get("/mmechano_categories/", response_model=List[MMechanoCategoriesSchema])
async def get_mmechano_categories(db: Session = Depends(get_db)):
    categories = db.query(MMechanoCategories).all()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return categories


@mmechano_router.get("/mmechano_groups/{category_id}", response_model=List[MMechanoGroupsSchema])
async def get_mmechano_groups(category_id: int, db: Session = Depends(get_db)):
    groups = db.query(MMechanoGroups).filter(MMechanoGroups.group_category_id == category_id).all()
    if not groups:
        raise HTTPException(status_code=404, detail="No groups found for the given category")
    return groups


@mmechano_router.post("/mmechano_ads/", response_model=dict)
async def get_mmechano_ads(
    group_ids: List[int],
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Page and page size must be positive integers.")

    mmechanos = db.query(MMechano).filter(MMechano.mmechano_group_id.in_(group_ids)).all()
    if not mmechanos:
        raise HTTPException(status_code=404, detail="No mmechanos found for the given groups")

    ads = []
    for mmechano in mmechanos:
        ads_for_mmechano = db.query(MMechanoAds).filter(MMechanoAds.mmechano_name_id == mmechano.mmechano_csr_code).all()
        ads.extend(ads_for_mmechano)

    if not ads:
        raise HTTPException(status_code=404, detail="No ads found for the given mmechanos")

    total_items = len(ads)
    total_pages = ceil(total_items / page_size)

    if page > total_pages and total_items > 0:
        raise HTTPException(status_code=404, detail="Page out of range")

    start = (page - 1) * page_size
    end = start + page_size
    paginated_ads = ads[start:end]

    return {
        "count": len(paginated_ads),
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "mmechano_ads": [
            {
                "id": ad.id,
                "mmechano_name_id": ad.mmechano_name_id,
                "mmechano_description": ad.mmechano_description,
                "mmechano_rent_price": ad.mmechano_rent_price,
                "mmechano_rent_price_currency": ad.mmechano_rent_price_currency,
                "mmechano_measure": ad.mmechano_measure,
                "mmechano_image": ad.mmechano_image,
                "mmechano_amount": ad.mmechano_amount,
                "mmechano_amount_measure": ad.mmechano_amount_measure,
                "mmechano_status": ad.mmechano_status,
                "mmechano_created_date": ad.mmechano_created_date,
                "mmechano_updated_date": ad.mmechano_updated_date,
                "mmechano_deactivated_date": ad.mmechano_deactivated_date,
                "sertificate_blank_num": ad.sertificate_blank_num,
                "sertificate_reestr_num": ad.sertificate_reestr_num,
                "mmechano_owner_id": ad.mmechano_owner_id,
                "company_stir": ad.company_stir,
                "mmechano_name": ad.mmechano_name.mmechano_name if ad.mmechano_name else None,
            }
            for ad in paginated_ads
        ]
    }


@mmechano_router.get("/mmechano_ads/filter", response_model=dict)
async def filter_mmechano_ads(
    region_name: Optional[str] = None,
    min_rent_price: Optional[float] = None,
    max_rent_price: Optional[float] = None,
    date: Optional[datetime] = None,
    name_value: Optional[str] = None,
    csr_code_value: Optional[str] = None,
    page: int = 1,
    page_size: int = 12,
    db: Session = Depends(get_db)
):
    query = db.query(MMechanoAds).join(MMechano, MMechano.mmechano_csr_code == MMechanoAds.mmechano_name_id)

    if name_value:
        query = query.filter(MMechano.mmechano_name.ilike(f"%{name_value}%"))

    if csr_code_value:
        query = query.filter(MMechano.mmechano_csr_code.ilike(f"%{csr_code_value}%"))

    if name_value:
        query = query.order_by(
            case(
                (MMechano.mmechano_name.ilike(f"{name_value}%"), 1),
                else_=2
            ),
            MMechano.mmechano_name
        )
    else:
        query = query.order_by(MMechano.mmechano_name)

    if region_name:
        query = query.join(Regions).filter(Regions.region_name_uz == region_name)
    if date:
        query = query.filter(func.date(MMechanoAds.mmechano_updated_date) == date)
    if min_rent_price is not None:
        query = query.filter(MMechanoAds.mmechano_rent_price >= min_rent_price)
    if max_rent_price is not None:
        query = query.filter(MMechanoAds.mmechano_rent_price <= max_rent_price)

    total_items = query.count()
    total_pages = ceil(total_items / page_size)

    if page > total_pages and total_items > 0:
        raise HTTPException(status_code=404, detail="Page out of range")

    mmechano_ads = query.offset((page - 1) * page_size).limit(page_size).all()

    if not mmechano_ads:
        raise HTTPException(status_code=404, detail="No mmechano ads found for the given filters")

    return {
        "count": len(mmechano_ads),
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "mmechano_ads": [
            {
                "id": ad.id,
                "mmechano_name_id": ad.mmechano_name_id,
                "mmechano_description": ad.mmechano_description,
                "mmechano_rent_price": ad.mmechano_rent_price,
                "mmechano_rent_price_currency": ad.mmechano_rent_price_currency,
                "mmechano_measure": ad.mmechano_measure,
                "mmechano_image": ad.mmechano_image,
                "mmechano_amount": ad.mmechano_amount,
                "mmechano_amount_measure": ad.mmechano_amount_measure,
                "mmechano_status": ad.mmechano_status,
                "mmechano_created_date": ad.mmechano_created_date,
                "mmechano_updated_date": ad.mmechano_updated_date,
                "mmechano_deactivated_date": ad.mmechano_deactivated_date,
                "sertificate_blank_num": ad.sertificate_blank_num,
                "sertificate_reestr_num": ad.sertificate_reestr_num,
                "mmechano_owner_id": ad.mmechano_owner_id,
                "company_stir": ad.company_stir,
                "mmechano_name": ad.mmechano_name.mmechano_name if ad.mmechano_name else None,
            }
            for ad in mmechano_ads
        ]
    }
