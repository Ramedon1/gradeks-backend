from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel
from typing import List, Optional


# Define the NewGrade model
class NewGrade(BaseModel):
    grade: int
    old_grade: Optional[int]
    date: str
    subject: str
    coff: int


def create_custom_image(grade_list: List[NewGrade], logo_path="logo.png"):
    # Define image properties
    width = 1250
    height = 512
    background_color = "#144f3b"
    logo_size = (120, 120)
    margin = 40
    font_size = 50
    badge_height = 40
    badge_padding = 0
    text_color = "white"
    gradeks_text = "Gradeks"

    # Load the logo and ensure it has transparency
    logo = Image.open(logo_path).convert("RGBA").resize(logo_size)

    # Create a blank image with RGB mode
    img = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # Create a transparent version of the main image for compositing
    img_with_alpha = img.convert("RGBA")

    # Paste the logo with transparency in the upper-left corner
    img_with_alpha.paste(logo, (margin, margin), mask=logo)

    # Set up the font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
        badge_font = ImageFont.truetype("arial.ttf", font_size - 10)
        gradeks_font = ImageFont.truetype("arial.ttf", font_size + 10)
    except IOError:
        font = ImageFont.load_default()
        badge_font = font
        gradeks_font = font

    # Write "Gradeks" opposite the logo
    gradeks_x = margin + logo_size[0] + margin
    gradeks_y = margin + (logo_size[1] - (font_size + 10)) // 2
    draw = ImageDraw.Draw(img_with_alpha)
    draw.text((gradeks_x, gradeks_y), gradeks_text, font=gradeks_font, fill=text_color)

    # Draw a divider line below the logo
    line_y = margin + logo_size[1] + margin - 20
    draw.line(((margin, line_y), (width - margin, line_y)), fill="yellow", width=5)

    # Starting position for the grades and badges
    x = margin
    y = margin + logo_size[1] + margin + 20  # Start below the divider
    line_height = font_size + badge_height + badge_padding

    for grade in grade_list:
        # Draw the "coff" badge
        coff_text = str(grade.coff)
        badge_width = draw.textbbox((0, 0), coff_text, font=badge_font)[2] + 20
        badge_x1 = x + 20
        badge_y1 = y
        badge_x2 = x + badge_width - 20
        badge_y2 = y + badge_height
        draw.rounded_rectangle(
            [(badge_x1, badge_y1), (badge_x2, badge_y2)],
            radius=10,
            fill="yellow",
        )
        coff_text_x = badge_x1 + (badge_width - draw.textbbox((0, 0), coff_text, font=badge_font)[2]) // 2
        coff_text_y = badge_y1 + (badge_height - draw.textbbox((0, 0), coff_text, font=badge_font)[3]) // 2
        draw.text((coff_text_x, coff_text_y), coff_text, font=badge_font, fill="black")

        # Draw the grade below the badge
        grade_text = str(grade.grade)
        grade_text_width = draw.textbbox((0, 0), grade_text, font=font)[2]
        grade_text_x = x
        grade_text_y = y + badge_height + badge_padding
        draw.text((grade_text_x, grade_text_y), grade_text, font=font, fill=text_color)

        # Update x position for the next badge and grade
        x += max(badge_width, grade_text_width) + margin

        # Wrap to the next line if needed
        if x > width - margin:
            x = margin
            y += line_height

        # Expand image height if needed
        if y + line_height > img_with_alpha.height - margin:
            new_height = img_with_alpha.height + line_height + margin
            new_img = Image.new("RGBA", (width, new_height), background_color)
            new_img.paste(img_with_alpha, (0, 0))
            img_with_alpha = new_img

    # Save and show the image
    img_with_alpha.convert("RGB").save("output_image.jpg")
    img_with_alpha.show()


# Example usage
grades = [
    NewGrade(grade=3, old_grade=80, date="2023-10-01", subject="Math", coff=2),
    NewGrade(grade=2, old_grade=None, date="2023-10-02", subject="Physics", coff=3),
    NewGrade(grade=1, old_grade=75, date="2023-10-03", subject="Chemistry", coff=1),
    NewGrade(grade=4, old_grade=90, date="2023-10-04", subject="Biology", coff=5),
]
create_custom_image(grades)
