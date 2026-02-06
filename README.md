Informační tabule pro hasičské zbrojnice postavená na Raspberry Pi. Systém automaticky přijímá informace o výjezdu, probudí televizi (přes HDMI CEC), zobrazí detaily události a vygeneruje dvě mapy (přehledovou a detailní) pomocí API Mapy.cz.

✨ Klíčové vlastnosti
Automatické probuzení TV: Využívá protokol HDMI CEC pro zapnutí TV a přepnutí vstupu při poplachu.

Dvojitá mapa (Turistická):

Horní: Přehledová mapa pro příjezdové cesty (Zoom 14).

Dolní: Detailní mapa místa zásahu (Zoom 19).

Obě mapy využívají podklad "Outdoor" (Turistická) pro maximální čitelnost silnic a čísel popisných.

Vizuální alarm: Agresivní červené blikající upozornění ("Pop-up") při novém výjezdu.

Webové notifikace: Podpora pro systémová upozornění ve Windows/prohlížeči (i na jiných PC v síti).

Klidový režim: Zobrazuje hodiny a stav "PŘIPRAVEN", po nastaveném čase automaticky zhasne/přejde do klidu.

🛠 Požadavky
Hardware
Raspberry Pi 3B+ / 4 / 5 (doporučeno RPi 4 pro 2x HDMI).

Televize s podporou HDMI CEC (SimpLink, Anynet+, Bravia Sync...).

Kvalitní napájecí zdroj (pro stabilní HDMI signál).

(Volitelně) HDMI Switch, pokud je TV pomalá na přepínání vstupů.

Software
Raspberry Pi OS (Lite verze s doinstalovaným X Serverem nebo Full verze).

Python 3.

Knihovny: flask, requests (pro Telegram script), cec-utils.

🚀 Instalace a nastavení
1. Příprava systému a závislostí
Aktualizujte systém a nainstalujte nástroje pro CEC a prohlížeč Chromium:

Bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install cec-utils chromium-browser python3-flask python3-requests --no-install-recommends
Pokud používáte Lite verzi OS (bez desktopu), doinstalujte grafický server:

Bash
sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox
2. Stažení projektu
Nahrajte soubory do složky /home/pi/fireport-dashboard. Struktura složek musí vypadat takto:

Plaintext
/home/pi/
├── server.py              # Hlavní backend (Flask)
├── telegram_listener.py   # Skript pro příjem zpráv (Telethon)
└── templates/
    └── index.html         # Frontend (vzhled dashboardu)
3. Konfigurace Mapy.cz API
Pro funkčnost map je nutné mít API klíč od Seznamu.

Jděte na Mapy.cz Developer.

Vytvořte projekt a API klíč.

DŮLEŽITÉ: V nastavení klíče povolte "Záměrně nezabezpečený API klíč" (protože RPi nemá veřejnou doménu).

Otevřete server.py a vložte klíč:

Python
MAPY_CZ_API_KEY = "vložte_váš_dlouhý_klíč_zde"
⚙️ Automatické spouštění (Systemd)
Aby dashboard běžel na pozadí a naběhl po výpadku proudu, vytvořte službu.

1. Služba pro Backend (Flask)
Vytvořte soubor: sudo nano /etc/systemd/system/fireport.service

Ini, TOML
[Unit]
Description=Fireport Dashboard Server
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /home/pi/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
Povolte službu:

Bash
sudo systemctl enable fireport.service
sudo systemctl start fireport.service
2. Autostart prohlížeče (Kiosk mód)
Upravte autostart soubor grafického prostředí: sudo nano /etc/xdg/lxsession/LXDE-pi/autostart (cesta se může lišit dle verze OS).

Přidejte na konec:

Bash
@xset s off
@xset -dpms
@xset s noblank
@chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:5000
🔔 Nastavení notifikací (PC/Windows)
Pokud máte dashboard otevřený na počítači v síti (např. v kanceláři velitele) a chcete dostávat systémová upozornění:

Otevřete v prohlížeči IP adresu RPi (např. http://192.168.1.50:5000).

Klikněte na tlačítko "🔔 Povolit upozornění ve Windows".

POZOR: Pokud Chrome blokuje notifikace (protože web neběží na HTTPS), musíte povolit výjimku:

Do adresního řádku napište: chrome://flags/#unsafely-treat-insecure-origin-as-secure

Povolte tuto volbu (Enabled).

Do pole vložte adresu RPi: http://192.168.1.50:5000

Restartujte Chrome.

📡 Integrace dat (Telegram / Fireport)
Data do dashboardu se posílají pomocí HTTP POST požadavku. Formát JSON:

JSON
{
  "fireport": "poplach",
  "kategorie": "POŽÁR, LESNÍ POROST",
  "lokace": "Hrádek nad Nisou, U Koupaliště",
  "dopres": "Hoří tráva 50x50m | Oznamovatel na místě",
  "tech": "CAS 20, CAS 30",
  "gps_lat": "50.853561",
  "gps_lon": "14.826439"
}
🖕 Poděkování (a stížnosti)
Speciální "poděkování" patří Matymu.

Děkuji mu za jeho neutuchající proud "geniálních nápadů" a vět začínajících slovy "Hele a nešlo by tam ještě...". Díky jeho kreativitě se projekt, který mohl být hotový za jedno odpoledne, protáhl na několik týdnů ladění detailů, překopávání map a řešení pixelů.

Maty, bez tebe by to bylo hotové dřív a já bych se vyspal. Ale aspoň to teď vypadá k světu. Díky (asi). 💩
