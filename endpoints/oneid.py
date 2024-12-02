from fastapi import FastAPI, Request, APIRouter, HTTPException
import requests

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

@app_oneid.get("/auth/callback")
def callback(code: str):
    token_url = "https://sso.egov.uz/sso/oauth/Authorization.do"
    token_data = {
        "grant_type": "one_authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(token_url, data=token_data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Token olishda xatolik yuz berdi")
    
    token_response = response.json()
    access_token = token_response.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Access token mavjud emas")

    # Foydalanuvchi ma'lumotlarini olish
    token_url = "https://sso.egov.uz/sso/oauth/Authorization.do"
    token_data = {
        "grant_type": "one_access_token_identify",  # Parametrni to'g'ri belgilash
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "access_token": access_token,  # Bu token sizga serverdan beriladi
        "scope": "myportal"  # Scope nomini to'g'ri kiriting
    }
    response = requests.post(token_url, data=token_data)
    
    # Agar javob muvaffaqiyatsiz bo'lsa, xato qaytarish
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Token olishda xatolik yuz berdi")

    # Foydalanuvchi ma'lumotlarini qaytarish
    return response.json()

