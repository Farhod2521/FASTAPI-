from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from database import get_db
from models import Materials, MMechano, Techno, MaterialAds, Regions, TechnoAds, MMechanoAds
from schemas import MaterialAdsSchema, MaterialsSchema


from typing import List, Optional
from datetime import datetime
from sqlalchemy import case
from sqlalchemy import func


app_main_router =  APIRouter(tags=["Main"])







@app_main_router.get("/monitoring/region/list/", response_model=dict)
async def monitoring_list(db: Session = Depends(get_db)):
    andijon_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Andijon")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Andijon")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Andijon")
        # .count()
    )
    buxoro_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Buxoro")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Buxoro")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Buxoro")
        # .count()
    )
    fargona_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Fargona")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Fargona")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Fargona")
        # .count()
    )
    jizzax_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Jizzax")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Jizzax")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Jizzax")
        # .count()
    )
    xorazm_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Xorazm")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Xorazm")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Xorazm")
        # .count()
    )
    namangan_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Namangan")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Namangan")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Namangan")
        # .count()
    )
    navoiy_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Navoiy")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Navoiy")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Navoiy")
        # .count()
    )
    qashqadaryo_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Qashqadaryo")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Qashqadaryo")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Qashqadaryo")
        # .count()
    )
    qoraqalpogiston_total = (
    db.query(MaterialAds)
    .join(Regions)
    .filter(Regions.region_name_uz == "Qoraqalpogiston Respublikasi")
    .count()
    +
    db.query(TechnoAds)
    .join(Regions)
    .filter(Regions.region_name_uz == "Qoraqalpogiston Respublikasi")
    .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Qoraqalpogʻiston Respublikasi")
        # .count()
    )
    samarqand_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Samarqand")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Samarqand")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Samarqand")
        # .count()
    )
    sirdaryo_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Sirdaryo")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Sirdaryo")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Sirdaryo")
        # .count()
    )
    surxandaryo_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Surxondaryo")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Surxondaryo")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Surxandaryo")
        # .count()
    )
    toshkent_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Toshkent")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Toshkent")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Toshkent")
        # .count()
    )
    toshkent_shahri_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Toshkent shahri")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Toshkent shahri")
        .count()
        # +
        # db.query(MMechanoAds)
        # .join(Regions)
        # .filter(Regions.region_name_uz == "Toshkent shahri")
        # .count()
    )
    
    result = {
        "Andijon viloyati (Jami)": andijon_total,
        "Buxoro viloyati (Jami)": buxoro_total,
        "Fargʻona viloyati (Jami)": fargona_total,
        "Jizzax viloyati (Jami)": jizzax_total,
        "Xorazm viloyati (Jami)": xorazm_total,
        "Namangan viloyati (Jami)": namangan_total,
        "Navoiy viloyati (Jami)": navoiy_total,
        "Qashqadaryo viloyati (Jami)": qashqadaryo_total,
        "Qoraqalpogʻiston Respublikasi (Jami)": qoraqalpogiston_total,
        "Samarqand viloyati (Jami)": samarqand_total,
        "Sirdaryo viloyati(Jami)": sirdaryo_total,
        "Surxondaryo viloyati(Jami)": surxandaryo_total,
        "Toshkent viloyati (Jami)": toshkent_total,
        "Toshkent shahri (Jami)": toshkent_shahri_total
    }
    return result








@app_main_router.get("/monitoring/region/filter/", response_model=dict)
async def filter_materials(
    region_name: Optional[str] = None,
    page: int = 1,
    limit: int = 24,
    db: Session = Depends(get_db)
):
    # Calculate offset based on the page and limit
    offset = (page - 1) * limit
    
    query = db.query(MaterialAds)

    if region_name:
        query = query.join(Regions).filter(Regions.region_name_uz == region_name)

    query = query.offset(offset).limit(limit)

    materials = query.all()

    if not materials:
        raise HTTPException(status_code=404, detail="No materials found for the given filters")
    total_count = query.count()

    return {
        "page": page,
        "limit": limit,
        "materials": [
            {
                "id": material.id,
                "material_name_id": material.material_name_id,
                "material_name": db.query(Materials).filter(Materials.material_csr_code == material.material_name_id).first().material_name if db.query(Materials).filter(Materials.material_csr_code == material.material_name_id).first() else None,
                "material_description": material.material_description,
                "material_price": material.material_price,
                "material_price_currency": material.material_price_currency,
                "material_measure": material.material_measure,
                "material_image": material.material_image,
                "material_amount": material.material_amount,
                "material_amount_measure": material.material_amount_measure,
                "material_status": material.material_status,
                "material_created_date": material.material_created_date,
                "material_updated_date": material.material_updated_date,
                "material_deactivated_date": material.material_deactivated_date,
                "sertificate_blank_num": material.sertificate_blank_num,
                "sertificate_reestr_num": material.sertificate_reestr_num,
                "material_owner_id": material.material_owner_id,
                "company_name": material.company_name,
                "company_stir": material.company_stir,
                "material_region_name": material.region.region_name_uz if material.region else None,
                "material_district_id": material.material_district_id,
            }
            for material in materials
        ]
    }
