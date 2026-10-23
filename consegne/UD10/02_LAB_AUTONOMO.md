# UD10 — Consegna laboratorio autonomo

## Baseline

- compose ps:

```bash
NAME                           IMAGE                                     COMMAND                  SERVICE    CREATED         STATUS         PORTS
catalogo-prodotti-backend-1    localhost/catalog-backend:ud10            "python /app/server.…"   backend    2 minutes ago   Up 2 minutes   8000/tcp
catalogo-prodotti-frontend-1   docker.io/library/catalog-frontend:ud10   "nginx -g daemon off;"   frontend   2 minutes ago   Up 2 minutes   127.0.0.1:8080->80/t
```

- health:

```bash
HTTP/1.1 200 OK
Server: nginx/1.31.8
Date: Fri, 23 Oct 2026 13:08:29 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 72
Connection: keep-alive

{
  "status": "ok",
  "service": "catalog-backend",
  "version": "2.0"
}
```

## Errore

- variabile: `LOW_STOCK_THRESHOLD`
- valore errato: `"not-a-number"`
- stato backend: `Exited`
- log/errore:

```txt
backend-1  | Traceback (most recent call last):
backend-1  |   File "/app/server.py", line 21, in read_int_env
backend-1  |     return int(raw)
backend-1  | ValueError: invalid literal for int() with base 10: 'not-a-number'
backend-1  |
backend-1  | The above exception was the direct cause of the following exception:
backend-1  |
backend-1  | Traceback (most recent call last):
backend-1  |   File "/app/server.py", line 28, in <module>
backend-1  |     LOW_STOCK_THRESHOLD = read_int_env("LOW_STOCK_THRESHOLD", 5)
backend-1  |   File "/app/server.py", line 23, in read_int_env
backend-1  |     raise ValueError(f"{name} deve essere un intero, ricevuto: {raw!r}") from exc
backend-1  | ValueError: LOW_STOCK_THRESHOLD deve essere un intero, ricevuto: 'not-a-number'
```

## Diagnosi

- Sintomo: Il comando `docker compose up -d` ritorna Errore
- Risultato atteso: Il container del backend dovrebbe ripartire.
- Evidenza: Logs estrapolati con `docker compose logs --tail 50 backend` mostrano un errore ValueError relativo alla variabile di configurazione `LOW_STOCK_TRESHOLD`.
- Ipotesi: La variabile `LOW_STOCK_TRESHOLD` contiene un valore invalido.
- Causa: Il valore assegnato alla variabile è una stringa che non si traduce in nessun numero (`not-a-number`).

## Fix

- modifica minima: Ripristinare `LOW_STOCK_TRESHOLD` al valore numerico di default `5`.
- rebuild necessario?: No
- motivazione: La configurazine riguarda la composizione delle immagini, non la build dell'immagine.

## Test

- backend healthy: Yes
- health: `200`
- products: `200`
- browser: `200`

## Modifica conservata

- APP_ENV: `local-docker`
- compose config: Mostra la modifica
- test: Successo.

*Nota: il comando `docker compose up -d` dopo aver ricreato il backend non aggiorna l'indirizzo ip che il frontend utilizza per contattare il backend. Questo accade solo con podman a quanto pare, ed è necessario riavviare il frontend manualmente.*

## Git

- branch: `fix/ud10-invalid-treshold`
- commit: `fix: validate Docker runtime configuration`
- PR: `UD10: validate Docker runtime configuration`
- diff verificato: Si
- merge: Effettuato

## Passaggio alla verifica

- stack mantenuto attivo: si
