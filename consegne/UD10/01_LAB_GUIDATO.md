# UD10 — Consegna laboratorio guidato

*Nota: ho usato podman al posto di docker; creando un `alias docker=podman`, tutti i comandi che utilizzano `docker` richiamano `podman` in realtà.*

## Preflight

- `docker version`:

```bash
$ docker version
Client:        Podman Engine
Version:       5.8.3
API Version:   5.8.3
Go Version:    go1.26.4-X:nodwarf5
Git Commit:    93dbfd0d86ee57f8f91801f61ce57dd880a4725f
Built:         Fri Jun 12 02:00:00 2026
Build Origin:  Fedora Project
OS/Arch:       linux/amd64
```

- `docker compose version`:
```Docker Compose version v5.6.1```

- daemon: Funzionante

- Docker da WSL2: NO

- Self-hosted future Docker readiness: OK

- RESULT: Docker configurato

## Build backend

- image: `catalog-backend`
- tag: `ud10`
- build context: `/app/catalogo-prodotti` (nel build file `.`)
- Dockerfile: `docker/backend.Dockerfile`
- layer/history osservati:

```bash
FROM
WORKDIR
COPY
RUN
USER
ENV
EXPOSE
CMD
COMMIT
```

## Container singolo

- nome: `catalog-backend-ud10`
- porta: `8000`
- health:

```bash
$ curl -i http://127.0.0.1:8000/health
HTTP/1.0 200 OK
Server: CatalogBackend/2.0 Python/3.13.17
Date: Fri, 23 Oct 2026 10:14:48 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 72

{
  "status": "ok",
  "service": "catalog-backend",
  "version": "2.0"
}
```

- products:

```bash
$ curl -s http://127.0.0.1:8000/api/products | python3 -m json.tool
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

- log:

```bash
Catalog backend listening on http://0.0.0.0:8000 threshold=5 runtime=/runtime
```

- environment verificato: Si

## Compose

- backend:

```yaml
backend:
    environment:
      APP_PORT: "8000"
      LOW_STOCK_THRESHOLD: "5"
      RUNTIME_DIR: /runtime
    image: catalog-backend:ud10
    networks:
      catalog-net: null
    volumes:
      - type: volume
        source: catalog-runtime
        target: /runtime
        volume: {}
    build:
      context: /var/home/user/Scrivania/workspace/azure-devops-lab/app/catalogo-prodotti
      dockerfile: docker/backend.Dockerfile
    expose:
      - "8000"
    healthcheck:
      test:
        - CMD
        - python
        - -c
        - import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health',
          timeout=2)
      timeout: 3s
      interval: 5s
      retries: 10
      start_period: 3s
```

- frontend:

```yaml
frontend:
    image: catalog-frontend:ud10
    networks:
      catalog-net: null
    build:
      context: /var/home/user/Scrivania/workspace/azure-devops-lab/app/catalogo-prodotti
      dockerfile: docker/frontend.Dockerfile
    depends_on:
      backend:
        condition: service_healthy
        required: true
    ports:
      - mode: ingress
        host_ip: 127.0.0.1
        target: 80
        published: "8080"
        protocol: tcp
```

- rete:

```bash
networks:
  catalog-net:
    name: catalogo-prodotti_catalog-net
    driver: bridge
```

- volume:

```bash
backend:
    ...
    volumes:
      - type: volume
        source: catalog-runtime
        target: /runtime
        volume: {}
...
volumes:
  catalog-runtime:
    name: catalogo-prodotti_catalog-runtime
```

- frontend URL: `http://127.0.0.1:8080/`
- backend healthy: Si
- `/health`:

```
$ curl -i http://127.0.0.1:8080/health
HTTP/1.1 200 OK
Server: nginx/1.31.8
Date: Fri, 23 Oct 2026 12:16:21 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 72
Connection: keep-alive

{
  "status": "ok",
  "service": "catalog-backend",
  "version": "2.0"
}
```

- `/api/products`:

```bash
$ curl -s http://127.0.0.1:8080/api/products | python3 -m json.tool
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

- P001:

```bash
$ curl -i http://127.0.0.1:8080/api/products/P001
HTTP/1.1 200 OK
Server: nginx/1.31.8
Date: Fri, 23 Oct 2026 12:17:06 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 130
Connection: keep-alive

