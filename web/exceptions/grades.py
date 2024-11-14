from fastapi import HTTPException
from starlette import status

GradeTypeException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Grade type is not valid"
)

GradeFilterTypeException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Grade filter type is not valid"
)
