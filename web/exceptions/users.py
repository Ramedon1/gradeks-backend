from fastapi import HTTPException
from starlette import status

DiaryIdDException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Diary ID is not valid"
)
