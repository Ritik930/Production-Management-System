from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional

class RollingParametersCreate(BaseModel):
    part_name: str
    machine_name: str

class RollingParametersUpdate(BaseModel):
    coolant_temperature: Optional[float] = None
    machining_angle: Optional[float] = None
    chuck_speed: Optional[float] = None

class RollingParametersResponse(BaseModel):
    part_name: str
    machine_name: str
    date_: date
    time_stamp: datetime
    shift: str
    coolant_temperature: float |None
    machining_angle:float | None
    chuck_speed: float | None
    is_completed: bool

    class Config:
        from_attributes = True

class ProductionStats(BaseModel):
    total_parts: int
    machine_wise: dict[str, int]

class ShiftInfo(BaseModel):
    shift : str
    current_time: str
