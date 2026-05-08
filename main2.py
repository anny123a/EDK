# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# from auth import generate_otp, send_email
# import models, schemas
# from database import engine, SessionLocal
# from auth import hash_password, verify_password, create_access_token
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import HTTPException
# from fastapi import Request
# from uuid import UUID, uuid4
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError
# from auth import SECRET_KEY, ALGORITHM
# from fastapi.exceptions import RequestValidationError
 
# models.Base.metadata.create_all(bind=engine)
 
# app = FastAPI(root_path="/api")
 
# # OAuth2 scheme
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
 
# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
 
 
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     user = db.query(models.User).filter(models.User.email == email).first()
#     if user is None:
#         raise HTTPException(status_code=401, detail="User not found")
#     return user
 
 
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     error = exc.errors()[0]
#     field = error["loc"][-1]
#     msg = error["msg"]
 
#     return JSONResponse(
#         status_code=422,
#         content={
#             "success": False,
#             "message": f"{field}: {msg}"
#         },
#     )
 
    
# @app.post("/signup")
# def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     existing_user = db.query(models.User).filter(
#         models.User.email == user.email
#     ).first()
 
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already exists")
 
#     new_user = models.User(
#         email=user.email,
#         password=hash_password(user.password)
#     )
 
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
 
#     token = create_access_token({"sub": new_user.email})
 
#     return {
#         "success": True,
#         "message": "User created successfully",
#         "data": {
#             "user_id": str(new_user.id),
#             "access_token": token,
#             "token_type": "bearer"
#         }
#     }   
 
    
# @app.post("/login")
# def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(
#         models.User.email == user.email
#     ).first()
 
#     if not db_user:
#         raise HTTPException(status_code=401, detail="User not found")
 
#     if not verify_password(user.password, db_user.password):
#         raise HTTPException(status_code=401, detail="Wrong password")
 
#     token = create_access_token({"sub": db_user.email})
 
#     return {
#         "success": True,
#         "message": "Login successful",
#         "data": {
#             "user_id": str(db_user.id),
#             "access_token": token,
#             "token_type": "bearer"
#         }
#     }
    
 
# @app.post("/forgot-password")
# def forgot_password(data: schemas.ForgotPassword, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == data.email).first()
 
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
 
#     otp = generate_otp()
#     user.otp = otp
#     user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
 
#     db.commit()
#     send_email(user.email, otp)
 
#     return {"message": "OTP sent to your email"}
 
 
# @app.post("/reset-password")
# def reset_password(data: schemas.ResetPassword, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == data.email).first()
 
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
 
#     # Check OTP
#     if user.otp != data.otp:
#         raise HTTPException(status_code=400, detail="Invalid OTP")
 
#     # Check expiry
#     if not user.otp_expiry or datetime.utcnow() > user.otp_expiry:
#         raise HTTPException(status_code=400, detail="OTP expired")
 
#     # Update password
#     user.password = hash_password(data.new_password)
 
#     # Clear OTP
#     user.otp = None
#     user.otp_expiry = None
 
#     db.commit()
 
#     return {"message": "Password reset successful"}
 
 
# # ✅ FIXED ENDPOINT - Works with both MySQL and PostgreSQL
# @app.post("/user-interests")
# def create_company_profile(
#     data: schemas.CompanyProfileCreate,
#     db: Session = Depends(get_db)
# ):
#     """
#     Create or update user company profile.
#     - If profile exists for user: UPDATE it
#     - If not: CREATE a new one
#     Works with both MySQL and PostgreSQL.
#     """
#     try:
#         print("data --->>", data)
 
#         profile_data = {
#             "company_profile": data.company_profile,
#             "countries": data.countries,
#             "company_intentions": data.company_intentions,
#             "industries": data.industries
#         }
 
#         existing_entry = db.query(models.CompanyProfile).filter(
#             models.CompanyProfile.user_id == data.user_id
#         ).first()
 
#         if existing_entry:
#             print(f"Updating profile for user {data.user_id}")
#             existing_entry.data = profile_data
#             flag_modified(existing_entry, "data")  # ✅ forces SQLAlchemy to detect JSON change
#             db.commit()
#             db.refresh(existing_entry)
 
#             return {
#                 "success": True,
#                 "message": "Data updated successfully",
#                 "data": {
#                     "id": str(existing_entry.id),
#                     "user_id": str(existing_entry.user_id),
#                     "data": existing_entry.data
#                 }
#             }
 
#         else:
#             print(f"Creating new profile for user {data.user_id}")
#             new_entry = models.CompanyProfile(
#                 id=uuid4(),
#                 user_id=data.user_id,
#                 data=profile_data
#             )
#             db.add(new_entry)
#             db.commit()
#             db.refresh(new_entry)
 
#             return {
#                 "success": True,
#                 "message": "Data saved successfully",
#                 "data": {
#                     "id": str(new_entry.id),
#                     "user_id": str(new_entry.user_id),
#                     "data": new_entry.data
#                 }
#             }
 
#     except Exception as e:
#         db.rollback()
#         print("ERROR:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))
 
    
# @app.get("/get-user-interests/{user_id}")
# def get_user_interests(user_id: UUID, db: Session = Depends(get_db)):
#     try:
#         user = db.query(models.User).filter(models.User.id == user_id).first()
 
#         default_profile = {
#             "company_profile": "",
#             "countries": [],
#             "company_intentions": [],
#             "industries": []
#         }
 
#         if not user:
#             return {
#                 "success": True,
#                 "message": "User not found",
#                 "data": {
#                     "user_id": str(user_id),
#                     "email": None,
#                     "profile": default_profile
#                 }
#             }
 
