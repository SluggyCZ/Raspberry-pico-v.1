from flask import Flask, render_template_string, redirect, url_for
import RPi.GPIO as GPIO

# Nastavení GPIO
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# Flask aplikace
app = Flask(__name__)

# Proměnná stavu LED
led_state = False

# HTML šablona přímo v kódu
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
    <h1>💡 Ovládání LED na GPIO17</h1>
    <p>LED je aktuálně: <strong>{{ 'ZAPNUTÁ' if led_state else 'VYPNUTÁ' }}</strong></p>
    <form action="/toggle" method="post">
        <button type="submit" class="{{ 'off' if led_state else 'on' }}">
            {{ 'Vypnout' if led_state else 'Zapnout' }}
        </button>
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, led_state=led_state)

@app.route("/toggle", methods=["POST"])
def toggle():
    global led_state
    led_state = not led_state
    GPIO.output(LED_PIN, GPIO.HIGH if led_state else GPIO.LOW)
    return redirect(url_for("index"))

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        GPIO.cleanup()