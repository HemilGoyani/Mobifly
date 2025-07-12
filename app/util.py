from os import access
from sqlite3 import dbapi2
from fastapi import HTTPException, status
from fastapi import status, HTTPException
from app.models import Usersignup, Modules, Permission, AccessName
from app import models
import jwt
from app.authentication import SECRET_KEY, SECURITY_ALGORITHM
from fastapi.responses import JSONResponse
from app.utils.redis_client import redis_client
import redis.asyncio as redis
from functools import wraps
from app.utils.logging_config import logger

import json

# common fuction permission access or not
def module_permission(request, db, module_name):
    token = request.headers.get("Authorization")
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
            user = (
                db.query(Usersignup)
                .filter(Usersignup.email == payload.get("email"))
                .first()
            )

            data = get_permission(user.id, db)
            for i in data:
                if i.get("module_name") == module_name:
                    return i.get("access_type")

        except:
            return JSONResponse(
                content={"detail": "INVALID TOKEN"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    elif not token:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing"
        )


def get_permission(user_id, db):
    get_user = db.query(Usersignup).filter(Usersignup.id == user_id).first()

    if not get_user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"user id {user_id} not found"
        )
    role_id = [role.id for role in get_user.roles]
    record = []

    module_list = db.query(Modules).all()

    for module in module_list:
        get_permission = (
            db.query(Permission)
            .filter(Permission.role_id.in_(role_id), Permission.module_id == module.id)
            .all()
        )
        dic = {"module_name": module.name, "access_type": models.AccessName.NONE}
        for data in get_permission:
            if data.access_type.value == AccessName.READ_WRITE.value:
                dic.update({"access_type": data.access_type})
                break
            elif data.access_type.value == AccessName.READ.value:
                dic.update({"access_type": data.access_type})
        record.append(dic)
    return record


def commit_data(table, db):
    db.add(table)
    db.commit()
    db.refresh(table)


def delete_data(table, db):
    table.delete(synchronize_session=False)
    db.commit()


def get_data(model, id, db):
    get_data = db.query(model).filter(model.id == id)
    return get_data


def check_role(role_id, Role, db):
    for role in role_id:
        check_role_id = db.query(Role).filter(Role.id == role).first()
        if not check_role_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"role id {role} is not exist",
            )


def has_permission(request, db, module_name, access_type):
    data = module_permission(request, db, module_name)
    for access_name in access_type:
        if data == access_name:
            return True
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="user has not permission")


def check_data(model, name, db):
    return db.query(model).filter(model.name == name).first()


def cache(key: str, expire: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                cached = await redis_client.get(key)
                if cached:
                    logger.info(f"Cache hit for key: {key}")
                    return json.loads(cached)

                result = func(*args, **kwargs)

                # Serialize only JSON-serializable data
                await redis_client.set(key, json.dumps(result), ex=expire)
                logger.info(f"Cache set for key: {key}")
                return result
            except Exception as e:
                logger.error(f"Redis cache error on {key}: {e}")
                return func(*args, **kwargs)

        return wrapper
    return decorator