from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: int, book: dict, response: Response, db: Session = Depends(get_db)):
    currentbook = db.query(models.Book).filter(models.Book.id == book_id).first()
    if currentbook:
        currentbook.id = book['id']
        currentbook.title = book['title']
        currentbook.author = book['author']
        currentbook.year = book['year']
        currentbook.is_published = book['is_published']
        db.commit()
        db.refresh(currentbook)
        response.status_code = 202
        return currentbook
    else:
        response.status_code = 404
        return {'message': 'book not found'}

@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db.delete(book)
    db.commit()



#---------Student----------
@router_v1.get('/student')
async def get_stu(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router_v1.get('/student/{stu_id}')
async def get_stu(stu_id: str, db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Student.id == stu_id).first()

@router_v1.post('/student')
async def create_stu(stu: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newstu = models.Student(id=stu['id'], fname=stu['fname'], lname=stu['lname'], dob=stu['dob'], gender=stu['gender'])
    db.add(newstu)
    db.commit()
    db.refresh(newstu)
    response.status_code = 201
    return newstu


#------Delete-------
@router_v1.delete('/student/{stu_id}')
async def del_stu(stu_id: str, db: Session = Depends(get_db)):
    stu = db.query(models.Student).filter(models.Student.id == stu_id).first()
    db.delete(stu)
    db.commit()

@router_v1.put('/student/{stu_id}')
async def update_stu(stu: models.StudentUpdate, stu_id: str, response: Response, db: Session = Depends(get_db)):

    stu_info = db.query(models.Student).filter(models.Student.id == stu_id).first()
    if not stu_info:
        response.status_code = 404
        return
    new_info = stu.dict(exclude_unset=True)
    for key,val in new_info.items():
        setattr(stu_info, key, val)
    db.commit()
    db.refresh(stu_info)
    response.status_code = 200
    return stu_info

    

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
