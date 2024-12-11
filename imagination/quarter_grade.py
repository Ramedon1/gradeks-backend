from PIL import Image, ImageDraw, ImageFont

from imagination.common import (create_badge, get_dynamic_font,
                                subject_with_line_grades)


def img_quarter_grade(data_quarter):
    logo_size = (120, 120)
    font_size = 50
    image_width = 1250
    padding_between_images = 20  # Padding between images
    top_padding = 100  # Initial padding at the top

    logo = Image.open("templates/logo.png").convert("RGBA").resize(logo_size)

    initial_height = 512
    img = Image.new("RGBA", (image_width, initial_height), "#144f3b")
    draw = ImageDraw.Draw(img)

    # Paste the logo with transparency in the upper-left corner
    logo_x, logo_y = 80, 67
    img.paste(logo, (logo_x, logo_y), mask=logo)

    # Write "Gradeks" opposite the logo
    gradeks_font = ImageFont.truetype("fonts/DMSans_24pt-Black.ttf", font_size + 10)
    gradeks_x = logo_x + logo_size[0] + 50
    gradeks_y = (logo_size[1] - (font_size + 10)) // 2 + logo_y
    draw.text((gradeks_x, gradeks_y), "Gradeks", font=gradeks_font, fill="white")

    # Define the subject name and adjust its position dynamically
    quarter_name = data_quarter.quarter_name
    quarter_name_font, wrapped_quarter_name = get_dynamic_font(
        quarter_name, 275, 86, "fonts/PFEncoreSansPro-Medium.ttf", initial_font_size=65
    )

    quarter_name_width = draw.textlength(quarter_name, font=quarter_name_font)
    quarter_name_x = (
        image_width - quarter_name_width - 90
    )  # Align to the right with padding

    # Adjust vertical alignment based on font size
    font_size_used = quarter_name_font.size
    adjustment_factor = (
        max(0, 55 - font_size_used) // 2
    )  # Lower when font size is smaller
    quarter_name_y = (
        gradeks_y + 15 + adjustment_factor
    )  # Align vertically with "Gradeks"

    draw.text(
        (quarter_name_x, quarter_name_y),
        quarter_name,
        font=quarter_name_font,
        fill="white",
    )

    # Generate subject results and calculate required canvas height
    subjects_result = []
    total_height = top_padding  # Start with initial padding
    for subject in data_quarter.subjects:
        badge_images = [
            create_badge(grade.grade, grade.coff) for grade in subject.grades
        ]
        subject_img = subject_with_line_grades(
            subject.subject_name,
            badge_images,
            2336,
            subject.new_type_grade,
            subject.old_type_grade,
        )
        subject_img = subject_img.convert("RGBA")  # Ensure transparency is retained
        subjects_result.append(subject_img)
        total_height += subject_img.height + padding_between_images

    # Expand the canvas height if needed (without stretching)
    if total_height > initial_height:
        new_height = total_height
        expanded_img = Image.new("RGBA", (image_width, new_height), "#144f3b")
        expanded_img.paste(
            img, (0, 0)
        )  # Paste the existing content onto the expanded canvas
        img = expanded_img  # Update img to the new expanded image

    # Draw subject images with uniform spacing
    current_y = top_padding
    for subject_img in subjects_result:
        subject_img = subject_img.resize(
            (subject_img.width // 2, subject_img.height // 2),
            Image.Resampling.LANCZOS,
        )
        img.paste(subject_img, (logo_x - 10, current_y + 150), mask=subject_img)
        current_y += subject_img.height + padding_between_images

    return img
