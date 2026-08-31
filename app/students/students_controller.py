from fastapi import APIRouter, status

from app.pets.pets_service import pets_service
from app.shared.response_schema import ApiResponse
from app.students.students_schemas import CreateStudentDto, Student, UpdateStudentDto
from app.students.students_service import students_service
from app.shared.ApiResponse import ApiResponse  

from app.shared.response_schema import ApiResponse
router = APIRouter(prefix="/api/students", tags=["Students"])

@router.get("")
def find_all() -> list[Student]:
    return students_service.find_all()

@router.get("/{student_id}")
def find_by_id(student_id: str) -> Student:
    return students_service.find_by_id(student_id)

@router.post("", status_code=201)
def create(body: CreateStudentDto) -> ApiResponse[Student]:
    student = students_service.create(body)
    return ApiResponse(
        success=True,
        status=201,
        message="Estudiante creado con éxito",
        data=student,
        error=None
    )

@router.patch("/{student_id}", response_model=ApiResponse[Student])
def update(student_id: str, body: UpdateStudentDto) -> ApiResponse[Student]:
    updated_student = students_service.update(student_id, body)
    return ApiResponse(
        success=True,
        status=200,
        message="Estudiante actualizado exitosamente",
        data=updated_student
    )

@router.delete("/{student_id}", response_model=ApiResponse[Student])
def delete(student_id: str):
    deleted = students_service.delete(student_id)
    pets_service.delete_all_for_student(student_id)
    return deleted
