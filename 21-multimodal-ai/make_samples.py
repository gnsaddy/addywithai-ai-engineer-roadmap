# make_samples.py: draw a small cafe receipt to test with (Episode 21)
from PIL import Image, ImageDraw, ImageFont

ROWS = [("Masala dosa", "120.00"), ("Filter coffee x2", "80.00"),
        ("Gulab jamun", "60.00"), ("GST 5%", "13.00")]

def font(size):
    try:
        return ImageFont.truetype("DejaVuSansMono.ttf", size)
    except OSError:
        return ImageFont.load_default()

img = Image.new("RGB", (600, 800), "white")
d = ImageDraw.Draw(img)
d.text((150, 40), "UDUPI CAFE", fill="black", font=font(44))
d.text((170, 100), "11 Nov 2026  19:42", fill="gray", font=font(24))
y = 190
for item, price in ROWS:
    d.text((40, y), item, fill="black", font=font(30))
    d.text((440, y), price, fill="black", font=font(30))
    y += 60
d.line((40, y + 10, 560, y + 10), fill="black", width=3)
d.text((40, y + 40), "TOTAL", fill="black", font=font(38))
d.text((420, y + 40), "273.00", fill="black", font=font(38))
img.save("receipt.png")
print("saved receipt.png", img.size)
