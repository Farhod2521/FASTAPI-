from fastapi import APIRouter, Depends, HTTPException

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













@app_main_router.get("/global/search/", response_model=dict)
async def global_search(
    name_value: Optional[str] = None,
    category: Optional[str]= None,
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
                case((Materials.material_name.ilike(f"{name_value}%"), 1), else_=2),
                Materials.material_name,
            )
        else:
            query = query.order_by(Materials.material_name)
        
        all_data = query.offset(offset).limit(limit).all()
        count = query.count()
        
        print(f"Query Params - name_value: {name_value}, category: {category}, page: {page}, limit: {limit}")
        print(f"Retrieved Data: {all_data}")
        
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
                case((MMechano.mmechano_name.ilike(f"{name_value}%"), 1), else_=2),
                MMechano.mmechano_name,
            )
        else:
            query = query.order_by(MMechano.mmechano_name)
        
        all_data = query.offset(offset).limit(limit).all()
        count = query.count()
        
        print(f"Query Params - name_value: {name_value}, category: {category}, page: {page}, limit: {limit}")
        print(f"Retrieved Data: {all_data}")
        
        if count == 0:
            return {"count": 0, "mmechno": []}
        
        result = {
            "count": count,
            "materials": [
                {
                    "mmechano_csr_code": mat.mmechano_csr_code,
                    "mmechano_name": mat.mmechano_name,
                }
                for mat in all_data
            ],
        }
        return result
    elif  category == "techno":
        query = db.query(Techno)
        
        if name_value:
            query = query.filter(Techno.techno_name.ilike(f"%{name_value}%"))
            query = query.order_by(
                case((Techno.techno_name.ilike(f"{name_value}%"), 1), else_=2),
                Techno.techno_name,
            )
        else:
            query = query.order_by(Techno.techno_name)
        
        all_data = query.offset(offset).limit(limit).all()
        count = query.count()
        
        print(f"Query Params - name_value: {name_value}, category: {category}, page: {page}, limit: {limit}")
        print(f"Retrieved Data: {all_data}")
        
        if count == 0:
            return {"count": 0, "techno": []}
        
        result = {
            "count": count,
            "materials": [
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


