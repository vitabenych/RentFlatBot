# routes.py
from typing import Optional, List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Flat(BaseModel):
    id: int
    district: str
    rooms: str
    price: int
    description: str
    url: str

@router.get("/flats/", response_model=List[Flat])
async def get_flats(
    district: Optional[str] = None,
    complex: Optional[str] = None,
    rooms: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
):
    # Тут логіка вибору квартир із бази чи кешу
    flats = [
        Flat(
            id=1,
            district=district or "Сихівський",
            rooms=rooms or "2",
            price=12000,
            description="Сучасна квартира в центрі Львова",
            url="https://t.me/example_flat1"
        )
    ]
    return flats
