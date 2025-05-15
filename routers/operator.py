from datetime import datetime, timedelta, time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Schema
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..schemas import ShiftInfo
from ..utils import determine_shift

router = APIRouter(
    prefix="/operator",
    tags=["operator"]
)

# Get Current shift

@router.get("/Current_Shift", response_model=ShiftInfo)
def determine_shift():
    now = datetime.now().time()
    shift_a_start = time(7, 0)
    shift_b_start = time(19, 0)

    shift = "A" if shift_a_start <= now < shift_b_start else "B"
    return {
        "shift": shift,
        "current_time": now.strftime("%H:%M:%S")
    }

#Scan Part Name

@router.post("/scan_Part_Name/", response_model=schemas.RollingParametersResponse)
def scan_part(
        part_data: schemas.RollingParametersCreate,
        db: Session = Depends(get_db)
):
    existing_part = db.query(models.RollingParameters).filter(
        models.RollingParameters.part_name == part_data.part_name
    ).first()

    if existing_part:
        raise HTTPException(status_code=400, detail="Part already scanned")

    db_part = models.RollingParameters(
        part_name=part_data.part_name,
        machine_name=part_data.machine_name,
        shift=determine_shift(),
        is_completed=False
    )

    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

#Update temp,angle,speed

@router.post("/update/{part_name}", response_model=schemas.RollingParametersResponse)
def update_parameters(
        part_name: str,
        params: schemas.RollingParametersUpdate,db: Session = Depends(get_db)):
    db_part = db.query(models.RollingParameters).filter(
        models.RollingParameters.part_name == part_name
    ).first()

    if not db_part:
        raise HTTPException(status_code=404, detail="Part not found")

    if params.coolant_temperature is not None:
        db_part.coolant_temperature = params.coolant_temperature
    if params.machining_angle is not None:
        db_part.machining_angle = params.machining_angle
    if params.chuck_speed is not None:
        db_part.chuck_speed = params.chuck_speed

    db_part.is_completed = True
    db.commit()
    db.refresh(db_part)
    return db_part

# delete Part_Name

@router.delete("/delete/{part_name}")
def delete_part(part_name: str, db: Session = Depends(get_db)):
    db_part = db.query(models.RollingParameters).filter(
        models.RollingParameters.part_name == part_name
    ).first()

    if not db_part:
        raise HTTPException(status_code=404, detail="Part not found")

    db.delete(db_part)
    db.commit()
    return {"message": "Part deleted successfully"}