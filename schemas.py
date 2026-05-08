from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

 

class Token(BaseModel):
    access_token: str
    token_type: str
    message: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    email: EmailStr
    otp: str
    new_password: str



# class CompanyProfileCreate(BaseModel):
#     user_id: UUID
#     company_profile: str
#     countries: list
#     company_intentions: list
#     industries: list



# class CompanyProfileCreate(BaseModel):
#     user_id: UUID
#     company_profile: str

#     countries:list
#     company_intentions:list
#     industries:list

#     business_type:list
#     business_stage:list
#     business_turnover:list
#     business_timeline:list
#     business_clients:list
#     business_deal_size:list
#     business_product_adaptation:list
#     business_international_experience:list
#     business_international_enquiries:list
#     business_budget:list
#     business_growth_export_team:list
#     business_preferences:list
#     business_risk_appetite:list
#     business_local_partners:list
#     business_type_of_support:list

class CompanyProfileCreate(BaseModel):
    user_id: UUID
    company_profile: str

    countries:list
    company_intentions:list
    industries:list

    business_type:list
    business_stage:list
    business_turnover:list
    business_timeline:list
    business_clients:list
    business_deal_size:list
    business_intentions:list
    business_product_adaptation:list
    business_international_experience:list
    business_international_enquiries:list
    business_budget:list
    business_growth_export_team:list
    business_preferences:list
    business_risk_appetite:list
    business_local_partners:list
    business_type_of_support:list
    
    
class UserIdRequest(BaseModel):
    user_id: UUID