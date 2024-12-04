from fastapi import FastAPI, Request, APIRouter, HTTPException, Response, Depends
import requests
import datetime
import jwt
from sqlalchemy.orm import Session # Django ORM yoki boshqa ORMga mos ravishda sozlang
from models import OneID
from database import get_db


app_oneid = APIRouter(tags=["Auth2"])
CLIENT_ID = "catalog_tmsiti_uz"
CLIENT_SECRET = "dJQZdRY8SiN0luwd5if9hiTb"
REDIRECT_URI = "https://mkinfo.uz/"

@app_oneid.get("/auth/login")
def login():
    auth_url = (
        f"https://sso.egov.uz/sso/oauth/Authorization.do?"
        f"response_type=one_code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={CLIENT_ID}&state=OneID"
    )
    return {"auth_url": auth_url}

@app_oneid.get("/auth/callback/")
def callback(code: str, db: Session = Depends(get_db)): # `db` - ma'lumotlar bazasini ulash uchun parametr
    token_url = "https://sso.egov.uz/sso/oauth/Authorization.do"
    token_data = {
        "grant_type": "one_authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    # 1. Birlamchi tokenni olish
    response = requests.post(token_url, data=token_data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Token olishda xatolik yuz berdi")
    
    token_response = response.json()
    access_token = token_response.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Access token mavjud emas")

    # 2. Foydalanuvchi ma'lumotlarini olish
    user_info_url = "https://sso.egov.uz/sso/oauth/Authorization.do"
    user_info_data = {
        "grant_type": "one_access_token_identify",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "access_token": access_token,
        "scope": "myportal"
    }
    user_response = requests.post(user_info_url, data=user_info_data)
    
    if user_response.status_code != 200:
        raise HTTPException(status_code=user_response.status_code, detail="Foydalanuvchi ma'lumotlarini olishda xatolik yuz berdi")
    
    user_data = user_response.json()

    # 3. Foydalanuvchi bazada bor-yo'qligini tekshirish (PIN orqali)
    pin = user_data.get("pin")
    full_name = user_data.get("full_name")
    birth_date = user_data.get("birth_date")
    user_id = user_data.get("user_id")
    birth_place = user_data.get("birth_place")
    passport_no = user_data.get("pport_no")

    user = db.query(OneID).filter(OneID.pin == pin).first()

    if not user:
        # Agar foydalanuvchi bazada yo'q bo'lsa, uni saqlaymiz
        new_user = OneID(
            pin=pin,
            full_name=full_name,
            birth_date=birth_date,
            user_id=user_id,
            birth_place=birth_place,
            passport_no=passport_no
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user  # Yangidan olingan foydalanuvchi obyektini ishlatamiz

    # 4. JWT token yaratish
    payload = {
        'id': user.id,
        'full_name': user.full_name,
        'pin': user.pin,
        'role': "customer",
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, minutes=60),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')

    # 5. Javobni qaytarish
    response = Response()
    response_data= response.data = {
        'token': token,
        'id': user.id,
        'full_name': user.full_name,
        'pin': user.pin,
        'role': "customer",
    }
    print(response.data)

    return response_data
