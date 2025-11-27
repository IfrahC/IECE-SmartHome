# ------------------------- IMPORTS ------------------------- #
import time
import board
import adafruit_dht
import tkinter as tk
from gpiozero import Servo, DistanceSensor, LED, MotionSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# ------------------------- HARDWARE SETUP ------------------------- #
factory = PiGPIOFactory()

# LEDs + Relay
led1 = LED(9)
led2 = LED(3)
relay = LED(19)
led1.on()
led2.off()

# PIR Motion Sensor
pir = MotionSensor(6, pin_factory=factory)

# Servo
servo = Servo(13, pin_factory=factory, min_pulse_width=0.001, max_pulse_width=0.002)
servo.min()

# Ultrasonic Sensor
sensor = DistanceSensor(echo=27, trigger=17, max_distance=1.5, pin_factory=factory)

# DHT11
dht_device = adafruit_dht.DHT11(board.D22)

# ------------------------- GLOBAL VARIABLES ------------------------- #
gateOpen = False
distanceDisplay = "--"
temp_c = "--"
humidity = "--"
motion_status = "None"

# ------------------------- SENSOR FUNCTIONS ------------------------- #
def detected():
    global gateOpen
    if not gateOpen:
        gateOpen = True
        servo.max()
        relay.on()
        led1.on()
        led2.off()
        sleep(1)

def not_detected():
    global gateOpen
    if gateOpen:
        gateOpen = False
        servo.min()
        relay.off()
        led1.off()
        led2.on()
        sleep(1)

def check_distance():
    global distanceDisplay
    dist = sensor.distance * 100
    distanceDisplay = f"{dist:.1f}"
    if dist > 40:
        not_detected()
    else:
        detected()

def read_DHT():
    global temp_c, humidity
    try:
        temp_c = dht_device.temperature
        humidity = dht_device.humidity
    except RuntimeError:
        temp_c = "--"
        humidity = "--"

def check_motion():
    global motion_status
    motion_status = "Detected" if pir.motion_detected else "None"

# ------------------------- GUI SETUP ------------------------- #
# Colors & fonts
WINDOW_BG = "#0f1724"
CARD_BG = "#0b1b2b"
CARD_HOVER = "#133041"
TITLE_FG = "#e6f0ff"
SUBTITLE_FG = "#a6b8d9"
ACCENTS = {
    "temp": "#00eaff",
    "humidity": "#ffdd57",
    "distance": "#98ff98",
    "motion": "#ff7373",
}

TITLE_FONT = ("Helvetica", 18, "bold")
LABEL_FONT = ("Helvetica", 10)
VALUE_FONT = ("Helvetica", 16, "bold")

# ------------------------- CARD CREATOR ------------------------- #
def create_card(parent, title_text, fg_color, width=140, height=110, radius=12):
    canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0, bg=WINDOW_BG)
    x1, y1, x2, y2 = 4, 4, width - 4, height - 4
    r = radius
    # Draw background with rounded corners
    bg_ids = [
        canvas.create_rectangle(x1+r, y1, x2-r, y2, fill=CARD_BG, outline=""),
        canvas.create_rectangle(x1, y1+r, x2, y2-r, fill=CARD_BG, outline=""),
        canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, fill=CARD_BG, outline=""),
        canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, fill=CARD_BG, outline=""),
        canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, fill=CARD_BG, outline=""),
        canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, fill=CARD_BG, outline=""),
    ]
    title_id = canvas.create_text(width//2, 20, text=title_text, font=LABEL_FONT, fill="#cbd7ea")
    divider_id = canvas.create_rectangle(8, height//2-18, width-8, height//2-16, fill="#173248", outline="")
    value_id = canvas.create_text(width//2, height//2+6, text="--", font=VALUE_FONT, fill=fg_color)

    def on_enter(event):
        for i in bg_ids: canvas.itemconfig(i, fill=CARD_HOVER)
    def on_leave(event):
        for i in bg_ids: canvas.itemconfig(i, fill=CARD_BG)
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    return canvas, value_id

# ------------------------- CREATE WINDOW ------------------------- #
window = tk.Tk()
window.title("Smart Sensor Dashboard")
window.geometry("640x260")
window.configure(bg=WINDOW_BG)

title = tk.Label(window, text="Live Sensor Dashboard", font=TITLE_FONT, fg=TITLE_FG, bg=WINDOW_BG)
title.pack(pady=(12, 2))
subtitle = tk.Label(window, text="Overview of connected sensors — updates live", font=LABEL_FONT, fg=SUBTITLE_FG, bg=WINDOW_BG)
subtitle.pack(pady=(0, 12))

cards_frame = tk.Frame(window, bg=WINDOW_BG)
cards_frame.pack(pady=6)

# Create sensor cards
temp_card_canvas, temp_val = create_card(cards_frame, "Temperature", ACCENTS["temp"])
humidity_card_canvas, humidity_val = create_card(cards_frame, "Humidity", ACCENTS["humidity"])
distance_card_canvas, distance_val = create_card(cards_frame, "Distance", ACCENTS["distance"])
motion_card_canvas, motion_val = create_card(cards_frame, "Motion", ACCENTS["motion"])

temp_card_canvas.grid(row=0, column=0, padx=10)
humidity_card_canvas.grid(row=0, column=1, padx=10)
distance_card_canvas.grid(row=0, column=2, padx=10)
motion_card_canvas.grid(row=0, column=3, padx=10)

# ------------------------- GUI UPDATE LOOP ------------------------- #
def update_gui():
    # Read sensor values
    check_distance()
    read_DHT()
    check_motion()

    # Update GUI using canvas.itemconfig instead of .config
    temp_card_canvas.itemconfig(temp_val, text=f"{temp_c} °C")
    humidity_card_canvas.itemconfig(humidity_val, text=f"{humidity} %")
    distance_card_canvas.itemconfig(distance_val, text=f"{distanceDisplay} cm")
    motion_color = ACCENTS["motion"] if motion_status == "Detected" else "#98ff98"
    motion_card_canvas.itemconfig(motion_val, text=motion_status, fill=motion_color)

    window.after(500, update_gui)

window.mainloop()