# @app_main_router.get("/monitoring/region/filter/", response_model=dict)
# async def monitor_region_filter(
#     region_name: Optional[str] = None,
#     page: int = 1,
#     limit: int = 50,
#     db: Session = Depends(get_db)
# ):
#     if not region_name:
#         raise HTTPException(status_code=400, detail="Region name is required")

#     # Paginated query for Materials
#     material_query = db.query(Materials).join(Regions).filter(Regions.region_name_uz == region_name)
#     total_materials = material_query.count()  # Get the total count for pagination
#     materials = material_query.offset((page - 1) * limit).limit(limit).all()

#     # Paginated query for TechnoAds
#     techno_query = db.query(TechnoAds).join(Regions).filter(Regions.region_name_uz == region_name)
#     total_techno_ads = techno_query.count()
#     techno_ads = techno_query.offset((page - 1) * limit).limit(limit).all()

#     # Paginated query for MMechanoAds
#     mmechano_query = db.query(MMechanoAds).join(Regions).filter(Regions.region_name_uz == region_name)
#     total_mmechano_ads = mmechano_query.count()
#     mmechano_ads = mmechano_query.offset((page - 1) * limit).limit(limit).all()

#     total_items = total_materials + total_techno_ads + total_mmechano_ads
#     total_pages = (total_items + limit - 1) // limit  # Calculate total pages

#     # Combine the results
#     result = {
#         "count": total_items,
#         "total_items": total_items,
#         "total_pages": total_pages,
#         "current_page": page,
#         "items": []
#     }

#     # Add Materials to the response
#     for material in materials:
#         material_name = db.query(Materials).filter(Materials.material_csr_code == material.material_name_id).first()
#         result["items"].append({
#             "type": "MaterialAds",
#             "id": material.id,
#             "material_name": material_name.material_name if material_name else None,
#             "material_description": material.material_description,
#             "material_price": material.material_price,
#             "material_price_currency": material.material_price_currency,
#             "material_measure": material.material_measure,
#             "material_image": material.material_image,
#             "material_amount": material.material_amount,
#             "material_amount_measure": material.material_amount_measure,
#             "material_status": material.material_status,
#             "material_created_date": material.material_created_date,
#             "material_updated_date": material.material_updated_date,
#             "material_deactivated_date": material.material_deactivated_date,
#             "sertificate_blank_num": material.sertificate_blank_num,
#             "sertificate_reestr_num": material.sertificate_reestr_num,
#             "material_owner_id": material.material_owner_id,
#             "company_name": material.company_name,
#             "company_stir": material.company_stir,
#             "material_region_name": material.region.region_name_uz if material.region else None,
#             "material_district_id": material.material_district_id,
#         })

#     # Add TechnoAds to the response
#     for ad in techno_ads:
#         result["items"].append({
#             "type": "TechnoAds",
#             "id": ad.id,
#             "techno_name": ad.techno_name.techno_name if ad.techno_name else None,
#             "techno_description": ad.techno_description,
#             "techno_price": ad.techno_price,
#             "techno_price_currency": ad.techno_price_currency,
#             "techno_measure": ad.techno_measure,
#             "techno_image": ad.techno_image,
#             "techno_amount": ad.techno_amount,
#             "techno_amount_measure": ad.techno_amount_measure,
#             "techno_status": ad.techno_status,
#             "techno_created_date": ad.techno_created_date,
#             "techno_updated_date": ad.techno_updated_date,
#             "techno_deactivated_date": ad.techno_deactivated_date,
#             "sertificate_blank_num": ad.sertificate_blank_num,
#             "sertificate_reestr_num": ad.sertificate_reestr_num,
#             "techno_owner_id": ad.techno_owner_id,
#             "company_name": ad.company_name,
#             "company_stir": ad.company_stir,
#             "techno_region_name": ad.region.region_name_uz if ad.region else None,
#         })

