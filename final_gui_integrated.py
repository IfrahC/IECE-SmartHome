import threading
import time
import random
import tkinter as tk
from gpiozero import Servo, DistanceSensor, LED, MotionSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import board
import adafruit_dht

# ============================
#  HARDWARE INITIALIZATION
# ============================

factory = PiGPIOFactory()

# LEDs + relay
led1 = LED(9)
relay = LED(19)
led2 = LED(3)
led1.on()
led2.off()

# PIR
pir = MotionSensor(6, pin_factory=factory)

# Servo
servo = Servo(13, pin_factory=factory, min_pulse_width=0.001, max_pulse_width=0.002)
servo.min()

# Ultrasonic
sensor = DistanceSensor(echo=27, trigger=17, max_distance=1.5, pin_factory=factory)

# DHT11
dht_device = adafruit_dht.DHT11(board.D22)

# State variables
gateOpen = False
distanceDisplay = "--"
tempDisplay = "--"
humidityDisplay = "--"
motionDisplay = "--"

# ============================
#  SENSOR FUNCTIONS
# ============================

def detected():
    global gateOpen
    if not gateOpen:
        gateOpen = True
        led1.on()
        led2.off()
        servo.max()
        sleep(2)
        relay.on()

def not_detected():
    global gateOpen
    if gateOpen:
        gateOpen = False
        led1.off()
        led2.on()
        servo.min()
        sleep(3)
        relay.off()

def read_distance():
    global distanceDisplay
    dist = sensor.distance * 100
    distanceDisplay = f"{dist:.1f}"
    if dist > 40:
        not_detected()
    else:
        detected()

def read_dht():
    global tempDisplay, humidityDisplay
    try:
        temp_c = dht_device.temperature
        humidity = dht_device.humidity
        if temp_c is not None:
            tempDisplay = f"{temp_c:.1f}"
            humidityDisplay = f"{humidity}"
    except Exception:
        tempDisplay = "--"
        humidityDisplay = "--"

def read_pir():
    global motionDisplay
    motionDisplay = "Detected" if pir.motion_detected else "None"

# ============================
#  BACKGROUND THREAD LOOP
# ============================

def sensor_loop():
    while True:
        read_distance()
        read_dht()
        read_pir()
        time.sleep(0.5)

threading.Thread(target=sensor_loop, daemon=True).start()

# ============================
#          GUI
# ============================

# Palette
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

# GUI window
window = tk.Tk()
window.title("Smart Sensor Dashboard")
window.geometry("650x260")
window.configure(bg=WINDOW_BG)

title = tk.Label(window, text="Live Sensor Dashboard", font=TITLE_FONT, fg=TITLE_FG, bg=WINDOW_BG)
title.pack(pady=(12, 2))
subtitle = tk.Label(window, text="Real-time readings from Raspberry Pi sensors", font=LABEL_FONT, fg=SUBTITLE_FG, bg=WINDOW_BG)
subtitle.pack(pady=(0, 12))

# Card creator
def create_card(parent, title_text, fg_color, width=140, height=110, radius=12):
    canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0, bg=WINDOW_BG)

    x1, y1, x2, y2 = 4, 4, width - 4, height - 4
    r = radius

    rect1 = canvas.create_rectangle(x1+r, y1, x2-r, y2, fill=CARD_BG, outline="")
    rect2 = canvas.create_rectangle(x1, y1+r, x2, y2-r, fill=CARD_BG, outline="")
    arc_parts = [
        canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, fill=CARD_BG, outline=""),
        canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, fill=CARD_BG, outline=""),
        canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, fill=CARD_BG, outline=""),
        canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, fill=CARD_BG, outline=""),
    ]
    bg_parts = [rect1, rect2] + arc_parts

    title_id = canvas.create_text(width//2, 20, text=title_text, font=LABEL_FONT, fill="#cbd7ea")
    value_id = canvas.create_text(width//2, height//2+6, text="--", font=VALUE_FONT, fill=fg_color)
    divider = canvas.create_rectangle(8, height//2-24, width-8, height//2-22, fill="#173248", outline="")

    def on_enter(e):
        for x in bg_parts: canvas.itemconfig(x, fill=CARD_HOVER)
    def on_leave(e):
        for x in bg_parts: canvas.itemconfig(x, fill=CARD_BG)

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)

    return canvas, value_id

cards = tk.Frame(window, bg=WINDOW_BG)
cards.pack()

temp_card, temp_val = create_card(cards, "Temperature", ACCENTS["temp"])
humidity_card, humidity_val = create_card(cards, "Humidity", ACCENTS["humidity"])
distance_card, distance_val = create_card(cards, "Distance", ACCENTS["distance"])
motion_card, motion_val = create_card(cards, "Motion", ACCENTS["motion"])

temp_card.grid(row=0, column=0, padx=10)
humidity_card.grid(row=0, column=1, padx=10)
distance_card.grid(row=0, column=2, padx=10)
motion_card.grid(row=0, column=3, padx=10)

# Update GUI continuously
def update_gui():
    temp_val.config(text=f"{tempDisplay} °C")
    humidity_val.config(text=f"{humidityDisplay} %")
    distance_val.config(text=f"{distanceDisplay} cm")
    motion_val.config(
        text=motionDisplay,
        fill=ACCENTS["motion"] if motionDisplay == "Detected" else "#98ff98"
    )
    window.after(300, update_gui)

update_gui()
window.mainloop()
