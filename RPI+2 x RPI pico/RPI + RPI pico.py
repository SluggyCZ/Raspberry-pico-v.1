from flask import Flask, render_template_string, request, redirect, url_for
import serial
import threading
import time

# === UART nastavení ===
# Pico A (tlačítko) - RX/TX na GPIO14/15
BUTTON_PICO_PORT = "/dev/serial0"  # nebo "/dev/ttyAMA0" podle konfigurace
BUTTON_BAUDRATE = 9600

# Pico B (LED) - RX/TX na GPIO17/18
LED_PICO_PORT = "/dev/serial1"  # nebo jiný port podle zapojení
LED_BAUDRATE = 9600

# Inicializace UART
button_serial = serial.Serial(BUTTON_PICO_PORT, BUTTON_BAUDRATE, timeout=0.1)
led_serial = serial.Serial(LED_PICO_PORT, LED_BAUDRATE, timeout=0.1)

# Stav LED
led_state = False
# Stav tlačítka
button_state = False

# Flask aplikace
app = Flask(__name__)

# HTML šablona
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>LED Control</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 100px; background: #222; color: white; }
        button { font-size: 22px; padding: 15px 40px; margin: 20px; border: none; border-radius: 10px; cursor: pointer; }
        .on { background-color: limegreen; }
        .off { background-color: crimson; }
    </style>
</head>
<body>
    <h1>💡 Ovládání LED</h1>
    <p>Tlačítko na Pico A je: <strong>{{ 'STISKNUTO' if button_state else 'VOLNO' }}</strong></p>
    <p>LED je: <strong>{{ 'ZAPNUTA' if led_state else 'VYPNUTA' }}</strong></p>
    <form action="/toggle" method="post">
        <button type="submit" class="{{ 'off' if led_state else 'on' }}">
            {{ 'Vypnout' if led_state else 'Zapnout' }}
        </button>
    </form>
</body>
</html>
"""

# === Funkce pro čtení tlačítka ===
def read_button():
    global button_state
    while True:
        if button_serial.in_waiting > 0:
            line = button_serial.readline().decode().strip()
            if line == "BTN:1":
                button_state = True
                # zapni LED i přes tlačítko
                send_led_command(True)
            elif line == "BTN:0":
                button_state = False
                send_led_command(False)
        time.sleep(0.05)

# === Funkce pro ovládání LED ===
def send_led_command(state):
    global led_state
    led_state = state
    cmd = "LED_ON\n" if state else "LED_OFF\n"
    led_serial.write(cmd.encode())

# === Flask routy ===
@app.route("/")
def index():
    return render_template_string(HTML, led_state=led_state, button_state=button_state)

@app.route("/toggle", methods=["POST"])
def toggle():
    send_led_command(not led_state)
    return redirect(url_for("index"))

# === Spuštění vlákna pro čtení tlačítka ===
threading.Thread(target=read_button, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
