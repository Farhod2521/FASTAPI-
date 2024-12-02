from fastapi import FastAPI, Request, APIRouter, HTTPException
import requests

app_oneid = APIRouter(tags=["Auth2"])
CLIENT_ID = "catalog_tmsiti_uz"
CLIENT_SECRET = "dJQZdRY8SiN0luwd5if9hiTb"
REDIRECT_URI = "https://mkinfo.uz/auth/login"

@app_oneid.get("/auth/login")
def login():
    auth_url = (
        f"https://sso.egov.uz/sso/oauth/Authorization.do?"
        f"response_type=one_code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
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
    user_info_url = "https://sso.egov.uz/sso/oauth/resource"  # To'g'ri URL'ni tekshiring
    user_info_response = requests.get(
        user_info_url,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if user_info_response.status_code != 200:
        raise HTTPException(
            status_code=user_info_response.status_code,
            detail="Foydalanuvchi ma'lumotlarini olishda xatolik"
        )
    return user_info_response.json()