# 🎧 SaltyChat Fixer Tool (LRP SaltyFix)

Ein einfaches Python-Tool, das häufige DNS-Probleme behebt, die bei der Nutzung von **SaltyChat** (z. B. in FiveM oder AltV) auftreten können.  
Das Tool bietet eine moderne Benutzeroberfläche, automatisierte Admin-Rechte, DNS-Wechsel (Google oder Cloudflare) und eine integrierte Reset-Funktion.

---

## 🚀 Features

- 🧠 **Automatische DNS-Reparatur** (Google oder Cloudflare)
- 🔄 **DNS-Reset auf DHCP**
- 🌐 **Direkter Zugriff auf [SaltyHub.net](https://saltyhub.net/download)**
- 🪟 **Automatischer Dark-/Lightmode je nach Windows-Thema**
- 🧰 **Läuft automatisch als Administrator**
- 🪞 **Modernes UI (CustomTkinter + Glass-Design)**
- 🧾 **Logging aller Aktionen (`activity.log`)**
- 🧱 **Saubere portable Build-Unterstützung über `PyInstaller`**

---

## 🧩 Voraussetzungen

- **Python** (empfohlen: `3.12.10` oder neuer)
- **Windows-Betriebssystem**
- **Administratorrechte erforderlich**
- Optional: `pip install customtkinter`

---

## ⚙️ Installation & Nutzung

### 🔹 Variante 1 – Portable EXE (empfohlen)

Lade dir die neueste Version herunter:  
👉 [**Release-Seite auf GitHub**](https://github.com/dreimalneunundsechzig/saltychat-fixer-tool/releases)

1. `saltychat-fixer-tool.exe` herunterladen  
2. Als Administrator starten  
3. Wähle deinen bevorzugten DNS (Google oder Cloudflare)  
4. Klicke auf **🔧 DNS Fix**  
5. Optional: Zurücksetzen mit **♻️ DNS Zurücksetzen**

---

### 🔹 Variante 2 – Manuell mit Python starten

```bash
git clone https://github.com/dreimalneunundsechzig/saltychat-fixer-tool.git
cd saltychat-fixer-tool
pip install customtkinter
python main.py
