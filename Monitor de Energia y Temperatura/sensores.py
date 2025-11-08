import psutil

def leer_temperatura():
    try:
        temps = psutil.sensors_temperatures()
        # 'coretemp' es común en Linux; adaptar según plataforma
        for key in temps:
            if temps[key]:
                return temps[key][0].current
        return None
    except Exception:
        return None

def leer_consumo_estimado(cpu_percent):
    # Estimación sencilla: consumo relativo (0-100) -> Watts aproximados
    # Ajusta según el equipo real si dispones de mediciones
    base_watts = 30
    max_watts = 95
    return base_watts + (max_watts - base_watts) * (cpu_percent / 100.0)