import time
import csv
import os
from datetime import datetime
import psutil
from sensores import leer_temperatura, leer_consumo_estimado

LOG_DIR = "logs"
CSV_FILE = os.path.join(LOG_DIR, "consumo.csv")
SLEEP_SECONDS = 60  # intervalo por defecto

os.makedirs(LOG_DIR, exist_ok=True)

def obtener_datos():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    temp = leer_temperatura()
    consumo_w = leer_consumo_estimado(cpu)
    return {"cpu": cpu, "ram": ram, "temp": temp, "consumo_w": round(consumo_w, 2)}

def inicializar_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Fecha", "CPU", "RAM", "Temperatura", "Consumo_W"])

def main():
    inicializar_csv()
    print("Iniciando monitor. Presiona Ctrl+C para detener.")
    try:
        while True:
            datos = obtener_datos()
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(CSV_FILE, "a", newline="") as f:
                csv.writer(f).writerow([ahora, datos["cpu"], datos["ram"], datos["temp"], datos["consumo_w"]])
            print(f"{ahora} | CPU {datos['cpu']}% | RAM {datos['ram']}% | Temp {datos['temp']}°C | Consumo {datos['consumo_w']} W")
            time.sleep(SLEEP_SECONDS)
    except KeyboardInterrupt:
        print("Monitor detenido por usuario.")

if __name__ == "__main__":
    main()