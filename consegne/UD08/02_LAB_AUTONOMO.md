# UD08 — Consegna laboratorio autonomo

## Baseline

- health:

```bash
$ curl -i http://127.0.0.1:8000/health
HTTP/1.0 200 OK
Server: CatalogoProdotti/1.0 Python/3.14.4
Date: Wed, 21 Oct 2026 13:52:44 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 74

{
  "status": "ok",
  "service": "catalogo-prodotti",
  "version": "1.0"
}
```

- products:

```bash
$curl -s http://127.0.0.1:8000/api/products | python3 -m json.tooll
{
    "count": 4,
    "products": [
        {
            "id": "P001",
            "name": "Notebook Pro 14",
            "category": "Notebook",
            "price": 1299.0,
            "stock": 8,
            "stock_status": "OK"
        },
        {
            "id": "P002",
            "name": "Monitor 27 UHD",
            "category": "Monitor",
            "price": 349.0,
            "stock": 4,
            "stock_status": "LOW"
        },
        {
            "id": "P003",
            "name": "Dock USB-C",
            "category": "Accessori",
            "price": 119.0,
            "stock": 15,
            "stock_status": "OK"
        },
        {
            "id": "P004",
            "name": "Keyboard Business",
            "category": "Accessori",
            "price": 59.0,
            "stock": 2,
            "stock_status": "LOW"
        }
    ]
}
```

## Errore introdotto

- configurazione modificata: `prefix`
- endpoint funzionante: `http://127.0.0.1:8000/api-v2/products`
- endpoint non funzionante: `http://127.0.0.1:8000/api/products`
- comportamento frontend: I prodotti non caricano, con messaggio di errore 404.

## Diagnosi

1. Si
2. Si
3. `/api-v2/products`
4. `/api/products`
5. `configurazione non applicata correttamente`

## Fix

- causa: Configurazione non compatibile
- fix: Ripristinare il vecchio prefisso
- environment aggiunto: Si

## Test finali

- `/health`: `200`
- `/api/products`: `200`
- `/api/products/P001`: `200`
- `/api/products/XXX`: `404`
- browser: `200`

## Git

- branch: `fix/ud08-api-prefix`
- `git diff` verificato: Si
- commit: Effettuato
- push: Effettuato
- PR: Effettuata
- `gh pr diff` verificato: Si
- merge: Effettuato
- main sincronizzata: Si

## Distinzione

- review collaborativa: review reale
- auto-verifica PR individuale: auto-verifica del diff