#         profile = db.query(models.CompanyProfile).filter(
#             models.CompanyProfile.user_id == user_id
#         ).first()
 
#         return {
#             "success": True,
#             "message": "Data not found" if not profile else "Data fetched successfully",
#             "data": {
#                 "user_id": str(user.id),
#                 "email": user.email,
#                 "profile": profile.data if profile else default_profile
#             }
#         }
 
#     except Exception as e:
#         return {
#             "success": False,
#             "message": str(e)
#         }
 
 
# @app.get("/get-user-id")
# def get_current_user_info(current_user: models.User = Depends(get_current_user)):
#     return {
#         "success": True,
#         "message": "User information retrieved successfully",
#         "data": {
#             "user_id": str(current_user.id),
#             "email": current_user.email
#         }
#     }







from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from auth import generate_otp, send_email
import models, schemas
from database import engine, SessionLocal
from auth import hash_password, verify_password, create_access_token
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import Request
from uuid import UUID, uuid4
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from auth import SECRET_KEY, ALGORITHM
from fastapi.exceptions import RequestValidationError

models.Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/api")

# OAuth2 schemegggggggggggggggggggg
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    field = error["loc"][-1]
    msg = error["msg"]

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": f"{field}: {msg}"
        },
    )

    
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email})

    return {
        "success": True,
        "message": "User created successfully",
        "data": {
            "user_id": str(new_user.id),
            "access_token": token,
            "token_type": "bearer"
        }
    }   

    
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_access_token({"sub": db_user.email})

    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "user_id": str(db_user.id),
            "access_token": token,
            "token_type": "bearer"
        }
    }
    

@app.post("/forgot-password")
def forgot_password(data: schemas.ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()
    user.otp = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)

    db.commit()
    send_email(user.email, otp)

    return {"message": "OTP sent to your email"}


@app.post("/reset-password")
def reset_password(data: schemas.ResetPassword, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check OTP
    if user.otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Check expiry
    if not user.otp_expiry or datetime.utcnow() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="OTP expired")

    # Update password
    user.password = hash_password(data.new_password)

    # Clear OTP
    user.otp = None
    user.otp_expiry = None

    db.commit()

    return {"message": "Password reset successful"}


# ✅ FIXED ENDPOINT - Works with both MySQL and PostgreSQL
@app.post("/user-interests")
def create_company_profile(
    data: schemas.CompanyProfileCreate,
    db: Session = Depends(get_db)
):
    """
    Create or update user company profile.
    
    This endpoint checkeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeees if a profile already exists for the user.
    - If exists: UPDATE the existing profile
    - If not: CREATE a new profile
    
    Works with MySQL, PostgreSQL, and SQLite.
    """
    try:
        print("data --->>", data)

        profile_data = {
            "company_profile": data.company_profile,
            "countries": data.countries,
            "company_intentions": data.company_intentions,
            "industries": data.industries
        }
        

        # ✅ Check if profile already exists for this user
        existing_entry = db.query(models.CompanyProfile).filter(
            models.CompanyProfile.user_id == str(data.user_id)
        ).first()

        if existing_entry:
            # ✅ UPDATE existing profile
            print(f"Updating profile for user {data.user_id}")
            existing_entry.data = profile_data
            db.commit()
            db.refresh(existing_entry)

            return {
                "success": True,
                "message": "Data updated successfully",
                "data": {
                    "id": str(existing_entry.id),
                    "user_id": str(existing_entry.user_id),
                    "data": existing_entry.data
                }
            }

        else:
            # ✅ CREATE new profile
            print(f"Creating new profile for user {data.user_id}")
            new_entry = models.CompanyProfile(
                id=uuid4(),  # Generate UUID only on creation
                user_id=data.user_id,
                data=profile_data
            )
            db.add(new_entry)
            db.commit()
            db.refresh(new_entry)

            return {
                "success": True,
                "message": "Data saved successfully",
                "data": {
                    "id": str(new_entry.id),
                    "user_id": str(new_entry.user_id),
                    "data": new_entry.data
                }
            }

    except Exception as e:
        db.rollback()
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

    #ggggggggg2
@app.get("/get-user-interests/{user_id}")
def get_user_interests(user_id: str, db: Session = Depends(get_db)):
    try:
        try:
            user_uuid = str(UUID(user_id))  # ✅ validate AND convert to string immediately
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user_id format.")

        default_profile = {
            "company_profile": "",
            "countries": [],
            "company_intentions": [],
            "industries": [],

            "business_type": [],
            "business_stage": [],
            "business_turnover": [],
            "business_timeline": [],
            "business_clients": [],
            "business_deal_size": [],
            "business_product_adaptation": [],
            "business_international_experience": [],
            "business_international_enquiries": [],
            "business_budget": [],
            "business_growth_export_team": [],
            "business_preferences": [],
            "business_risk_appetite": [],
            "business_local_partners": [],
            "business_type_of_support": [],
  }

        # ✅ user_uuid is already a str now
        user = db.query(models.User).filter(models.User.id == user_uuid).first()

        if not user:
            return {
                "success": True,
                "message": "User not found",
                "data": {
                    "user_id": user_id,
                    "email": None,
                    "profile": default_profile
                }
            }

        profile = db.query(models.CompanyProfile).filter(
            models.CompanyProfile.user_id == user_uuid  # ✅ also a str
        ).first()

        return {
            "success": True,
            "message": "Data not found" if not profile else "Data fetched successfully",
            "data": {
                "user_id": str(user.id),
                "email": user.email,
                "profile": profile.data if profile else default_profile
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.get("/get-user-id")
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    return {
        "success": True,
        "message": "User information retrieved successfully",
        "data": {
            "user_id": str(current_user.id),
            "email": current_user.email
        }
    }