from PIL import Image, ImageDraw, ImageFont

from imagination.common import get_color_grade, get_dynamic_font


def day_grade_img(date: str, grade: int, coff: int, subject: str):
    template = Image.open("templates/day_template.png").convert("RGB")
    draw = ImageDraw.Draw(template)
    grade_font = ImageFont.truetype("fonts/DMSans_24pt-Black.ttf", 150)
    coff_font = ImageFont.truetype("fonts/DMSans_24pt-Black.ttf", 52)
    date_font = ImageFont.truetype("fonts/DMSans_24pt-Black.ttf", 27)
    subject_font_path = "fonts/PFEncoreSansPro-Medium.ttf"

    # Draw the Grade
    draw.text(
        (722, 775), str(grade), fill=get_color_grade(grade), font=grade_font
    )

    # Draw the Coff
    draw.text((885, 695), str(coff), fill="white", font=coff_font)

    # Draw the Date
    draw.text((1227, 1408), date, fill="black", font=date_font)

    # Draw the Subject with dynamic font size
    max_width = 500
    max_height = 75
    block_x_center = 525 + max_width / 2  # Center of the block
    y_subject = 1122

    # Get dynamically adjusted font and wrapped text
    subject_font, wrapped_subject = get_dynamic_font(
        subject, max_width, max_height, subject_font_path, initial_font_size=79
    )

    line_spacing = 10
    for line in wrapped_subject:
        text_width = draw.textbbox((0, 0), line, font=subject_font)[2]
        x_subject = block_x_center - (text_width / 2)
        _, _, _, line_height = draw.textbbox((0, 0), line, font=subject_font)
        draw.text((x_subject, y_subject), line, fill="#074E46", font=subject_font)
        y_subject += line_height + line_spacing

    template.convert("RGB").save("output_image.jpg")

    return
