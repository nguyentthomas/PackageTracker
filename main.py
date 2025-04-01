from fastapi import FastAPI, status, HTTPException, Query, Depends
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from typing import List
import schemas
import models

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
    db: Session = Depends(get_db)
):
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

@app.post("/packages", status_code=status.HTTP_201_CREATED)  # previous called test
def create_packages(packages: List[schemas.Packages]):
    try:
        session = Session(bind=engine, expire_on_commit=False)

        for package in packages:
            package_db = models.Packages(
                id=package.id,
                recipient =package.recipient,
                sender=package.sender,
                trackingReference=package.trackingReference,
                shippingMethod=package.shippingMethod,
                deliveryType=package.deliveryType,
                item=package.item,
                status=package.status,
                dateSent=package.dateSent,
                note=package.note
            )
            session.add(package_db)

        session.commit()
        batchid = [package_db.id for package_db in packages]
        session.close()

        return {"message": f"Created Package items with id {batchid}"}

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error creating Package items: {str(e)}"
        )

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
def delete_package(id: str):
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