from fastapi import HTTPException
from starlette import status

DiaryIdException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Diary ID is not valid"
)

GradeTypeException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid grade type filter"
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)

UserInactiveException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive"
)
