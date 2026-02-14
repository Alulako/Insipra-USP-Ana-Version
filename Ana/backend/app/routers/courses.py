from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import Course, User
from ..schemas import CourseCreate, CourseOut

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("", response_model=list[CourseOut])
def list_courses(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Course).filter(Course.user_id == user.id).all()

@router.post("", response_model=CourseOut)
def create_course(data: CourseCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = Course(user_id=user.id, title=data.title, description=data.description)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}")
def delete_course(course_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course or course.user_id != user.id:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    db.delete(course)
    db.commit()
    return {"ok": True}
