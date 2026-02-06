import subprocess
import time
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# --- KONFIGURACE ---
TIMEOUT_SEKUND = 1200 #20 min 
MAPY_CZ_API_KEY = "API"

stav = {
    "aktivni": False,
    "last_update": 0,
    "typ": "",
    "adresa": "",
    "popis": "",
    "technika": "",
    "mapa_overview": "", # URL pro horní mapu
    "mapa_detail": ""    # URL pro spodní mapu
}

def probudit_tv():
    try:
        subprocess.run('echo "on 0" | cec-client -s -d 1', shell=True) #mozno odstrnit "as" probouzi pres HDMI cec
        subprocess.run('echo "as" | cec-client -s -d 1', shell=True)
    except:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/novy-vyjezd', methods=['POST'])
def trigger_alarm():
    data = request.json
    if not data: return jsonify({"status": "error"}), 400

    lat = data.get('gps_lat', '')
    lon = data.get('gps_lon', '')
    kategorie = data.get('kategorie', '')

    url_overview = ""
    url_detail = ""

    if lat and lon: 
        # 1. HORNÍ MAPA
        url_overview = (
            f"https://api.mapy.cz/v1/static/map"
            f"?apikey={MAPY_CZ_API_KEY}"
            f"&lon={lon}&lat={lat}"
            f"&zoom=14"
            f"&width=800&height=500"
            f"&mapset=outdoor"
            f"&markers=color:red;size:normal;{lon},{lat}"
        )

        # 2. SPODNÍ MAPA
        url_detail = (
            f"https://api.mapy.cz/v1/static/map"
            f"?apikey={MAPY_CZ_API_KEY}"
            f"&lon={lon}&lat={lat}"
            f"&zoom=18"
            f"&width=800&height=500"
            f"&mapset=outdoor"
            f"&markers=color:red;size:normal;{lon},{lat}"
        )
        

    global stav
    stav = {
        "aktivni": True,
        "last_update": time.time(),
        "typ": kategorie,
        "adresa": data.get('lokace', ''),
        "popis": data.get('dopres', ''),
        "technika": data.get('tech', ''),
        "mapa_overview": url_overview,
        "mapa_detail": url_detail
    }
    
    if data.get('fireport') == 'poplach':
        probudit_tv()

    return jsonify({"status": "success"})

@app.route('/status')
def get_status():
    global stav
    if stav["aktivni"] and (time.time() - stav["last_update"] > TIMEOUT_SEKUND):
        stav["aktivni"] = False
    return jsonify(stav)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)