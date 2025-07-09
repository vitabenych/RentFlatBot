from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.actions import parse_and_save_listing

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello from RentFlatBot"}

class ListingText(BaseModel):
    text: str

@router.post("/parse_listing/")
async def parse_listing_endpoint(listing: ListingText):
    response = await parse_and_save_listing(listing.text)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response
