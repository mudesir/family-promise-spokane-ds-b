"""Machine learning functions"""
import random
import logging
from fastapi import APIRouter
from pydantic import BaseModel,Field,validator
import datetime
from joblib import load
import pandas as pd

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
    length_stay: str = Field(...,example='two to six weeks')
    enrollment_length: int = Field(...,example=20)
    household_type: str = Field(...,example='household without children')
    barrier_count_entry: int = Field(...,example=4)
    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])
    
    @validator('personal_id')
    def variable_validation(cls,value):
        '''Validate variables'''
        assert value > 0, f'personal_id == {value} must be > 0'
        return value

@router.post('/predict')
async def predict(guest_info: PersonInfo):
    '''# Data model PlaceHolder 
       # Usage: 
         - personal id (integer) Exmple : 232314
         - case_members: (integer) Example: 5
         - race: (string) Examples: white,asian,etc
         - ethnicity: (string) Example: Native Amrican, Latin, etc. 
         - current_age: (integer) Example: 20
         - gender: (string) Examples: Male, Female, non-binary,etc.
         - length_stay: (string) Example: Two to 5 days (Length of stay in Days in previous housing situation)
         - enrollment_length: (integer) Example: 15 (Length of stay in shelter)
         - household_type: (string) Example: household without children, etc. 
         - barrier_count_entry: (integer) Example: 3 (barrier count at entry)
         - Request body Subject to change once a working model is in place
         - Post Method'''
        
    #Prediction Pipe 
    random_forest_pipe = load('app/assets/randomforest_modelv3.pkl') #loads pickled model (using loblib)
    df = guest_info.to_df()
    X = df.drop('personal_id',axis=1)
    X.rename(columns={'case_members':'CaseMembers', 'race':'Race', 'ethnicity':'Ethnicity', 
                      'current_age':'Current Age', 'gender':'Gender','length_stay':'Length of Stay',
                      'enrollment_length':'Days Enrolled in Project', 'household_type':'Household Type',
                      'barrier_count_entry':'Barrier Count at Entry'},inplace=True)

    y_pred = random_forest_pipe.predict(X)
    
    #feature Importances
    model = random_forest_pipe.named_steps['classifier']
    encoder = random_forest_pipe.named_steps['ord']
    encoded_columns = encoder.transform(X).columns
    importances = pd.Series(model.feature_importances_,encoded_columns)
    top_feats = importances.sort_values(ascending=False)[:3]
    feats = {}
    for k,v in top_feats.items():
        feats[k] = v


    predicted,features = prediction()
    return { 
        'personal_id': guest_info.personal_id,
        'exit_strategy': y_pred[0],
        'top_features': feats
    }