{
  "id": "P001",
  "name": "Notebook Pro 14",
  "category": "Notebook",
  "price": 1299.0,
  "stock": 8,
  "stock_status": "OK"
}
```

- XXX:

```bash
$ curl -i http://127.0.0.1:8080/api/products/XXX
HTTP/1.1 404 Not Found
Server: nginx/1.31.8
Date: Fri, 23 Oct 2026 12:17:17 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 57
Connection: keep-alive

{
  "error": "product_not_found",
  "product_id": "XXX"
}
```

## Networking

- `backend` risolto dal frontend:

```bash
$ docker compose exec frontend \
  sh -c 'wget -qO- http://backend:8000/health'

{
  "status": "ok",
  "service": "catalog-backend",
  "version": "2.0"
}
```

- `localhost:8000` dal frontend:

```bash
$ docker compose exec frontend \
  sh -c 'wget -qO- http://localhost:8000/health'

wget: can't connect to remote host (127.0.0.1): Connection refused
Error: executing /home/steve/.docker/cli-plugins/docker-compose exec frontend sh -c wget -qO- http://localhost:8000/health: exit status 1
```

- spiegazione: `localhost` dentro il frontend indica il frontend stesso, quindi la richiesta fallisce, mentre `backend` è correttamente risolto dal DNS interno.

## Environment

- threshold iniziale: `5`
- threshold temporaneo: `10`
- effetto osservato: Con soglia 10 un solo prodotto non risulta `LOW`
- valore ripristinato: Si

*Nota: il comando `docker compose up -d` dopo aver ricreato il backend non aggiorna l'indirizzo ip che il frontend utilizza per contattare il backend. Questo accade solo con podman a quanto pare, ed è necessario riavviare il frontend manualmente.*

## Volume

- counter before: `1`
- counter after recreate: `4`
- persistenza: PASS
- volume: `catalogo-prodotti_catalog-runtime`

## Lifecycle

- restart test: Effettuato
- log backend:

```bash
backend-1  | Catalog backend listening on http://0.0.0.0:8000 threshold=5 runtime=/runtime
backend-1  | [backend] 127.0.0.1 - "GET /health HTTP/1.1" 200 -
backend-1  | [backend] 10.89.0.7 - "GET /api/products HTTP/1.1" 200 -
backend-1  | [backend] 127.0.0.1 - "GET /health HTTP/1.1" 200 -
backend-1  | [backend] 10.89.0.7 - "GET /api/products HTTP/1.1" 200 -
backend-1  | [backend] 127.0.0.1 - "GET /health HTTP/1.1" 200 -
backend-1  | [backend] 127.0.0.1 - "GET /health HTTP/1.1" 200 -
backend-1  | [backend] 127.0.0.1 - "GET /health HTTP/1.1" 200 -
backend-1  | [backend] 127.0.0.1 - "GET /health HTTP/1.1" 200 -
```

- log frontend:

```bash

frontend-1  | 2026/10/23 13:02:34 [notice] 1#1: start worker process 21
frontend-1  | 2026/10/23 13:02:34 [notice] 1#1: start worker process 22
frontend-1  | 2026/10/23 13:02:34 [notice] 1#1: start worker process 23
frontend-1  | 2026/10/23 13:02:34 [notice] 1#1: start worker process 24
frontend-1  | 2026/10/23 13:02:34 [notice] 1#1: start worker process 25
frontend-1  | 2026/10/23 13:02:34 [notice] 1#1: start worker process 26
frontend-1  | 2026/10/23 13:02:34 [notice] 1#1: start worker process 27
frontend-1  | 2026/10/23 13:02:34 [notice] 1#1: start worker process 28
frontend-1  | 2026/10/23 13:02:34 [notice] 1#1: start worker process 29
frontend-1  | 10.89.0.7 - - [23/Oct/2026:13:02:36 +0000] "GET /api/products HTTP/1.1" 200 688 "-" "curl/8.18.0" "-"
```

## Git

- commit: Effettuato
- push/PR: Push effettuato
