from pydantic import BaseModel

class Packages(BaseModel):
    packageID: str
    recipient: str
    sender: str
    trackingReference: str
    item: str
    shippingMethod: str
    dateSent: str
    status: str
    note: str
