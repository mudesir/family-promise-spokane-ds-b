"""Machine learning functions"""
import random
import logging
from fastapi import APIRouter
from pydantic import BaseModel,Field,validator
import datetime

router = APIRouter()
class PersonInfo(BaseModel):
    '''Data model for Request Body 
       
    personal_id: Personal_id (int) Sample 14245
    Data Subject to change once a working model is done'''
    # Features
    # features = [ 'CaseMembers','Race, 'Ethnicity', 'Current Age', 
    #              'Gender', 'Length of Stay', 'Enrollment Length',
    #              'Household Type', 'Barrier Count at Entry']  
    personal_id: int = Field(...,example=421344)
    case_members: int = Field(...,example=6)
    race: str = Field(...,example='White')
    ethnicity: str = Field(...,example='Native American')
    current_age: int = Field(...,example=20)
    gender: str = Field(...,example='Male')
    length_stay: int = Field(...,example=10)
    enrollment_length: int = Field(...,example=20)
    household_type: str = Field(...,example='householde without children')
    barrier_county_entry: int = Field(...,example=4)
    
    @validator('personal_id')
    def variable_validation(cls,value):
        '''Validate variables'''
        assert value > 0, f'personal_id == {value} must be > 0'
        return value

@router.post('/predict')
async def predict(person_id: PersonInfo):
    '''# Data model PlaceHolder 
       # Usage: 
         - personal id (integer) Exmple : 232314
         - case_members: (integer) Example: 5
         - race: (string) Examples: white,asian,etc
         - ethnicity: (string) Example: Native Amrican, Latin, etc. 
         - current_age: (integer) Example: 20
         - gender: (string) Examples: Male, Female, non-binary,etc.
         - length_stay: (integer) Example: 10 (Length of stay in Days in previous housing situation)
         - enrollment_length: (integer) Example: 15 (Length of stay in shelter)
         - household_type: (string) Example: household without children, etc. 
         - barrier_count_entry: (integer) Example: 3 (barrier count at entry)
         - Request body Subject to change once a working model is in place
         - Post Method'''
    predicted,features = prediction()
    return { 
        'personal_id': person_id.personal_id,
        'exit_strategy': predicted,
        'top_features': features
    }
def prediction():
    # Clllassified Label
    # top three features
    label = random.choice(['Unknown/Other', 'Permanent Exit','Emergency Shelter','Temporary Exit',
                          'Transitional Housing'])
    features = ['personal_id', 'case_members','race', 'ethnicity',
                'current_age','gender','length_stay','enrollment_length','household_type',
                'barrier_county_entry', 'top_features']
    top_features = random.sample(features,3)
    return label,top_features