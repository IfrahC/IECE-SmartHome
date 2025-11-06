from guizero import App, Text, Box
from gpiozero import LED, Button, PWMLED
from signal import pause

BG_COLOR = "#b9dbf9"

app = App(title="Project", bg=BG_COLOR, width=480, height=220)

label_color = "#0b2a47"
value_color = "#09213a"
label_size = 16
value_size = 16

top_spacer = Box(app, height=20)
container = Box(app, layout="grid")

Text(container, text="Humidity", grid=[0, 1], align="left", size=label_size, color=label_color)
humidity_val = Text(container, text="0%", grid=[1, 1], align="right", size=value_size, color=value_color)

Text(container, text="Gate Status", grid=[0, 2], align="left", size=label_size, color=label_color)
gateStatus = Text(container, text="Closed", grid=[1, 2], align="right", size=value_size, color=value_color)

Text(container, text="PIR Status", grid=[0, 3], align="left", size=label_size, color=label_color)
pirStatus = Text(container, text="No Motion", grid=[1, 3], align="right", size=value_size, color=value_color)

app.display()