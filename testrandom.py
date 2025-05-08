from PIL import Image as PILImage, ImageDraw, ImageFont
import uuid

def create_rotated_text_image(text, img_width=100, img_height=40, font_size=12):
    bg_color = "white"
    text_color = "black"

    # Create blank image
    image = PILImage.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Get text size
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)

    # Center the text
    x = (img_width - text_width) / 2
    y = (img_height - text_height) / 2

    draw.text((x, y), text, fill=text_color, font=font)

    # Rotate the image 90 degrees
    rotated_image = image.rotate(90, expand=True)

    # Save to a unique filename to avoid overwriting
    output_path = f"assets/rotated_{uuid.uuid4().hex[:8]}.png"
    rotated_image.save(output_path)

    return output_path
