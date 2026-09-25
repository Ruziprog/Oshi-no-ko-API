import jwt

from fastapi import Depends, HTTPException
from sqlalchemy import select

from database import SessionLocal
from models import User
from security import SECRET_KEY, ALGORITHM, oauth2_scheme


async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    async with SessionLocal() as session:
        statement = select(User).where(
            User.username == username
        )

        result = await session.execute(statement)

        db_user = result.scalar_one_or_none()

        if db_user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return db_user