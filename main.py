from fastapi import FastAPI
from .routers import operator, manager
from .models import Base
from .database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Production Management System " )

app.include_router(operator.router)
app.include_router(manager.router)

