from datetime import datetime ,timezone,timedelta
from jose import jwt,JWTError
from app.core.security import setting

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_token(data : dict ,ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})

    return jwt.encode(
        to_encode ,
        setting.JWT_SECRET_KEY,
        algorithm=setting.JWT_ALGORITHM
    )


def verify_token (token : str):
    try:
        payload = jwt.decode(          
          token ,
          setting.JWT_SECRET_KEY ,
          algorithms=[setting.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
    
