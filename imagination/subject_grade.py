from PIL import Image, ImageDraw, ImageFont

from imagination.common import (badge_line, create_badge, get_color_grade,
                                get_dynamic_font)
from web.models.users.user import GradesInfo


async def subject_grade_img(
    subject: str, new_type_grade: float, old_type_grade: float, grades: list[GradesInfo]
):
    logo_size = (120, 120)
    font_size = 50
    image_width = 1250
    padding_from_edge = 80

    logo = Image.open("imagination/templates/logo.png").convert("RGBA").resize(logo_size)

    initial_height = 512
    img = Image.new("RGB", (image_width, initial_height), "#144f3b")

    img_with_alpha = img.convert("RGBA")

    # Paste the logo with transparency in the upper-left corner
    logo_x, logo_y = 80, 67
    img_with_alpha.paste(logo, (logo_x, logo_y), mask=logo)

    # Write "Gradeks" opposite the logo
    gradeks_font = ImageFont.truetype("imagination/fonts/DMSans_24pt-Black.ttf", font_size + 10)
    gradeks_x = logo_x + logo_size[0] + 50
    gradeks_y = (logo_size[1] - (font_size + 10)) // 2 + logo_y
    draw = ImageDraw.Draw(img_with_alpha)
    draw.text((gradeks_x, gradeks_y), "Gradeks", font=gradeks_font, fill="white")

    # Define the subject name and adjust its position dynamically
    subject_name = subject
    subject_font, wrapped_subject = get_dynamic_font(
        subject, 275, 86, "imagination/fonts/PFEncoreSansPro-Medium.ttf", initial_font_size=65
    )

    # Calculate the width of the subject text
    subject_width = draw.textlength(subject_name, font=subject_font)
    subject_x = (
        image_width - subject_width - padding_from_edge
    )  # Align to the right with padding

    # Adjust vertical alignment based on font size
    font_size_used = subject_font.size
    adjustment_factor = (
        max(0, 55 - font_size_used) // 2
    )  # Lower when font size is smaller
    subject_y = (
        gradeks_y + 15 + adjustment_factor
    )  # Align vertically with "Gradeks" with adjustment

    draw.text((subject_x, subject_y), subject_name, font=subject_font, fill="white")

    grades_font = ImageFont.truetype("imagination/fonts/PFEncoreSansPro-Medium.ttf", 45)
    # Grades as separate parts with a slash
    new_grade_text = f"{new_type_grade:.1f}"
    old_grade_text = f"{old_type_grade:.1f}"
    slash_text = " / "

    # Colors for each grade
    new_grade_color = get_color_grade(new_type_grade)
    old_grade_color = get_color_grade(old_type_grade)

    # Calculate text widths
    new_grade_width = draw.textlength(new_grade_text, font=grades_font)
    slash_width = draw.textlength(slash_text, font=grades_font)
    old_grade_width = draw.textlength(old_grade_text, font=grades_font)

    # Total width of the combined grades text
    total_grades_width = new_grade_width + slash_width + old_grade_width

    # Align grades 80 pixels from the right
    grades_x = image_width - total_grades_width - padding_from_edge
    grades_y = subject_y + 65  # Position grades below the subject

    # Draw each part of the grades text with its color
    draw.text(
        (grades_x, grades_y), new_grade_text, font=grades_font, fill=new_grade_color
    )
    draw.text(
        (grades_x + new_grade_width, grades_y),
        slash_text,
        font=grades_font,
        fill="white",
    )
    draw.text(
        (grades_x + new_grade_width + slash_width, grades_y),
        old_grade_text,
        font=grades_font,
        fill=old_grade_color,
    )

    # Draw a grades line
    badges_list = [create_badge(grade.grade, grade.coff) for grade in grades]
    rgba_badge_line = badge_line(badges_list, 2336)
    # Halve the size of the badge line
    badge_line_resized = rgba_badge_line.resize(
        (rgba_badge_line.width // 2, rgba_badge_line.height // 2),
        Image.Resampling.LANCZOS,
    )

    # Determine if the image needs to expand
    badge_line_bottom = 240 + badge_line_resized.height
    if badge_line_bottom > img.height:
        # Expand the image downward
        new_height = badge_line_bottom + 50  # Add some padding
        expanded_img = Image.new("RGB", (image_width, new_height), "#144f3b")
        expanded_img.paste(img_with_alpha, (0, 0))
        img_with_alpha = expanded_img

    img_with_alpha.paste(badge_line_resized, (logo_x - 10, 240), badge_line_resized)

    logo = Image.open("imagination/templates/prod_by_ramedon_w.png").convert("RGBA")
    img_with_alpha.paste(logo, (434, img_with_alpha.height - 80), mask=logo)

    return img_with_alpha
