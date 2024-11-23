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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Andijon")
        .count()
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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Buxoro")
        .count()
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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Fargona")
        .count()
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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Jizzax")
        .count()
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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Xorazm")
        .count()
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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Namangan")
        .count()
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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Navoiy")
        .count()
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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Qashqadaryo")
        .count()
    )
    qoraqalpogiston_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Qoraqalpogʻiston Respublikasi")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Qoraqalpogʻiston Respublikasi")
        .count()
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Qoraqalpogʻiston Respublikasi")
        .count()
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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Samarqand")
        .count()
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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Sirdaryo")
        .count()
    )
    surxandaryo_total = (
        db.query(MaterialAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Surxandaryo")
        .count()
        +
        db.query(TechnoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Surxandaryo")
        .count()
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Surxandaryo")
        .count()
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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Toshkent")
        .count()
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
        +
        db.query(MMechanoAds)
        .join(Regions)
        .filter(Regions.region_name_uz == "Toshkent shahri")
        .count()
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
        "Toshkent shahri (Jami)": toshkent_shahri_total,
    }
    return result


