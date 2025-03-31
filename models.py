from sqlalchemy import Column,String
from database import Base

class Packages(Base):
    __tablename__ = 'packages'
    id = Column(String, primary_key=True)
    recipient = Column(String)
    sender = Column(String)
    trackingReference = Column(String)
    deliveryType=Column(String)
    item = Column(String)
    shippingMethod = Column(String)
    dateSent = Column(String)
    status = Column(String)
    note = Column(String)
