import psutil

def leer_temperatura(sensor_priority=None):
    """
    Devuelve temperatura en grados Celsius si está disponible, sino None.
    sensor_priority: lista opcional de nombres de sensores preferidos.
    """
    try:
        temps = psutil.sensors_temperatures()
    except Exception:
        return None

    if not temps:
        return None

    if sensor_priority:
        for key in sensor_priority:
            if key in temps and temps[key]:
                return _first_current(temps[key])

    # Si no hay prioridad, devolver la primera temperatura disponible
    for key in temps:
        if temps[key]:
            return _first_current(temps[key])
    return None

def _first_current(entries):
    for e in entries:
        if hasattr(e, "current"):
            return getattr(e, "current")
        # compatibilidad con namedtuple distinto
        try:
            return e.current
        except Exception:
            continue
    return None

def leer_consumo_estimado(cpu_percent, base_watts=30, max_watts=95):
    """
    Estimación simple del consumo en Watts en función del uso de CPU.
    Ajusta base_watts/max_watts según mediciones reales del equipo.
    """
    try:
        cpu = float(cpu_percent)
    except (ValueError, TypeError):
        cpu = 0.0
    consumo = base_watts + (max_watts - base_watts) * (cpu / 100.0)
    return consumo