from PIL import Image, ImageDraw, ImageFont

from imagination.common import (create_badge, get_dynamic_font,
                                subject_with_line_grades)
from web.models.users.user import DiaryInfo


async def img_quarter_grade(data_quarter: DiaryInfo, quarter_name: str):
    logo_size = (120, 120)
    font_size = 50
    image_width = 1250
    padding_between_images = 20
    top_padding = 100
    bottom_padding = 100
    image_scale_factor = 0.5

    logo = (
        Image.open("imagination/templates/logo.png").convert("RGBA").resize(logo_size)
    )
    initial_height = 512
    img = Image.new("RGBA", (image_width, initial_height), "#144f3b")
    draw = ImageDraw.Draw(img)

    logo_x, logo_y = 80, 67
    img.paste(logo, (logo_x, logo_y), mask=logo)

    gradeks_font = ImageFont.truetype(
        "imagination/fonts/DMSans_24pt-Black.ttf", font_size + 10
    )
    gradeks_x = logo_x + logo_size[0] + 50
    gradeks_y = (logo_size[1] - (font_size + 10)) // 2 + logo_y
    draw.text((gradeks_x, gradeks_y), "Gradeks", font=gradeks_font, fill="white")

    quarter_name_font, wrapped_quarter_name = get_dynamic_font(
        quarter_name,
        275,
        86,
        "imagination/fonts/PFEncoreSansPro-Medium.ttf",
        initial_font_size=65,
    )
    quarter_name_width = draw.textlength(quarter_name, font=quarter_name_font)
    quarter_name_x = image_width - quarter_name_width - 90
    font_size_used = quarter_name_font.size
    adjustment_factor = max(0, 55 - font_size_used) // 2
    quarter_name_y = gradeks_y + 15 + adjustment_factor
    draw.text(
        (quarter_name_x, quarter_name_y),
        quarter_name,
        font=quarter_name_font,
        fill="white",
    )

    subjects_result = []
    total_height = top_padding + bottom_padding
    for subject in data_quarter.subjects:
        badge_images = [
            create_badge(grade.grade, grade.coff).convert("RGBA")
            for grade in subject.grades
        ]

        subject_img = subject_with_line_grades(
            subject.subject_name,
            badge_images,
            2336,
            subject.new_type_grade,
            subject.old_type_grade,
        ).convert("RGBA")

        subject_img = subject_img.resize(
            (
                int(subject_img.width * image_scale_factor),
                int(subject_img.height * image_scale_factor),
            ),
            Image.Resampling.LANCZOS,
        )

        subjects_result.append(subject_img)
        total_height += subject_img.height + padding_between_images

    if subjects_result:
        total_height -= padding_between_images

    if total_height > initial_height:
        new_height = total_height + 150
        expanded_img = Image.new("RGBA", (image_width, new_height), "#144f3b")
        expanded_img.paste(img, (0, 0))
        img = expanded_img

    current_y = top_padding + 150
    for subject_img in subjects_result:
        img.paste(subject_img, (logo_x - 10, current_y), mask=subject_img)
        current_y += subject_img.height + padding_between_images

    logo = Image.open("imagination/templates/prod_by_ramedon_w.png").convert("RGBA")
    img.paste(logo, (434, img.height - 80), mask=logo)

    return img
