from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    cevap = None
    if request.method == "POST":
        stres = request.form.get("stres")
        duygu_durumu = request.form.get("duygu_durumu")

        url = "https://yapayzekaodev.app.n8n.cloud/webhook/stres-veri"
        try:
            response = requests.post(url, json={
                "stres": int(stres),
                "duygu_durumu": duygu_durumu
            })

            print("Gelen cevap (raw):", response.text)

            if response.ok:
                json_cevap = response.json()
                if isinstance(json_cevap, list):
                    json_cevap = json_cevap[0]
                cevap_raw = json_cevap.get("ai_cevabi", "Cevap alınamadı.")
                cevap = str(cevap_raw).strip().removeprefix("{").removesuffix("}")
            else:
                cevap = f"Hata: {response.status_code} - {response.text}"

        except Exception as e:
            cevap = f"İstek başarısız: {str(e)}"

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Stres Botu</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: #f0f2f5;
                color: #333;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 40px;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 500px;
            }
            h2 {
                color: #4A90E2;
                margin-bottom: 20px;
                text-align: center;
            }
            label {
                display: block;
                margin: 12px 0 4px;
            }
            input[type="number"], input[type="text"] {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
            input[type="submit"] {
                margin-top: 20px;
                padding: 10px 16px;
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                width: 100%;
            }
            input[type="submit"]:hover {
                background-color: #357ABD;
            }
            .response {
                margin-top: 30px;
                background: #e6f2ff;
                padding: 15px;
                border-left: 5px solid #4A90E2;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Stres ve Duygu Bilgisi Gönder</h2>
            <form method="post">
                <label for="stres">Stres Seviyesi (1-10):</label>
                <input type="number" name="stres" id="stres" required>

                <label for="duygu_durumu">Duygu Durumu:</label>
                <input type="text" name="duygu_durumu" id="duygu_durumu" required>

                <input type="submit" value="Gönder">
            </form>

            {% if cevap %}
            <div class="response">
                <strong>AI Cevabı:</strong>
                <p>{{ cevap }}</p>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    ''', cevap=cevap)

if __name__ == "__main__":
    app.run(debug=True)
