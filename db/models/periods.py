from datetime import date

from sqlmodel import Field, SQLModel


class Periods(SQLModel, table=True):
    """
    Данные о четвертях и полугодиях.

    Attributes:
        period_type (str): тип периода, может быть "quarter" или "semester"
        period_name (str): название периода
        period_date_start (date): дата начала периода
        period_date_end (date): дата окончания периода
    """

    __tablename__ = "periods"

    period_type: str = Field(default=None, nullable=False)
    period_name: str = Field(default=None, nullable=False, primary_key=True)
    period_date_start: date = Field(default=None, nullable=False)
    period_date_end: date = Field(default=None, nullable=True)
