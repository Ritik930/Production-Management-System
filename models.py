from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, Date, func
from .database import Base

class RollingParameters(Base):
    __tablename__ = "rolling_parameters"

    id = Column(Integer, primary_key=True, index=True)
    part_name = Column(String, unique=True, nullable=False)
    machine_name = Column(String, nullable=False)
    date_ = Column(Date, nullable=False, default=func.current_date())
    time_stamp = Column(DateTime, nullable=False, default=func.now())
    shift = Column(String, nullable=True)
    coolant_temperature = Column(Float, nullable=True)
    machining_angle = Column(Float, nullable=True)
    chuck_speed = Column(Float, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)