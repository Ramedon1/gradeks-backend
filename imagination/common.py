from PIL import Image, ImageDraw, ImageFont


def get_color_grade(grade: int | float) -> str:
    if grade >= 5:
        return "#0ca139"
    if grade >= 4:
        return "#ff9600"
    if grade >= 3:
        return "#FC0"
    if grade >= 2:
        return "#ff4d4d"
    return "#000"


def wrap_text(draw, text, font, max_width):
    """Wraps text to fit within a specified width."""
    lines = []
    words = text.split()
    current_line = ""

    for word in words:
        # Check if the word can fit in the current line
        test_line = f"{current_line} {word}".strip()
        text_width = draw.textbbox((0, 0), test_line, font=font)[
            2
        ]  # Get the width of the text
        if text_width <= max_width:
            current_line = test_line
        else:
            # Move current line to the list and start a new line
            lines.append(current_line)
            current_line = word

    # Add the last line
    if current_line:
        lines.append(current_line)

    return lines


def get_dynamic_font(subject, max_width, max_height, font_path, initial_font_size):
    """Adjust font size to ensure text fits within the given block."""
    font_size = initial_font_size
    while font_size > 10:  # Minimum font size threshold
        font = ImageFont.truetype(font_path, font_size)
        temp_image = Image.new(
            "RGB", (1, 1)
        )  # Create a temporary canvas to measure text size
        draw = ImageDraw.Draw(temp_image)

        wrapped_text = wrap_text(draw, subject, font, max_width)
        total_height = (
            sum(draw.textbbox((0, 0), line, font=font)[3] for line in wrapped_text)
            + (len(wrapped_text) - 1) * 10
        )  # Add line spacing

        if total_height <= max_height:
            return font, wrapped_text  # Return the font and wrapped text
        font_size -= 1  # Reduce font size

    raise ValueError("Text cannot fit within the specified dimensions.")


def create_badge(grade: int, coff: int) -> Image:
    # Layer dimensions
    layer_width, layer_height = 170, 100
    corner_radius = 20  # Rounded corners for the badge and notification areas

    # Colors
    badge_color = (238, 242, 241)  # Light background
    text_color = get_color_grade(grade)
    notification_color = (28, 41, 35)  # Dark background for notification
    notification_text_color = (255, 255, 255)  # White for "2"

    # Create a blank layer (transparent)
    layer = Image.new("RGBA", (layer_width, layer_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(layer)

    # Draw rounded rectangle for the main badge background
    badge_width, badge_height = 120, 80
    badge_x = (layer_width - badge_width) // 2
    badge_y = (layer_height - badge_height) // 2
    draw.rounded_rectangle(
        [(badge_x, badge_y), (badge_x + badge_width, badge_y + badge_height)],
        radius=corner_radius,
        fill=badge_color,
    )

    # Draw smaller rounded rectangle for notification
    notif_width, notif_height = 60, 40
    notif_x = badge_x + badge_width - notif_width + 20
    notif_y = 0
    draw.rounded_rectangle(
        [(notif_x, notif_y), (notif_x + notif_width, notif_y + notif_height)],
        radius=corner_radius // 2,
        fill=notification_color,
    )

    font_large = ImageFont.truetype("fonts/DMSans_24pt-Black.ttf", 40)
    font_small = ImageFont.truetype("fonts/DMSans_24pt-Black.ttf", 23)

    text = str(grade)
    text_bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = badge_x + (badge_width - text_width) // 2 + 3
    text_y = badge_y + (badge_height - text_height) // 2 - 8
    draw.text((text_x, text_y), text, fill=text_color, font=font_large)

    notif_text = str(coff)
    notif_text_bbox = draw.textbbox((0, 0), notif_text, font=font_small)
    notif_text_width, notif_text_height = (
        notif_text_bbox[2] - notif_text_bbox[0],
        notif_text_bbox[3] - notif_text_bbox[1],
    )
    notif_text_x = notif_x + (notif_width - notif_text_width) // 2 + 2
    notif_text_y = notif_y + (notif_height - notif_text_height) // 2 - 5
    draw.text(
        (notif_text_x, notif_text_y),
        notif_text,
        fill=notification_text_color,
        font=font_small,
    )

    return layer


def badge_line(images: list[Image.Image], max_width: int):
    # Variables to track the current line's dimensions
    current_width = 0
    current_height = 0
    lines = []
    line = []

    # Organize images into lines based on max_width
    for image in images:
        if current_width + image.width > max_width:
            # Add the current line to lines and reset
            lines.append((line, current_width, current_height))
            line = []
            current_width = 0
            current_height = 0

        line.append(image)
        current_width += image.width
        current_height = max(current_height, image.height)

    # Add the final line
    if line:
        lines.append((line, current_width, current_height))

    # Calculate the total height and width of the final image
    total_height = sum(line_height for _, _, line_height in lines)
    total_width = max(line_width for _, line_width, _ in lines)

    # Create a blank image with a transparent background
    final_image = Image.new("RGBA", (total_width, total_height), (255, 255, 255, 0))

    # Paste the images into the final image
    y_offset = 0
    for line, _, line_height in lines:
        x_offset = 0
        for image in line:
            final_image.paste(image, (x_offset, y_offset), mask=image)
            x_offset += image.width
        y_offset += line_height

    return final_image.convert("RGBA")


def subject_with_line_grades(
    subject_name: str,
    image_line: list[Image.Image],
    max_width: int,
    new_type_grade: float,
    old_type_grade: float,
):
    # Calculate dimensions for the subject text
    font = ImageFont.truetype("fonts/PFEncoreSansPro-Medium.ttf", 60)
    temp_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
    draw = ImageDraw.Draw(temp_image)

    subject_bbox = draw.textbbox((0, 0), subject_name, font=font)
    subject_width = subject_bbox[2] - subject_bbox[0]
    subject_height = subject_bbox[3] - subject_bbox[1]

    # Generate the badge line image
    badge_line_image = badge_line(image_line, max_width=max_width)

    # Determine final image dimensions
    final_width = max(
        subject_width + 200, badge_line_image.width + 200
    )  # Add padding for grades on the right
    final_height = subject_height + 20 + badge_line_image.height

    # Create the final canvas
    img = Image.new("RGBA", (final_width + 50, final_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    grades_font = ImageFont.truetype("fonts/PFEncoreSansPro-Medium.ttf", 45)
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

    # Position grades on the right side (offset from the subject text)
    grades_x = subject_bbox[2] + 40
    grades_y = subject_height // 2 - (subject_height // 4)
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

    # Draw the subject name aligned with the badge line's start
    text_x = 20  # A little padding from the left
    text_y = 0
    draw.text((text_x, text_y), subject_name, fill="white", font=font)

    # Paste the badge line image below the subject name
    badge_line_y = subject_height + 20
    badge_line_x = subject_bbox[1]
    img.paste(badge_line_image, (badge_line_x, badge_line_y), mask=badge_line_image)

    return img.convert("RGBA")
