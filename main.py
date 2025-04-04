from fastapi import FastAPI, status, HTTPException, Query, Depends, Body
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from typing import List, Union
import models, schemas
from uuid import UUID

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CorrelationIdMiddleware)

origins = [
    "https://localhost:5173",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Create the database
Base.metadata.create_all(engine)

@app.get("/")
async def root():
    return {"message": "Package Tracker"}

#PACKAGES
@app.get("/packages")
def read_package_list(
    page: int = Query(1, alias="page"), 
    per_page: int = Query(10, alias="perPage"), 
    filters: dict = Body({}, embed=True),
    db: Session = Depends(get_db)
):
    if filters:
        for key, value in filters.items():
            query = query.filter(getattr(models.Packages, key).ilike(f"%{value}%"))  # Case-insensitive search

    total = db.query(models.Packages).count()  # Get total count
    start = (page - 1) * per_page  # Offset calculation

    package_list = (
        db.query(models.Packages)
        .offset(start)
        .limit(per_page)
        .all()
    )

    return {
        "data": [package.__dict__ for package in package_list],
        "total": total
    }


@app.get("/packages/{id}")
def read_package(id: str):
    session = Session(bind=engine, expire_on_commit=False)
    package = session.query(models.Packages).get(id)
    session.close()
    return f"Package object with id: {package.id}"

@app.post("/packages", status_code=201)
def create_packages(package: schemas.Packages, db: Session = Depends(get_db)):  
    try:
        package_db = models.Packages(**package.dict())  
        db.add(package_db)
        db.commit()
        db.refresh(package_db)
        
        return {"data": {"id": package_db.id, **package.dict()}}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating Package item: {str(e)}")
    
@app.put("/packages/{id}")
def update_package(id: str, recipient: str, sender: str, trackingReference: str, deliveryType:str, item: str, shippingMethod: str, dateSent: str, status: str, note: str):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # Get Package from id
    package = session.query(models.Packages).get(id)

    # Update each variable
    if package:
        package.id = id
        package.recipient = recipient
        package.sender = sender
        package.trackingReference = trackingReference
        package.item = item
        package.dateSent = dateSent
        package.deliveryType = deliveryType
        package.shippingMethod = shippingMethod
        package.status = status
        package.note = note
        session.commit()

    # close the session
    session.close()

    if not package:
        raise HTTPException(
            status_code=404, detail=f"Package item with id '{id}' not found"
        )

    return package

@app.delete("/packages/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_packages(package: schemas.Packages, db: Session = Depends(get_db)):  
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # Get Package from id
    package = session.query(models.Packages).get(id)

    # if Package with given id exists, delete it from the database. Otherwise raise 404 error
    if package:
        session.delete(package)
        session.commit()
        session.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Package item with id '{id}' not found"
        )

    return None