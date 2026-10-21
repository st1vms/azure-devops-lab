# UD08 — Consegna laboratorio guidato

## Repository

- repository: `azure-devops-lab`
- branch principale: `master`
- `gh auth status` verificato: Si
- working tree iniziale pulito: Si

## Collaborazione ricevuta sul mio repository

- collaborator: `simonesalvi06-spec`
- invito accettato: Si
- branch contributor: `feature/ud08-collab-simonesalvi06-spec`
- numero PR: `#1`
- URL PR: `https://github.com/st1vms/azure-devops-lab/pull/1`
- prima review: Confermata
- modifica richiesta: `Aggiungi una sezione "## Esito" con la frase:
Review completata e modifica corretta.`
- nuovo commit: `79a84e2a87e889154e3092e6b79ffd7e21ae315f`
- approvazione/commento finale: "Approvato"
- merge: Confermato
- branch remota eliminata: Si
- collaboratore rimosso: Si

## Collaborazione eseguita sul repository altrui

- repository: `azure-devops-lab`
- branch: `feature/ud08-collab-st1vms`
- numero PR: `#1`
- prima review ricevuta: Si
- correzione eseguita: Si
- merge completato: Si

## Conflitto locale

- branch A: `lab/conflict-a`
- branch B: `lab/conflict-b`
- file: `ud08-conflict.txt`
- marker osservati: `PORT=7000 | PORT=9000`
- contenuto finale scelto: `PORT=8000`
- commit risoluzione: `dc22c5d5104b99974be09472e260014098b5ebcf`
- cleanup completato: Si

## Catalogo prodotti

- server avviato: Si
- `/health`:

```bash
$ curl -i http://127.0.0.1:8000/health
HTTP/1.0 200 OK
Server: CatalogoProdotti/1.0 Python/3.14.4
Date: Wed, 21 Oct 2026 12:15:16 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 74

{
  "status": "ok",
  "service": "catalogo-prodotti",
  "version": "1.0"
}
```

- `/api/products`:

```bash
$ curl -s http://127.0.0.1:8000/api/products | python3 -m json.tooll
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

- `/api/products/P001`:

```bash
$ curl -i http://127.0.0.1:8000/api/products/P001
HTTP/1.0 200 OK
Server: CatalogoProdotti/1.0 Python/3.14.4
Date: Wed, 21 Oct 2026 12:16:28 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 130

{
  "id": "P001",
  "name": "Notebook Pro 14",
  "category": "Notebook",
  "price": 1299.0,
  "stock": 8,
  "stock_status": "OK"
}
```

- `/api/products/XXX`:

```bash
$ curl -i http://127.0.0.1:8000/api/products/XXX
HTTP/1.0 404 Not Found
Server: CatalogoProdotti/1.0 Python/3.14.4
Date: Wed, 21 Oct 2026 12:17:19 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 57

{
  "error": "product_not_found",
  "product_id": "XXX"
}
```

- frontend browser: Funzionante
- prodotti restituiti:

```tsv
ID Prodotto Categoria Prezzo Stock Stato
P001 Notebook Pro 14 Notebook € 1299.00 8 OK
P002 Monitor 27 UHD Monitor € 349.00 4 LOW
P003 Dock USB-C Accessori € 119.00 15 OK
P004 Keyboard Business Accessori € 59.00 2 LOW
```

- prodotto LOW: `P002` e `P004`

## Architettura

- frontend: HTML/JS/CSS
- backend/API: Python http.server
- configurazione:

```json
{
  "host": "127.0.0.1",
  "port": 8000,
  "api_prefix": "/api",
  "low_stock_threshold": 5
}
```

- dati:

```json
[
  {
    "id": "P001",
    "name": "Notebook Pro 14",
    "category": "Notebook",
    "price": 1299.0,
    "stock": 8
  },
  {
    "id": "P002",
    "name": "Monitor 27 UHD",
    "category": "Monitor",
    "price": 349.0,
    "stock": 4
  },
  {
    "id": "P003",
    "name": "Dock USB-C",
    "category": "Accessori",
    "price": 119.0,
    "stock": 15
  },
  {
    "id": "P004",
    "name": "Keyboard Business",
    "category": "Accessori",
    "price": 59.0,
    "stock": 2
  }
]

```

- endpoint: `http://127.0.0.1:8000/api`

## Baseline Git

- commit: `dc22c5d5104b99974be09472e260014098b5ebcf`
- push/PR: Effettuate
- stato finale main: nessuna modifica
