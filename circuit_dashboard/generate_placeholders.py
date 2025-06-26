import os
from PIL import Image, ImageDraw, ImageFont

def create_simple_test_image(filepath="circuit_dashboard/static/images/components/test_image.png"):
    """Creates a very simple test image."""
    width, height = 200, 150
    color = (200, 200, 200) # Light gray

    image = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(image)

    try:
        # Try to use a standard font
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        # Fallback to a default PIL font if arial.ttf is not found
        font = ImageFont.load_default()

    text = "Test Image"
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]

    # Calculate text position to center it
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2

    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font) # Black text

    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    image.save(filepath)
    print(f"✅ Created simple test image: {filepath}")

if __name__ == "__main__":
    create_simple_test_image() 