from fastapi import APIRouter
from app.pets.pets_service import pets_service
from app.students.students_schemas import CreateStudentDto, Student, UpdateStudentDto
from app.students.students_service import students_service
#from app.shared.response_schema import ApiResponse

from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")

# Clase temporal de respuesta estándar hasta que se integre la de la carpeta shared
class ApiResponse(BaseModel, Generic[T]):
    success: bool
    status: int
    message: str
    error: Optional[Any] = None
    data: Optional[T] = None

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.get("", response_model=ApiResponse[list[Student]])
def find_all():
    students = students_service.find_all()
    return ApiResponse(
        success=True,
        status=200,
        message="Estudiantes obtenidos exitosamente",
        data=students
    )

@router.get("/{student_id}", response_model=ApiResponse[Student])
def find_by_id(student_id: str):
    try:
        student = students_service.find_by_id(student_id)
        return ApiResponse(
            success=True,
            status=200,
            message="Estudiante obtenido exitosamente",
            error=None,
            data=student
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            status=404,
            message="No se pudo encontrar el estudiante",
            error=str(e),
            data=None
        )
    
@router.post("", status_code=201, response_model=ApiResponse[Student])
def create(body: CreateStudentDto):
    student = students_service.create(body)
    return ApiResponse(
        success=True,
        status=201,
        message="Estudiante creado exitosamente",
        data=student
    )

@router.patch("/{student_id}", response_model=ApiResponse[Student])
def update(student_id: str, body: UpdateStudentDto):
    student = students_service.update(student_id, body)
    return ApiResponse(
        success=True,
        status=200,
        message="Estudiante actualizado exitosamente",
        data=student
    )

@router.delete("/{student_id}", response_model=ApiResponse[Student])
def delete(student_id: str):
    deleted = students_service.delete(student_id)
    pets_service.delete_all_for_student(student_id)
    return ApiResponse(
        success=True,
        status=200,
        message="Estudiante eliminado exitosamente",
        data=deleted
    )