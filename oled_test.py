from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306  # Using SSD1306 driver for SH1106
from PIL import Image, ImageDraw, ImageFont

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

device.clear()

# Create image for drawing
image = Image.new("1", (device.width, device.height))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()
draw.text((0, 10), "Hello SH1106!", font=font, fill=255)

device.display(image)
