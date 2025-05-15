from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/manager",
    tags=["manager"]
)

#Daily Production

@router.get("/daily-production/", response_model=schemas.ProductionStats)
def get_daily_production(date_: date = date.today(),db: Session = Depends(get_db)):
    total_parts = db.query(models.RollingParameters).filter(models.RollingParameters.date_ == date_).count()

    machine_counts = db.query(models.RollingParameters.machine_name,func.count(models.RollingParameters.id)
    ).filter(models.RollingParameters.date_ == date_).group_by(models.RollingParameters.machine_name).all()

    return {
        "total_parts": total_parts,
        "machine_wise": dict(machine_counts)
    }

#Weekly Production

@router.get("/weekly_production/", response_model=schemas.ProductionStats)
def get_weekly_production(
        year: int,
        month: int,
        week: int,
        db: Session = Depends(get_db)
):

    start_date = date.fromisocalendar(year, week, 1)

    end_date = date.fromisocalendar(year, week, 7)

    total_parts = (db.query(models.RollingParameters).filter(models.RollingParameters.date_ >= start_date,models.RollingParameters.date_ <= end_date
        ).count()
    )

    machine_counts = (
        db.query(models.RollingParameters.machine_name, func.count(models.RollingParameters.id))
        .filter(models.RollingParameters.date_ >= start_date,models.RollingParameters.date_ <= end_date)
        .group_by(models.RollingParameters.machine_name).all()
    )

    machine_wise_counts = {
        machine: count
        for machine, count in machine_counts
    }
    return {
        "total_parts": total_parts,
        "machine_wise": machine_wise_counts
    }

#monthly Production

@router.get("/monthly-production/", response_model=schemas.ProductionStats)
def get_monthly_production(
        year: int,
        month: int,
        db: Session = Depends(get_db)
):
    total_parts = db.query(models.RollingParameters).filter(
        func.extract('year', models.RollingParameters.date_) == year,
        func.extract('month', models.RollingParameters.date_) == month
    ).count()

    machine_counts = db.query(
        models.RollingParameters.machine_name,
        func.count(models.RollingParameters.id)
    ).filter(
        func.extract('year', models.RollingParameters.date_) == year,
        func.extract('month', models.RollingParameters.date_) == month
    ).group_by(
        models.RollingParameters.machine_name
    ).all()

    return {
        "total_parts": total_parts,
        "machine_wise": dict(machine_counts)
    }

#Get Data Machine Wise

@router.get("/Machine_Wise/{machine_name}")
def get_machineWise_Production(machine_name: str, db: Session = Depends(get_db)):
    total_parts = (db.query(models.RollingParameters).filter(models.RollingParameters.machine_name == machine_name).count())

    return{
        "total_parts" : total_parts
    }

#Get all DATA

@router.get("/all")
async def get_all_production_data(skip: int = 0,limit: int = 100,db: Session = Depends(get_db)):

    total_count = db.query(models.RollingParameters).count()

    data = db.query(models.RollingParameters) \
        .order_by(models.RollingParameters.time_stamp.desc()) \
        .offset(skip) \
        .limit(limit) \
        .all()

    return {
        "data": data,
        "count": total_count
    }