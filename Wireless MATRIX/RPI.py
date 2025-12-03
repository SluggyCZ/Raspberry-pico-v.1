from flask import Flask, render_template_string
import requests

PICO_IP = "172.20.10.7"  # doplníš podle výpisu Pico

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>LED Matrix 8x8</title>
<style>
    table { margin: 30px auto; }
    td { width: 40px; height: 40px; }
    button {
        width: 40px; height: 40px;
        background: #222; color: white; border: 1px solid #555;
    }
    .on { background: lime; }
</style>
</head>
<body style="text-align:center; background:#111; color:white;">
<h1>LED Matrix Controller</h1>
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
    # Horizontální zrcadlení: sloupec 0 ↔ 7
    mirrored_col = 7 - c
    url = f"http://{PICO_IP}/set/{r}/{mirrored_col}/{v}"
    requests.get(url)

@app.route("/")
def index():
    return render_template_string(HTML, matrix=matrix)

@app.post("/toggle/<int:r>/<int:c>")
def toggle(r, c):
    matrix[r][c] = 0 if matrix[r][c] else 1
    send_to_pico(r, c, matrix[r][c])
    return index()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
