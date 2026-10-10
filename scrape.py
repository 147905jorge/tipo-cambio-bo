#!/usr/bin/env python3
"""Sincroniza el tipo de cambio oficial del USD/BOB publicado por el
Banco Central de Bolivia y lo guarda en tipo-cambio.json para que
cualquier sitio lo consuma via raw.githubusercontent.com (CORS abierto)."""
import re
import json
import sys
from datetime import datetime, timezone
from urllib.request import urlopen, Request

URL = "https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php"

MESES = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12",
}


def fecha_a_iso(texto):
    m = re.match(r"(\d{1,2}) de (\w+) (\d{4})", texto.strip(), re.IGNORECASE)
    if not m:
        return None
    dia, mes_nombre, anio = m.groups()
    mes = MESES.get(mes_nombre.lower())
    if not mes:
        return None
    return f"{anio}-{mes}-{int(dia):02d}"


def main():
    req = Request(URL, headers={"User-Agent": "Mozilla/5.0 (sync-tipo-cambio-bo)"})
    with urlopen(req, timeout=20) as r:
        html = r.read().decode("utf-8", errors="ignore")

    fecha_m = re.search(r"FECHA DE LA COTIZACI[^<]*</span><strong>([^<]+)</strong>", html)
    usd_m = re.search(
        r"D&Oacute;LAR</td>\s*<td class=\"centro\">USD</td>\s*<td class=\"numero\">([\d.]+)</td>",
        html,
    )

    if not usd_m:
        print("[ERROR] No se pudo encontrar el valor del dolar en la pagina del BCB", file=sys.stderr)
        sys.exit(1)

    usd_bob = float(usd_m.group(1))
    fecha_cotizacion = fecha_a_iso(fecha_m.group(1)) if fecha_m else None

    data = {
        "usd_bob": usd_bob,
        "fecha_cotizacion": fecha_cotizacion,
        "actualizado_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fuente": "Banco Central de Bolivia (TCO)",
        "fuente_url": "https://www.bcb.gob.bo/",
    }

    with open("tipo-cambio.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] usd_bob={usd_bob} fecha_cotizacion={fecha_cotizacion}")


if __name__ == "__main__":
    main()
