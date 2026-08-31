from fastapi import APIRouter, status

from app.pets.pets_service import pets_service
from app.shared.response_schema import ApiResponse
from app.students.students_schemas import CreateStudentDto, Student, UpdateStudentDto
from app.students.students_service import students_service
#from app.shared.ApiResponse import ApiResponse  

from app.shared.response_schema import ApiResponse
router = APIRouter(prefix="/api/students", tags=["Students"])

@router.get("", response_model=ApiResponse[list[Student]])
def find_all() -> ApiResponse[list[Student]]:
    students = students_service.find_all()
    return ApiResponse(
        success=True,
        status=status.HTTP_200_OK,
        message="La lista de estudiantes se obtuvo exitosamente",
        data=students,
        error=None,
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

    if not deleted:
        return ApiResponse(
            status=404,
            error=True,
            message=f"Estudiante con ID {student_id} no fue encontrado",
            data=None,
        )

    return ApiResponse(
        status=200,
        error=False,
        message="Estudiante eliminado exitosamente",
        data=deleted,
    )
