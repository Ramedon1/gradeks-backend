from PIL import Image, ImageDraw, ImageFont
from imagination.common import get_dynamic_font, badge_line, create_badge
from web.models.users.user import GradesInfo


def subject_grade_img(subject, grades: list[GradesInfo]):
    # Define image properties
    logo_size = (120, 120)
    font_size = 50
    image_width = 1250
    padding_from_edge = 80

    # Load the logo and resize it
    logo = Image.open('templates/logo.png').convert("RGBA").resize(logo_size)

    # Create a blank image with RGB mode
    img = Image.new("RGB", (image_width, 512), "#144f3b")
    draw = ImageDraw.Draw(img)

    # Create a transparent version of the main image for compositing
    img_with_alpha = img.convert("RGBA")

    # Paste the logo with transparency in the upper-left corner
    logo_x, logo_y = 80, 67
    img_with_alpha.paste(logo, (logo_x, logo_y), mask=logo)




    # Write "Gradeks" opposite the logo
    gradeks_font = ImageFont.truetype("fonts/DMSans_24pt-Black.ttf", font_size + 10)
    gradeks_x = logo_x + logo_size[0] + 50
    gradeks_y = (logo_size[1] - (font_size + 10)) // 2 + logo_y
    draw = ImageDraw.Draw(img_with_alpha)
    draw.text((gradeks_x, gradeks_y), "Gradeks", font=gradeks_font, fill="white")




    # Define the subject name and adjust its position dynamically
    subject_name = subject
    subject_font, wrapped_subject = get_dynamic_font(
        subject, 275, 86, 'fonts/PFEncoreSansPro-Medium.ttf', initial_font_size=65
    )

    # Calculate the width of the subject text
    subject_width = draw.textlength(subject_name, font=subject_font)
    subject_x = image_width - subject_width - padding_from_edge  # Align to the right with padding

    # Adjust vertical alignment based on font size
    font_size_used = subject_font.size
    adjustment_factor = max(0, 55 - font_size_used) // 2  # Lower when font size is smaller
    subject_y = gradeks_y + 15 + adjustment_factor  # Align vertically with "Gradeks" with adjustment

    draw.text((subject_x, subject_y), subject_name, font=subject_font, fill="white")



    # Draw a grades line
    badges_list = [create_badge(grade.grade, grade.coff) for grade in grades]
    rgba_badge_line = badge_line(badges_list, 2336)
    # Halve the size of the badge line
    badge_line_resized = rgba_badge_line.resize(
        (rgba_badge_line.width // 2, rgba_badge_line.height // 2), Image.Resampling.LANCZOS
    )

    # Paste the resized badge line onto the main image
    img_with_alpha.paste(badge_line_resized, (logo_x - 10, 250), badge_line_resized)

    # Save and show the image
    img_with_alpha.save("output_image.png")
    img_with_alpha.show()

subject_grade_img(subject='Основы безопасности и защиты Родины', grades=[GradesInfo(grade=5, coff=1, date='2022-10-10'), GradesInfo(grade=4, coff=2, date='2022-10-10'), GradesInfo(grade=3, coff=3, date='2022-10-10'), GradesInfo(grade=5, coff=1, date='2022-10-10'),GradesInfo(grade=5, coff=1, date='2022-10-10'), GradesInfo(grade=4, coff=2, date='2022-10-10'), GradesInfo(grade=3, coff=3, date='2022-10-10'), GradesInfo(grade=4, coff=2, date='2022-10-10'), GradesInfo(grade=3, coff=3, date='2022-10-10'), GradesInfo(grade=5, coff=1, date='2022-10-10'), GradesInfo(grade=4, coff=2, date='2022-10-10'), GradesInfo(grade=3, coff=3, date='2022-10-10'), GradesInfo(grade=5, coff=1, date='2022-10-10'), GradesInfo(grade=4, coff=2, date='2022-10-10'), GradesInfo(grade=3, coff=3, date='2022-10-10'), GradesInfo(grade=5, coff=1, date='2022-10-10'), GradesInfo(grade=4, coff=2, date='2022-10-10'), GradesInfo(grade=3, coff=3, date='2022-10-10')])
