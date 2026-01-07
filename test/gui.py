import tkinter as tk

# ------------------------- GUI SETUP ------------------------- #
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

def create_card(parent, title_text, fg_color, width=140, height=110, radius=12):
    canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0, bg=WINDOW_BG)
    x1, y1, x2, y2 = 4, 4, width - 4, height - 4
    r = radius
    # Draw rounded rectangle background
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

window.mainloop()