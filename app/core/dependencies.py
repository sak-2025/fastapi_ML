from fastapi import Header ,HTTPException
from app.core.config import setting
from app.core.security import verify_token



def verify_api_key(ap_key: str = Header(...)):
    if api_key != setting.API_KEY:
        raise HTTPException(status_code = 403 ,detail = "Invalid API Key")


def get_current_user(token:str = Header(...)):
    payload = verify_token
    if not payload:
        raise HTTPException(status_code=401 ,detail = " ")
    return payload