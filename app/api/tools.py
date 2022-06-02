from enum import Enum

from fastapi import HTTPException

from app.models.tools import Message


def raise_400(err: Enum) -> None:
    message = Message(err=str(err), message=str(err.value)).dict()
    raise HTTPException(status_code=400, detail=message)
