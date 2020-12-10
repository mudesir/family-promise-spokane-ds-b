"""Machine learning functions"""
import random
import logging
from fastapi import APIRouter
from pydantic import BaseModel,Field,validator

router = APIRouter()
class PersonInfo(BaseModel):
    '''Data model for Request Body 
       
    personal_id: Personal_id (int) Sample 14245
    Data Subject to change once a working model is done'''
    personal_id: int = Field(...,example=421344)
    @validator('personal_id')
    def variable_validation(cls,value):
        '''Validate variables'''
        assert value > 0, f'x1 == {value} must be > 0'
        return value

@router.post('/predict')
async def predict(person_id: PersonInfo):
    '''# Data model PlaceHolder 
       # Usage: 
         - personal id (integer) Exmple : 232314
         - Request body Subject to change once a working model is in place
         - Post Method'''
    return { 
        'exit_strategy': prediction()
    }
def prediction():
    return random.choice(['Unknown/Other', 'Permanent Exit','Emergency Shelter','Temporary Exit',
                          'Transitional Housing'])
            