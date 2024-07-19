from fastapi import FastAPI,Depends,HTTPException
from pydantic import UUID3, BaseModel
from typing import Optional,List,Annotated
from uuid import uuid4
import models
from database import engine,sessionLocal
from sqlalchemy.orm import Session
# app
app=FastAPI()
models.Base.metadata.create_all(bind=engine)
# class
class Task(BaseModel):
    id:Optional[str]=None
    title:str
    description:Optional[str]=None
    complete:bool=False
    user_id:Optional[str]=None
class User(BaseModel):
    id:Optional[str]=None
    name:str
    
# database dependency
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session,Depends(get_db)]

#route
@app.post('/users/',response_model=User)
async def create_user(user:User,db:db_dependency):
    user.id=str(uuid4())
    print(user)
    db_user=models.User(id=user.id,name=user.name)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


    
    
@app.get('/users/{user_name}',response_model=User)
async def read_user(db:db_dependency,user_name:str):
    user=db.query(models.User).filter(models.User.name==user_name).first()
    if user:
        return user
    raise HTTPException(status_code=404,detail='User not found')
@app.get('/users/{user_name}/tasks',response_model=List[Task])
async def read_all_tasks(db:db_dependency,user_name:str):
    user=db.query(models.User).filter(models.User.name==user_name).first()
    if not user:
        raise HTTPException(status_code=404,detail='User not found')
    all_tasks=db.query(models.Task).filter(models.Task.user_id==user.id).all()
    return all_tasks
@app.post('/users/{user_name}/tasks',response_model=Task)
async def create_task(task:Task,db:db_dependency,user_name:str):
    user=db.query(models.User).filter(models.User.name==user_name).first()
    if not user:
        raise HTTPException(status_code=404,detail='User not found')
    task.id=str(uuid4())
    task.user_id=user.id
    # db_task=models.Task(id=task.id,title=task.title,description=task.description,user_id=task.user)
    db_task=models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task

@app.get('/users/{user_name}/tasks/{task_id}',response_model=Task)
async def read_task(task_id:str,user_name:str,db:db_dependency):
    user=db.query(models.User).filter(models.User.name==user_name).first()
    if not user:    
        raise HTTPException(status_code=404,detail='User not found')
    if not db.query(models.Task).filter(models.Task.id==task_id and models.Task.user==user.id).first():
        raise HTTPException(status_code=404,detail='User or Task not found')
    return db.query(models.Task).filter(models.Task.id==task_id and models.Task.user==user.id).first()
@app.put('/users/{user_name}/tasks/{task_id}',response_model=Task)
async def update_task(task_id:str,user_name:str,db:db_dependency,task:Task):
    user=db.query(models.User).filter(models.User.name==user_name).first()
    if not user:    
        raise HTTPException(status_code=404,detail='User not found')
    db_task=db.query(models.Task).filter(models.Task.id==task_id and models.Task.user==user.id).first()
    if not db_task:
        raise HTTPException(status_code=404,detail='User or Task not found')
    db_task.title=task.title
    db_task.complete=task.complete
    db_task.description=task.description
    db.commit()

    return db_task
    
@app.delete('/users/{user_name}/tasks/{task_id}')
async def delete_task(task_id:str,user_name:str,db:db_dependency,):
    user=db.query(models.User).filter(models.User.name==user_name).first()
    if not user:    
        raise HTTPException(status_code=404,detail='User not found')
    db_task=db.query(models.Task).filter(models.Task.id==task_id and models.Task.user_id==user.id).first()
    if not db_task:
        raise HTTPException(status_code=404,detail='User or Task not found')
    
    db.delete(db_task)
    db.commit()
    return {'message':'success!'}
    
 
@app.get('/')
def home():
    return {'homepage':"TTP"}


if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,port=8000)