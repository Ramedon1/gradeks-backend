from db.manager import db_manager
from web.models.users.user import DiaryInfo, GradesInfo, SubjectsInfo


def get_old_grade(grades: list[GradesInfo]) -> float:
    return round(sum(g.grade for g in grades) / len(grades), 2) if grades else None


def get_new_grade(grades: list[GradesInfo]) -> float:
    weighted_sum = sum(g.grade * g.coff for g in grades)
    cont = sum(g.coff for g in grades)
    return round(weighted_sum / cont, 2) if grades else None


async def get_diary_info(user_id: str, period_name: str) -> list[DiaryInfo]:
    periods = await db_manager.periods.get_periods_by_name(period_name)

    diary_info_list = []

    for period in periods:
        user_grades = await db_manager.grades.get_grades_by_quarter(
            user_id, period.period_date_start, period.period_date_end
        )
        subjects_dict = {}

        if user_grades:
            for grade in user_grades:
                subject_name = grade.subject
                if subject_name not in subjects_dict:
                    subjects_dict[subject_name] = []
                subjects_dict[subject_name].append(
                    GradesInfo(
                        coff=grade.grade_weight,
                        grade=grade.grade,
                        date=grade.grading_date.strftime("%d.%m"),
                    )
                )

        subjects_list = (
            sorted(
                [
                    SubjectsInfo(
                        subject_name=subject_name,
                        grades=(grades_info if grades_info else []),
                        new_type_grade=(
                            get_new_grade(grades_info) if grades_info else None
                        ),
                        old_type_grade=(
                            get_old_grade(grades_info) if grades_info else None
                        ),
                    )
                    for subject_name, grades_info in subjects_dict.items()
                ],
                key=lambda subject: subject.subject_name,
            )
            if user_grades
            else []
        )

        diary_info_list.append(
            DiaryInfo(
                quarter_name=quarter.quarter_name,
                quarter_date=f"{quarter.quarter_date_start.strftime('%d.%m.%y')} - {quarter.quarter_date_end.strftime('%d.%m.%y')}",
                type_grade=await db_manager.users.get_grade_type(user_id),
                subjects=subjects_list,
            )
        )

    return diary_info_list
