from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306  # We'll use ssd1306 class but it works with many 1106 modules
from PIL import Image, ImageDraw, ImageFont

# Initialize I2C (SDA=GPIO2, SCL=GPIO3)
serial = i2c(port=1, address=0x3C)

# Create device — ssd1306 class sometimes works for SSD1106
device = ssd1306(serial, rotate=0)  # rotate may be needed depending on your screen

# Clear display
device.clear()

# Create an image for drawing
image = Image.new("1", (device.width, device.height))
draw = ImageDraw.Draw(image)

# Draw some text
font = ImageFont.load_default()
draw.text((0, 10), "Hello SSD1106!", font=font, fill=255)

# Display the image
device.display(image)
