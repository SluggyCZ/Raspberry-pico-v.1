from flask import Flask, render_template_string
import requests
import json

DB_FILE = "db.txt"

PICO_IP = "172.20.10.7"  # doplníš podle výpisu Pico

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>LED Matrix 8x8</title>
<style>
    table { margin: 20px auto; }
    td { width: 40px; height: 40px; }
    button {
        width: 40px; height: 40px;
        background: #222; color: white; border: 1px solid #555;
        cursor:pointer;
    }
    .on { background: lime; }
    .control-button {
        padding: 15px 30px; 
        margin: 10px; 
        font-size: 20px;
        border:none; 
        border-radius: 10px; 
        cursor:pointer;
    }
    .clear { background: red; color: white; }
    .save { background: blue; color: white; }
    .load { background: green; color: white; }
</style>
</head>
<body style="text-align:center; background:#111; color:white;">
<h1>LED Matrix Controller</h1>
<p>
<form method="post" action="/clear" style="display:inline;">
    <button class="control-button clear">CLEAR MATRIX</button>
</form>
<form method="post" action="/save" style="display:inline;">
    <button class="control-button save">SAVE</button>
</form>
<form method="post" action="/load" style="display:inline;">
    <button class="control-button load">LOAD</button>
</form>
</p>
<table>
{% for r in range(8) %}
<tr>
    {% for c in range(8) %}
    <td>
        <form method="post" action="/toggle/{{r}}/{{c}}">
            <button class="{{ 'on' if matrix[r][c] else '' }}"></button>
        </form>
    </td>
    {% endfor %}
</tr>
{% endfor %}
</table>
</body>
</html>
"""

matrix = [[0]*8 for _ in range(8)]

def send_to_pico(r, c, v):
    # horizontální zrcadlení
    mirrored_col = 7 - c
    url = f"http://{PICO_IP}/set/{r}/{mirrored_col}/{v}"
    try:
        requests.get(url, timeout=0.2)  # rychle timeout, aby to nečekalo moc
    except:
        pass

@app.route("/")
def index():
    return render_template_string(HTML, matrix=matrix)

@app.post("/toggle/<int:r>/<int:c>")
def toggle(r, c):
    matrix[r][c] = 0 if matrix[r][c] else 1
    send_to_pico(r, c, matrix[r][c])
    return index()

@app.post("/clear")
def clear():
    global matrix
    matrix = [[0]*8 for _ in range(8)]  # vymaže data
    # pošli všechny nuly na Pico efektivně
    for r in range(8):
        for c in range(8):
            send_to_pico(r, c, 0)
    return index()

@app.post("/save")
def save():
    global matrix
    # uloží matrix jako JSON
    with open(DB_FILE, "w") as f:
        json.dump(matrix, f)
    return index()

@app.post("/load")
def load():
    global matrix
    # clear nejdřív
    matrix = [[0]*8 for _ in range(8)]
    for r in range(8):
        for c in range(8):
            send_to_pico(r, c, 0)
    # načti z db.txt
    try:
        with open(DB_FILE, "r") as f:
            saved = json.load(f)
            matrix = saved
            # pošli do Pica
            for r in range(8):
                for c in range(8):
                    send_to_pico(r, c, matrix[r][c])
    except FileNotFoundError:
        pass
    return index()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
