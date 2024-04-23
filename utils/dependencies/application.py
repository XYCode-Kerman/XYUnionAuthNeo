from typing import Tuple

import jwt
from fastapi import HTTPException

from configs import SECRET

from ..auth import hash_password
from ..database import db


async def require_application(app_id: str, app_secret: str, app_token: str) -> Tuple[str, str]:
    """返回元组，第一个参数为 app_id，第二个参数为 app_secret。"""

    result = await db.hget('xyuan_application_tokens', f'{app_id}_{hash_password(app_secret)}')

    if result is None:
        raise HTTPException(
            status_code=401, detail="错误的 Application ID 或 Application Secret")

    # 解码
    try:
        decoded = jwt.decode(app_token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的 Token")

    if decoded['app_id'] != app_id or decoded['app_secret'] != app_secret:
        raise HTTPException(status_code=401, detail="错误的 Token")

    return (app_id, app_secret)
