import time
import csv
import os
import json
from datetime import datetime
from sensores import leer_temperatura, leer_consumo_estimado

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
CSV_FILE = os.path.join(LOG_DIR, "consumo.csv")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {
    "interval_seconds": 60,
    "temperature_sensor_priority": ["coretemp", "acpitz"],
    "log_dir": "logs",
    "write_header": True
}

def cargar_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        cfg = DEFAULT_CONFIG
    # Merge defaults
    for k, v in DEFAULT_CONFIG.items():
        cfg.setdefault(k, v)
    return cfg

def inicializar_csv(path, write_header=True):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["Fecha", "CPU", "RAM", "Temperatura_C", "Consumo_W"])

def obtener_metricas():
    # Import here to avoid heavy import on module import if not needed
    import psutil
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    temp = leer_temperatura()
    consumo = leer_consumo_estimado(cpu)
    return {"cpu": cpu, "ram": ram, "temp": temp, "consumo_w": round(consumo, 2)}

def main():
    cfg = cargar_config()
    interval = cfg.get("interval_seconds", 60)
    write_header = cfg.get("write_header", True)
    inicializar_csv(CSV_FILE, write_header=write_header)
    print(f"Iniciando monitor. Intervalo: {interval}s. Logs: {CSV_FILE}")
    try:
        while True:
            datos = obtener_metricas()
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([ahora, datos["cpu"], datos["ram"], datos["temp"], datos["consumo_w"]])
            print(f"{ahora} | CPU: {datos['cpu']}% | RAM: {datos['ram']}% | Temp: {datos['temp']}°C | Consumo: {datos['consumo_w']} W")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Monitor detenido por usuario.")

if __name__ == "__main__":
    main()