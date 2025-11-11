import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Create the I2C interface
i2c = board.I2C()

# Create the display object
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display
display.fill(0)
display.show()

# Create an image to draw on
image = Image.new("1", (display.width, display.height))
draw = ImageDraw.Draw(image)

# Draw text
font = ImageFont.load_default()
draw.text((10, 30), "Hello Pi!", font=font, fill=255)

# Display image
display.image(image)
display.show()
