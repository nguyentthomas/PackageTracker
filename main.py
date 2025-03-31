from fastapi import FastAPI, status, HTTPException
from database import Base, engine
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
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create the database
Base.metadata.create_all(engine)

@app.get("/")
async def root():
    return {"message": "Package Tracker"}

#PACKAGES
@app.get("/packages/")
def read_package_list():
    session = Session(bind=engine, expire_on_commit=False)
    package_list = session.query(models.Packages).all()
    session.close()
    return package_list

@app.get("/packages/{packageID}")
def read_package(packageID: int):
    session = Session(bind=engine, expire_on_commit=False)
    package = session.query(models.Packages).get(packageID)
    session.close()
    return f"Package object with PackageID: {package.packageID}"

@app.post("/packages", status_code=status.HTTP_201_CREATED)  # previous called test
def create_packages(packages: List[schemas.Packages]):
    try:
        session = Session(bind=engine, expire_on_commit=False)

        for package in packages:
            package_db = models.Packages(
                packageID=package.packageID,
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
        batchPackageID = [package_db.packageID for package_db in packages]
        session.close()

        return {"message": f"Created Package items with packageID {batchPackageID}"}

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error creating Package items: {str(e)}"
        )

@app.put("/packages/{packageID}")
def update_package(packageID: str, recipient: str, sender: str, trackingReference: str, deliveryType:str, item: str, shippingMethod: str, dateSent: str, status: str, note: str):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # Get Package from PackageID
    package = session.query(models.Packages).get(packageID)

    # Update each variable
    if package:
        package.packageID = packageID
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
            status_code=404, detail=f"Package item with PackageID '{packageID}' not found"
        )

    return package

@app.delete("/packages/{packageID}", status_code=status.HTTP_204_NO_CONTENT)
def delete_package(packageID: str):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # Get Package from PackageID
    package = session.query(models.Packages).get(packageID)

    # if Package with given PackageID exists, delete it from the database. Otherwise raise 404 error
    if package:
        session.delete(package)
        session.commit()
        session.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Package item with PackageID '{packageID}' not found"
        )

    return None