# 🚒 Fireport Dashboard (Raspberry Pi)

Informační tabule pro hasičské zbrojnice postavená na Raspberry Pi. Systém automaticky přijímá informace o výjezdu, probudí televizi (přes HDMI CEC), zobrazí detaily události a vygeneruje dvě mapy (přehledovou a detailní) pomocí API Mapy.cz.

## ✨ Klíčové vlastnosti

* **Automatické probuzení TV:** Využívá protokol HDMI CEC pro zapnutí TV a přepnutí vstupu při poplachu.
* **Dvojitá mapa (Turistická):**
    * *Horní:* Přehledová mapa pro příjezdové cesty (Zoom 14).
    * *Dolní:* Detailní mapa místa zásahu (Zoom 19).
    * *Obě mapy využívají podklad "Outdoor" (Turistická) pro maximální čitelnost silnic a čísel popisných.*
* **Vizuální alarm:** Agresivní červené blikající upozornění ("Pop-up") při novém výjezdu.
* **Webové notifikace:** Podpora pro systémová upozornění ve Windows/prohlížeči (i na jiných PC v síti).
* **Klidový režim:** Zobrazuje hodiny a stav "PŘIPRAVEN", po nastaveném čase automaticky zhasne/přejde do klidu.

---

## 🛠 Požadavky

### Hardware
* Raspberry Pi 3B+ / 4 / 5 (doporučeno RPi 4 pro 2x HDMI).
* Televize s podporou HDMI CEC (SimpLink, Anynet+, Bravia Sync...).
* Kvalitní napájecí zdroj (pro stabilní HDMI signál).
* *(Volitelně)* HDMI Switch, pokud je TV pomalá na přepínání vstupů.

### Software
* Raspberry Pi OS (Lite verze s doinstalovaným X Serverem nebo Full verze).
* Python 3.
* Knihovny: `flask`, `requests` (pro Telegram script), `cec-utils`.

---

## 🚀 Instalace a nastavení

### 1. Příprava systému a závislostí
Aktualizujte systém a nainstalujte nástroje pro CEC a prohlížeč Chromium:

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install cec-utils chromium-browser python3-flask python3-requests --no-install-recommends
