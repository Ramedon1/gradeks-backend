from datetime import date

from sqlmodel import Field, SQLModel


class Quarters(SQLModel, table=True):
    """
    Данные о четвертях и полугодиях.

    Attributes:
        quarter_name (str): название четверти
        quarter_date_start (date): дата начала четверти
        quarter_date_end (date): дата окончания четверти
    """

    __tablename__ = "quarters"

    quarter_name: str = Field(default=None, nullable=False, primary_key=True)
    quarter_date_start: date = Field(default=None, nullable=False)
    quarter_date_end: date = Field(default=None, nullable=False)
