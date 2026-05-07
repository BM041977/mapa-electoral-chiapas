"""
Extrae las primeras 100 líneas (head + inicio del body) y las últimas 500 líneas
(donde típicamente está el <script> con la lógica del mapa) del mapa.html.

Salta toda la parte gigante del GeoJSON embebido, que es lo que infla el archivo.

Uso: pon este script en la misma carpeta que mapa.html y córrelo:
    python extraer_logica.py
"""

ARCHIVO_ENTRADA = "templates/mapa.html"   # ajusta si está en otra ruta
ARCHIVO_SALIDA = "mapa_resumen.html"
LINEAS_INICIO = 100
LINEAS_FINAL = 500

with open(ARCHIVO_ENTRADA, "r", encoding="utf-8") as f:
    lineas = f.readlines()

total = len(lineas)
print(f"Archivo original: {total:,} líneas")

inicio = "".join(lineas[:LINEAS_INICIO])
final = "".join(lineas[-LINEAS_FINAL:])

separador = f"\n\n<!-- ============================================ -->\n"
separador += f"<!-- {total - LINEAS_INICIO - LINEAS_FINAL:,} líneas de GeoJSON omitidas -->\n"
separador += f"<!-- ============================================ -->\n\n"

with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
    f.write(inicio + separador + final)

print(f"✅ Resumen guardado en: {ARCHIVO_SALIDA}")
print(f"   ({LINEAS_INICIO + LINEAS_FINAL} líneas — fácil de copiar)")
