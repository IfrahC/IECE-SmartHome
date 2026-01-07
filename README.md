# SmartHome — Smart Sensor Dashboard

**Project Overview**

- **Description:** A Raspberry Pi–based live sensor dashboard and gate controller that reads temperature/humidity (DHT11), distance (ultrasonic), motion (PIR), and drives a servo, LEDs and a relay. The project includes a Tkinter GUI for real-time display and control logic in `final.py`.
- **Purpose:** Demonstrates simple home automation and sensor visualization for teaching and prototyping.

**Features**

- **Live Dashboard:** GUI shows Temperature, Humidity, Distance, and Motion status updating in real time.
- **Gate Control:** Servo moves between min/max based on ultrasonic distance readings.
- **Motion Response:** PIR motion toggles relay and updates motion status.
- **LED Indicators:** Visual status using two LEDs and relay control logic.
- **Lightweight Threaded Loop:** Sensor polling runs in a daemon thread; GUI runs on main thread.

**Components Used**

- **Microcontroller:** Raspberry Pi (GPIO + PiGPIO for remote pin control)
- **Sensors & Actuators:**
  - DHT11 (temperature & humidity)
  - Ultrasonic Distance Sensor (HC-SR04 style)
  - PIR Motion Sensor
  - Servo motor (gate)
  - LEDs and Relay module
- **Wiring (as used in `final.py`):**
  - **LED1:** GPIO 9
  - **LED2:** GPIO 3
  - **Relay:** GPIO 20
  - **PIR:** GPIO 6
  - **Servo:** GPIO 13
  - **Ultrasonic Trigger:** GPIO 17
  - **Ultrasonic Echo:** GPIO 27
  - **DHT11:** board.D4 (physical pin D4)

**Software & Libraries**

- **Language:** Python 3
- **GUI:** `tkinter`
- **GPIO & hardware:** `gpiozero`, `pigpio` (PiGPIOFactory), `adafruit_dht`, `board`
- **Utilities:** `time`, `threading`

**Setup & Run**

- **Install dependencies:**

```bash
pip3 install gpiozero pigpio adafruit-circuitpython-dht adafruit-blinka
```

- **Ensure `pigpiod` is running on the Pi:**

```bash
sudo pigpiod
```

- **Run the dashboard:**

```bash
python3 final.py
```

**Notes & Tips**

- Run on a Raspberry Pi with required sensors connected to the pins listed above.
- `adafruit_dht` may require running with appropriate permissions; if you see DHT read errors, wait and retry (the script catches short RuntimeErrors).
- The repository contains additional example scripts and unit tests under the `test/` folder for OLED and sensor examples.

**Files**

- **Main GUI & logic:** [final.py](final.py)
- **Other scripts & tests:** see `test/` folder (dht*oled.py, gui.py, oled*_.py, unit_tests/_)

**Authors**

- Ifrah Chishti
- Muhammad Khan
- Marrium Burhan
- Syeda Batool Fatima
