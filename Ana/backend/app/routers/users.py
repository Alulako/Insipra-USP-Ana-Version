from fastapi import APIRouter, Depends
from ..deps import get_current_user
from ..schemas import UserOut
from ..models import User

router = APIRouter(tags=["users"])

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
