from app.database import db
from fastapi import APIRouter, status, Depends, HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from app.operation import role
from typing import List

router = APIRouter(prefix='/role',tags=["Roles"])

get_db = db.get_db
module_name = 'Roles'

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.Getroles)
async def create_role( name: str, active: bool, db: Session = Depends(get_db)):
    return role.create_role(name, active, db)

@router.get('/get_all', status_code=status.HTTP_200_OK, response_model=List[schemas.Getroles])
async def create_role(db: Session = Depends(get_db)):
    return role.get_role(db)

@router.delete('/delete/{role_id}', status_code=status.HTTP_200_OK)    
async def delete_role(role_id: int,db: Session = Depends(get_db)):
    return role.delete_role(role_id,db) 

@router.get('/get_role_permission/{role_id}',response_model= List[schemas.Getrole_permission], status_code=status.HTTP_200_OK) 
async def get_role_permission(role_id: int, db: Session = Depends(get_db)):  
    return role.get_role_permission(role_id,db)