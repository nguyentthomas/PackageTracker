from pydantic import BaseModel

class Packages(BaseModel):
    id: str
    recipient: str
    sender: str
    trackingReference: str
    deliveryType:str
    item: str
    shippingMethod: str
    dateSent: str
    status: str
    note: str