#     # Add MMechanoAds to the response
#     for ad in mmechano_ads:
#         result["items"].append({
#             "type": "MMechnoAds",
#             "id": ad.id,
#             "mmechano_name": ad.mmechano_name.mmechano_name if ad.mmechano_name else None,
#             "mmechano_description": ad.mmechano_description,
#             "mmechano_rent_price": ad.mmechano_rent_price,
#             "mmechano_rent_price_currency": ad.mmechano_rent_price_currency,
#             "mmechano_measure": ad.mmechano_measure,
#             "mmechano_image": ad.mmechano_image,
#             "mmechano_amount": ad.mmechano_amount,
#             "mmechano_amount_measure": ad.mmechano_amount_measure,
#             "mmechano_status": ad.mmechano_status,
#             "mmechano_created_date": ad.mmechano_created_date,
#             "mmechano_updated_date": ad.mmechano_updated_date,
#             "mmechano_deactivated_date": ad.mmechano_deactivated_date,
#             "sertificate_blank_num": ad.sertificate_blank_num,
#             "sertificate_reestr_num": ad.sertificate_reestr_num,
#             "mmechano_owner_id": ad.mmechano_owner_id,
#             "company_stir": ad.company_stir,
#         })

#     return result

@app_main_router.get("/global/search/", response_model=dict)
async def global_search(
    name_value: Optional[str] = None,
    category: Optional[str] = None,
    page: int = 1,
    limit: int = 12,
    db: Session = Depends(get_db),
):
    page = max(page, 1)
    limit = max(limit, 1)
    offset = (page - 1) * limit
    
    if category == "material":
        query = db.query(Materials)
        
        if name_value:
            query = query.filter(Materials.material_name.ilike(f"%{name_value}%"))
            query = query.order_by(
                case(
                    (Materials.material_name.ilike(f"{name_value}%"), 1),
                    else_=2
                ),
                Materials.material_name,
            )
        else:
            query = query.order_by(Materials.material_name)
        
        all_data = query.offset(offset).limit(limit).all()
        count = query.count()
        

        
        if count == 0:
            return {"count": 0, "materials": []}
        
        result = {
            "count": count,
            "materials": [
                {
                    "material_csr_code": mat.material_csr_code,
                    "material_name": mat.material_name,
                }
                for mat in all_data
            ],
        }
        return result

    elif category == "mmechno":
        query = db.query(MMechano)
        
        if name_value:
            query = query.filter(MMechano.mmechano_name.ilike(f"%{name_value}%"))
            query = query.order_by(
                case(
                    (MMechano.mmechano_name.ilike(f"{name_value}%"), 1),
                    else_=2
                ),
                MMechano.mmechano_name,
            )
        else:
            query = query.order_by(MMechano.mmechano_name)
        
        all_data = query.offset(offset).limit(limit).all()
        count = query.count()

        
        if count == 0:
            return {"count": 0, "mmechano": []}
        
        result = {
            "count": count,
            "mmechano": [
                {
                    "mmechano_csr_code": mat.mmechano_csr_code,
                    "mmechano_name": mat.mmechano_name,
                }
                for mat in all_data
            ],
        }
        return result

    elif category == "techno":
        query = db.query(Techno)
        
        if name_value:
            query = query.filter(Techno.techno_name.ilike(f"%{name_value}%"))
            query = query.order_by(
                case(
                    (Techno.techno_name.ilike(f"{name_value}%"), 1),
                    else_=2
                ),
                Techno.techno_name,
            )
        else:
            query = query.order_by(Techno.techno_name)
        
        all_data = query.offset(offset).limit(limit).all()
        count = query.count()

        if count == 0:
            return {"count": 0, "techno": []}
        
        result = {
            "count": count,
            "techno": [
                {
                    "techno_csr_code": mat.techno_csr_code,
                    "techno_name": mat.techno_name,
                }
                for mat in all_data
            ],
        }
        return result
    else:
        result = {
            "message": "Category kiritish kerak !!!",
        }
        return result

