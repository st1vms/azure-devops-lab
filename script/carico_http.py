#!/usr/bin/env python3
"""Carico HTTP didattico: richieste GET di sola lettura per un tempo limitato.

Uso nel Job Kubernetes: python3 /scripts/carico_http.py http://backend:8000/api/products 120
"""
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen


def richiesta(url, fine):
    riuscite = 0
    errori = 0
    while time.monotonic() < fine:
        try:
            with urlopen(url, timeout=3) as risposta:
                risposta.read()
                riuscite += risposta.status == 200
        except Exception:
            errori += 1
    return riuscite, errori


def main():
    if len(sys.argv) != 3 or not sys.argv[2].isdigit():
        print("Uso: python3 carico_http.py URL DURATA_SECONDI")
        return 2
    url = sys.argv[1]
    durata = int(sys.argv[2])
    if durata < 10 or durata > 180:
        print("Durata consentita: 10–180 secondi")
        return 2
    fine = time.monotonic() + durata
    print(f"Carico GET verso {url} per {durata} secondi, 8 worker")
    with ThreadPoolExecutor(max_workers=8) as pool:
        risultati = list(pool.map(lambda _: richiesta(url, fine), range(8)))
    print("Risposte HTTP 200:", sum(x[0] for x in risultati))
    print("Errori di collegamento:", sum(x[1] for x in risultati))
    return 0 if sum(x[0] for x in risultati) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
