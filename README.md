# Monitor de Energía y Temperatura

Script en Python que registra periódicamente CPU, RAM, temperaturas de sensores y una estimación de consumo en Watts. Guarda logs en `logs/consumo.csv` para análisis, alertas y mantenimiento preventivo.

## Tecnologías
- Python 3
- psutil
- CSV para registros

## Funcionalidades
- Lectura periódica de CPU y RAM
- Lectura de temperaturas vía `psutil.sensors_temperatures()`
- Estimación de consumo en Watts basada en uso de CPU
- Guardado periódico en `logs/consumo.csv`
- Configuración mediante `config.json`
- Plantilla opcional para ejecución como servicio systemd

## Instalación
```bash
git clone https://github.com/TU_USUARIO/Monitor-Energia-Temperatura.git
cd Monitor-Energia-Temperatura
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
## Instalación
```
Uso
- Ajusta config.json si lo deseas.
- Ejecuta:
python monitor.py


- Revisa logs/consumo.csv para ver los registros.
Estructura


Ejecutar como servicio (systemd) — resumen
- Copia systemd/monitor_energia.service a /etc/systemd/system/ y ajusta rutas y User.
- Recarga systemd:
sudo systemctl daemon-reload
sudo systemctl enable --now monitor_energia.service
sudo journalctl -u monitor_energia.service -f
