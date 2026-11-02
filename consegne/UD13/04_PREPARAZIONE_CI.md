# UD13 — Evidenze preparazione Continuous Integration

- Percorso repository usato:
- Resource Group e nome ACR (senza credenziali):

```bash
az group exists --name rg-ud13-15-delivery
true
```

```bash
export ACR_NAME=$(az acr list \
  --resource-group rg-ud13-15-delivery \
  --query "[0].name" \
  --output tsv)

echo $ACR_NAME
acrud1315vanpejrkpcmd6
```

- Esito dei 3 test locali:

```bash
$ python3 -m unittest discover \
  -s app/catalog-backend-ci/tests \
  -v
test_health_status (test_backend.CatalogTests.test_health_status) ... ok
test_health_version (test_backend.CatalogTests.test_health_version) ... ok
test_product_count (test_backend.CatalogTests.test_product_count) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

- Build Docker locale ed esito `/health`:

Build:

```bash
docker build \
  -t catalog-backend:ud13-local \
  app/catalog-backend-ci
STEP 1/8: FROM python:3.13-slim
STEP 2/8: WORKDIR /app
--> Using cache 8205761b06fe69c2f92397750659bb758619380b06fc3c21b117e2c3ae5c5125
--> 8205761b06fe
STEP 3/8: COPY server.py /app/server.py
--> e1495cbaccef
STEP 4/8: RUN useradd --create-home --uid 10001 appuser     && chown -R appuser:appuser /app
--> 6612b9af9606
STEP 5/8: USER appuser
--> 3f41800e8d2c
STEP 6/8: ENV APP_HOST=0.0.0.0     APP_PORT=8000     APP_VERSION=ci-v1
--> 0378b34d4514
STEP 7/8: EXPOSE 8000
--> 47d968c8bdce
STEP 8/8: CMD ["python", "/app/server.py"]
COMMIT catalog-backend:ud13-local
--> 84b78b3877a3
Successfully tagged localhost/catalog-backend:ud13-local
84b78b3877a3f5735f334f715b6f228f86d3ebd4f13998bbd27e52f7b245a5ec
```

Test `/health`:

```bash
curl -s http://127.0.0.1:18014/health \
  | python3 -m json.tool

{
    "status": "ok",
    "service": "catalog-backend",
    "version": "ci-v1"
}
```

- Stato di `sc-acr-ud14` e WIF:

- Modalità agent scelta (`MICROSOFT_HOSTED` oppure `SELF_HOSTED_FALLBACK`): `SELF_HOSTED_FALLBACK` BLOCKED_BY_DOCKER_SERVICE_CONNECTION

- YAML CI utilizzato: `azure-pipelines-ci-selfhosted.yml`
- Nome della sola pipeline CI: `azure-pipelines-ci-selfhosted.yml`
- Prima run (ID, esito osservato o blocco reale):
- Stage Test (esito):
- Stage BuildPush (esito):
- Traccia dei log Agent.Name / OS / MachineName:
- Stato finale e azioni rinviate alla nuova UD14:
