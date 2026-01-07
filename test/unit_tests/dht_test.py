import time
import board
import adafruit_dht

# Initialise the DHT22 device, using the board pin naming
# The pin is specified using the D number, not the physical pin number
# Example: GPIO pin 4 is board.D4, GPIO pin 18 is board.D18
dht_device = adafruit_dht.DHT11(board.D22)

try:
    while True:
        try:
            # Get both temperature and humidity in a single line
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity
            
            # Convert to Fahrenheit if needed
            temperature_f = temperature_c * (9 / 5) + 32
            
            # Print the results
            print("Temp: {:.1f} C / {:.1f} F Humidity: {}%".format(temperature_c, temperature_f, humidity))

        except RuntimeError as e:
            # Reading a sensor is not always successful, so retry
            print("Error reading data: {}".format(e.args[0]))
            
        time.sleep(2.0) # Wait for 2 seconds before repeating

        
finally:
    print("Exit Successful")
    dht_device.exit()


