import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize display (most 1.3" OLEDs are 128x64)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display
disp.fill(0)
disp.show()

# Create a blank image for drawing
image = Image.new("1", (disp.width, disp.height))
draw = ImageDraw.Draw(image)

# Draw a white rectangle and some text
draw.rectangle((0, 0, disp.width, disp.height), outline=255, fill=0)
draw.text((10, 25), "Hello OLED!", fill=255)

# Display image
disp.image(image)
disp.show()

print("✅ OLED test complete!")
