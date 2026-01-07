import Adafruit_DHT
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
from time import sleep, strftime

DHT_SENSOR = Adafruit_DHT.DHT22   
DHT_PIN = 4                       # GPIO pin connected to DHT data pin

RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    current_time = strftime("%H:%M:%S")
    current_date = strftime("%b %d, %Y")

    if humidity is not None and temperature is not None:
        draw.text((0, 0), f"Temp: {temperature:.1f}°C", font=font, fill=255)
        draw.text((0, 16), f"Humidity: {humidity:.1f}%", font=font, fill=255)
    else:
        draw.text((0, 0), "Sensor error!", font=font, fill=255)

    draw.text((0, 36), f"{current_time}", font=font, fill=255)
    draw.text((0, 48), f"{current_date}", font=font, fill=255)

    disp.image(image)
    disp.display()
    sleep(2)
