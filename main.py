import os
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime
import sys
import ctypes
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import winreg

APP_NAME = "LRP SaltyFix"
FOLDER_PATH = Path("C:/Program Files/LRPSALTYFIX")
LOG_FILE = FOLDER_PATH / "activity.log"
ICON_PATH = Path("app.ico")

DNS_GOOGLE = ["8.8.8.8", "8.8.4.4"]
DNS_CLOUDFLARE = ["1.1.1.1", "1.0.0.1"]

PRIMARY_COLOR = "#2b0169"
GLOW_COLOR = "#6600ff"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def restart_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

if not is_admin():
    restart_as_admin()

def log_action(action: str):
    try:
        FOLDER_PATH.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {action}\n")
    except Exception as e:
        try:
            messagebox.showerror("Log Fehler", f"Konnte Logdatei nicht schreiben:\n{e}")
        except Exception:
            print("Log Fehler:", e)

def get_active_adapter():
    try:
        result = subprocess.check_output("netsh interface show interface", shell=True, text=True)
        for line in result.splitlines():
            if "Connected" in line or "Verbunden" in line:
                parts = line.split()
                if len(parts) >= 4:
                    return " ".join(parts[3:])
                else:
                    return parts[-1]
    except Exception as e:
        log_action(f"Fehler Adapter finden: {e}")
    return None

def set_dns(use_cloudflare=False):
    adapter = get_active_adapter()
    if not adapter:
        messagebox.showerror("Fehler", "Kein aktiver Netzwerkadapter gefunden!")
        log_action("DNS Fehler: Kein Adapter")
        return

    dns = DNS_CLOUDFLARE if use_cloudflare else DNS_GOOGLE

    try:
        os.system(f'netsh interface ipv4 set dns name="{adapter}" static {dns[0]}')
        os.system(f'netsh interface ipv4 add dns name="{adapter}" {dns[1]} index=2')
        os.system(f'netsh interface ipv6 set dnsservers name="{adapter}" static {dns[0]}')
        os.system(f'netsh interface ipv6 add dnsservers name="{adapter}" {dns[1]} index=2')
        os.system("ipconfig /flushdns")
        messagebox.showinfo("Erfolg", f"DNS erfolgreich gesetzt ({'Cloudflare' if use_cloudflare else 'Google'}) für {adapter}")
        log_action(f"DNS gesetzt ({'Cloudflare' if use_cloudflare else 'Google'}) für Adapter: {adapter}")
    except Exception as e:
        messagebox.showerror("Fehler", str(e))
        log_action(f"Fehler DNS setzen: {e}")

def reset_dns():
    adapter = get_active_adapter()
    if not adapter:
        messagebox.showerror("Fehler", "Kein aktiver Netzwerkadapter gefunden!")
        log_action("DNS Reset Fehler: Kein Adapter")
        return
    try:
        os.system(f'netsh interface ipv4 set dnsservers name="{adapter}" source=dhcp')
        os.system(f'netsh interface ipv6 set dnsservers name="{adapter}" source=dhcp')
        os.system("ipconfig /flushdns")
        messagebox.showinfo("Zurückgesetzt", f"DNS automatisch bezogen für {adapter}")
        log_action(f"DNS zurückgesetzt für Adapter: {adapter}")
    except Exception as e:
        messagebox.showerror("Fehler", str(e))
        log_action(f"Fehler DNS Reset: {e}")

def open_website():
    webbrowser.open("https://saltyhub.net/download")
    log_action("Website geöffnet")

def get_windows_mode():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return "light" if value == 1 else "dark"
    except Exception:
        return "light"

appearance_mode = get_windows_mode()
ctk.set_appearance_mode(appearance_mode)
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title(APP_NAME)
app.geometry("480x320")
app.resizable(False, False)

if ICON_PATH.exists():
    try:
        app.iconbitmap(str(ICON_PATH))
    except Exception:
        pass

bg_color_dark = "#310375"
bg_color_light = "#f5f5f5"
bg_color = bg_color_dark if appearance_mode=="dark" else bg_color_light
canvas = tk.Canvas(app, width=480, height=320, highlightthickness=0, bg=bg_color)
canvas.place(x=0, y=0)

main_frame = ctk.CTkFrame(app, width=420, height=300, corner_radius=20,
                          fg_color="#310375", border_width=0)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

canvas.create_rectangle(0,0,480,320, fill="", outline="")
main_frame.configure(fg_color="#310375")

title_label = ctk.CTkLabel(main_frame, text="SaltyChat AutoFix",
                           font=ctk.CTkFont(size=22, weight="bold"),
                           text_color="#fff")
title_label.pack(pady=(20,20))

dns_var = ctk.StringVar(value="Google")
segmented_btn = ctk.CTkSegmentedButton(main_frame, values=["Google", "Cloudflare"],
                                       variable=dns_var,
                                       width=260,
                                       fg_color=PRIMARY_COLOR,
                                       selected_color=PRIMARY_COLOR,
                                       text_color=("white","white"),
                                       corner_radius=6)
segmented_btn.pack(pady=(0,15))

def create_glass_button(text, command):
    btn = ctk.CTkButton(main_frame, text=text,
                        width=260, height=44,
                        corner_radius=6,
                        fg_color=PRIMARY_COLOR,
                        hover_color="#6600ff",
                        text_color="white",
                        command=command)
    def on_enter(e):
        btn.configure(width=280)
    def on_leave(e):
        btn.configure(width=260)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

fix_btn = create_glass_button("🔧 DNS Fix", lambda: set_dns(use_cloudflare=(dns_var.get()=="Cloudflare")))
reset_btn = create_glass_button("♻️ DNS Zurücksetzen", reset_dns)
web_btn = create_glass_button("🌐 SaltyHub öffnen", open_website)

fix_btn.pack(pady=(5,5))
reset_btn.pack(pady=(5,5))
web_btn.pack(pady=(5,5))

info_label = ctk.CTkLabel(main_frame, text="⚠️ Programm läuft als Administrator",
                          text_color="#ff4d4d", font=ctk.CTkFont(size=10))
info_label.pack(pady=(10,0))

version_label = ctk.CTkLabel(main_frame, text="Version 1.0.6 © 2025 LightningRP all rights reserved.",
                             font=ctk.CTkFont(size=9))
version_label.pack(side="bottom", pady=(10,5))

log_action("Programm gestartet")

app.mainloop()
