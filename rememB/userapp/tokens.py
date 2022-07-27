# 토큰 발급, 복호화하기 위한 함수 관리를 위한 페이지

import jwt
import datetime
from decouple import config

def generate_token(payload, type): # payload 값과 토큰의 종류
    if type == "access":
        # 2시간
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    elif type == "refresh":
        # 2주
        exp = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    else:
        raise Exception("Invalid tokenType")
    
    payload['exp'] = exp
    payload['iat'] = datetime.datetime.utcnow() # 발급 시간
    encoded = jwt.encode(payload, config("JWT_SECRET_KEY"), algorithm="HS256")

    return encoded