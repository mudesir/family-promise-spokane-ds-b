"""Data visualization functions
   Not used on this cohort. Left file for future use"""

from fastapi import APIRouter

router = APIRouter()

@router.get('/visualization')
async def visualization():
   return "to do"