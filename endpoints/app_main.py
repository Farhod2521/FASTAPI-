from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from database import get_db
from models import Materials, MMechano, Techno, MaterialAds, Regions, TechnoAds, MMechanoAds
from schemas import MaterialAdsSchema, MaterialsSchema


from typing import List, Optional
from datetime import datetime
from sqlalchemy import case
from sqlalchemy import func, distinct
import httpx

app_main_router =  APIRouter(tags=["Main"])

############################## BIRJA API #################################################
@app_main_router.get("/birja_data/", response_model=dict)
async def birja_data(crs_code: Optional[str] = None):
    start = datetime(2024, 9, 1)
    finish = datetime(2024, 11, 30)
    if crs_code:
        url = f"http://10.190.4.38:4040/api/Construction/GetProductsByDate/1/5000/%20/{start.strftime('%Y-%m-%d')}/{finish.strftime('%Y-%m-%d')}/%20/%20"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Filtrlash
            filtered_data = [
                item for item in data if item.get("constructioncode") == crs_code
            ]
            return {"filtered_data": filtered_data}
        else:
            error_message = "Serverdan yaroqsiz javob qaytardi"
            raise HTTPException(status_code=response.status_code, detail={'error': error_message})
    else:
        error_message = "crs_code parametri kerak"
        raise HTTPException(status_code=400, detail={'error': error_message})
###############################   SOLIQ API   #############################################
@app_main_router.get("/soliq_data/", response_model=dict)
async def soliq_data(mxik_code: Optional[str] = None):
    if mxik_code:
        url1 = f"https://mspd-api.soliq.uz/minstroy/construction/get-factura-list-by-catalog-code?catalogCode={mxik_code}&fromDate=01.10.2024&toDate=29.11.2024"
        
        try:
            async with httpx.AsyncClient() as client:
                response1 = await client.get(url1)
        except httpx.ConnectError as e:
            raise HTTPException(status_code=502, detail={'error': "Connection to the external server failed", 'details': str(e)})
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail={'error': "Request to the external server failed", 'details': str(e)})

        if response1.status_code == 200:
            try:
                data1 = response1.json()
                if data1.get("success") and data1.get("data"):
                    data = data1["data"]
                    
                    # delivery_sum / product_count hisoblash
                    ratios = [d["delivery_sum"] / d["product_count"] for d in data if d["product_count"] > 0]

                    # max, min va o'rtacha qiymatlarni hisoblash
                    max_sum = max(ratios)
                    min_sum = min(ratios)
                    midle_sum = sum(ratios) / len(ratios) if ratios else 0

                    return {
                        "success": True,
                        "reason": "success",
                        "max_sum": max_sum,
                        "min_sum": min_sum,
                        "midle_sum": midle_sum,
                        "data": data
                    }
                else:
                    raise HTTPException(status_code=404, detail={'error': "No data found for the given mxik_code"})
            except ValueError:
                raise HTTPException(status_code=500, detail={'error': "Invalid JSON response from server"})
        else:
            error_message = "Server returned an invalid response"
            raise HTTPException(status_code=response1.status_code, detail={'error': error_message})
    else:
        error_message = "mxik_code parameter is required"
        raise HTTPException(status_code=400, detail={'error': error_message})

############################################  REGION  KOMPANIY #####
@app_main_router.get("/monitoring/region_by_filter_company/")
async def region_by_filter_company(db: Session = Depends(get_db)):
    # Querying to count unique company_stir in each region and order by company_count in descending order
    results = (
        db.query(
            Regions.region_name_uz,  # Viloyat nomi
            func.count(distinct(MaterialAds.company_stir)).label("company_count")  # Unique kompaniyalarni hisoblash
        )
        .join(MaterialAds, MaterialAds.material_region_id == Regions.id)  # Regions va MaterialAds o'rtasidagi join
        .group_by(Regions.region_name_uz)  # Guruhlash viloyatlar bo'yicha
        .order_by(func.count(distinct(MaterialAds.company_stir)).desc())  # Kamayish tartibida saralash
        .all()
    )

    # Resultni JSON shaklida qaytarish
    return [{"region": region_name, "company_count": company_count} for region_name, company_count in results]
########################   REGIONS AD   ###########################
@app_main_router.post("/monitoring/regions/", response_model=dict)
async def monitor_regions(
    regions_name: Optional[List[str]] = None,
    db: Session = Depends(get_db),
    page: int = 1,  # Sahifa raqami (default 1)
    limit: int = 24,  # Har sahifada ko'rsatiladigan elementlar soni (default 12)
):
    query = db.query(MaterialAds)
    if regions_name:
        query = query.join(MaterialAds.region).filter(
            Regions.region_name_uz.in_(regions_name)
        )
    total_count = query.count()
    results = query.offset((page - 1) * limit).limit(limit).all()
    return {
        "count": total_count,
        "page": page,
        "limit": limit,
        "data": [
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
            for material in results
        ]
    }









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
    limit: int = 50,
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


