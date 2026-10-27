# UD11 — Consegna laboratorio guidato

## Preflight

- Azure: Loggato
- Docker: Installato
- containerapp extension:

```bash
$ az extension show \
  --name containerapp \
  --query "{Name:name,Version:version}" \
  --output table
Name          Version
------------  ---------
containerapp  1.3.0b5
```

- Microsoft.App:

```bash
$ az provider show \
  --namespace Microsoft.App \
  --query registrationState \
  --output tsv
Registered
```

- Microsoft.OperationalInsights:

```bash
$ az provider show \
  --namespace Microsoft.OperationalInsights \
  --query registrationState \
  --output tsv
Registered
```

- Microsoft.ContainerRegistry:

```bash
$ az provider show \
  --namespace Microsoft.ContainerRegistry \
  --query registrationState \
  --output tsv
Registered
```

## ACR

- nome: `acr1793093899ud11`
- SKU: `Basic`
- login server: `acr1793093899ud11.azurecr.io`
- repository: `app/catalog-backend-cloud`
- tag v1: `ud11-v1`
- tag v2: `ud11-v2`
- admin user abilitato: NO

```bash
$ az acr create \
  --resource-group "$LAB_RG" \
  --name "$ACR" \
  --sku Basic \
  --location "$LAB_LOCATION" \
  --role-assignment-mode rbac \
  --output table
NAME               RESOURCE GROUP      LOCATION    SKU    LOGIN SERVER                  CREATION DATE         ADMIN ENABLED
-----------------  ------------------  ----------  -----  ----------------------------  --------------------  ---------------
acr1793093899ud11  rg-ud11-containers  italynorth  Basic  acr1793093899ud11.azurecr.io  2026-10-27T09:59:41Z  False
```

## v1

- local test: Funzionante
- push: Effettuato con successo

- ACR tag:

```bash
$ az acr repository show-tags \
  --name "$ACR" \
  --repository "$IMAGE_REPO" \
  --output table
Result
--------
v1
```

- ACA environment:

```bash
$ az containerapp env show \
  --name "$ACA_ENV" \
  --resource-group "$LAB_RG" \
  --query "{Name:name,Location:location,State:properties.provisioningState}" \
  --output table
Name         Location     State
-----------  -----------  ---------
acaenv-ud11  Italy North  Succeeded
```

- Container App: Creata
- managed identity:

```bash
az containerapp identity show \
  --name "$ACA_APP" \
  --resource-group "$LAB_RG" \
  --query "{Type:type}" \
  --output table
Type
--------------
SystemAssigned
```

- registry identity: `system`
- ingress: `external`
- target port: `8000`
- FQDN: `catalog-api-ud11.kindpond-6ea78ed6.italynorth.azurecontainerapps.io`
- health:

```bash
curl -i "https://$ACA_FQDN/health"
HTTP/2 200
server: CatalogBackend/3.0 Python/3.13.17
date: Tue, 27 Oct 2026 10:51:31 GMT
content-type: application/json; charset=utf-8
content-length: 71

{
  "status": "ok",
  "service": "catalog-backend",
  "version": "v1"
}
```

- version: `v1`
- revision:

```bash
az containerapp revision list \
  --name "$ACA_APP" \
  --resource-group "$LAB_RG" \
  --query "[].{Name:name,Active:properties.active,Health:properties.healthState,Replicas:properties.replicas}" \
  --output table
Name                  Active    Health    Replicas
--------------------  --------  --------  ----------
catalog-api-ud11--v1  True      Healthy   1
```

- logs:

```bash
az containerapp logs show \
  --name "$ACA_APP" \
  --resource-group "$LAB_RG" \
  --tail 30
{"TimeStamp": "2026-10-27T10:53:14.17342", "Log": "Connecting to the container 'catalog-api-ud11'..."}
{"TimeStamp": "2026-10-27T10:53:14.27274", "Log": "Successfully Connected to container: 'catalog-api-ud11' [Revision: 'catalog-api-ud11--v1', Replica: 'catalog-api-ud11--v1-5b86cc874-vks8n']"}
{"TimeStamp": "2026-10-27T10:49:35.5227121+00:00", "Log": "F Catalog backend v1 listening on http://0.0.0.0:8000 threshold=5"}
{"TimeStamp": "2026-10-27T10:51:31.0464422+00:00", "Log": "F [backend v1] 100.100.0.161 - \"GET /health HTTP/1.1\" 200 -"}
{"TimeStamp": "2026-10-27T10:52:05.5558265+00:00", "Log": "F [backend v1] 100.100.0.161 - \"GET /api/products HTTP/1.1\" 200 -"}
{"TimeStamp": "2026-10-27T10:52:27.8608718+00:00", "Log": "F [backend v1] 100.100.0.161 - \"GET /api/products HTTP/1.1\" 200 -"}
{"TimeStamp": "2026-10-27T10:53:06.256864+00:00", "Log": "F [backend v1] 100.100.0.66 - \"GET / HTTP/1.1\" 404 -"}
```

## v2

- Dockerfile version: `v2`
- local test: Superato
- push: Effettuato con successo
- ACR tag:

```bash
az acr repository show-tags \
  --name "$ACR" \
  --repository "$IMAGE_REPO" \
  --orderby time_desc \
  --output table
Result
--------
v2
v1
```

- update: Effettuato
- revision:

```bash
az containerapp revision list \
  --name "$ACA_APP" \
  --resource-group "$LAB_RG" \
  --query "[].{Name:name,Active:properties.active,Health:properties.healthState,Created:properties.createdTime}" \
  --output table
Name                  Active    Health    Created
--------------------  --------  --------  -------------------------
catalog-api-ud11--v1  True      Healthy   2026-10-27T10:48:48+00:00
catalog-api-ud11--v2  True      Healthy   2026-10-27T10:56:23+00:00
```

- health:

```bash
$ curl -s "https://$ACA_FQDN/health" | python3 -m json.tool
{
    "status": "ok",
    "service": "catalog-backend",
    "version": "v2"
}
```

- version: `v2`

## Scaling

```bash
$ az containerapp show \
  --name "$ACA_APP" \
  --resource-group "$LAB_RG" \
  --query properties.template.scale \
  --output jsonc
{
  "cooldownPeriod": 300,
  "maxReplicas": 1,
  "minReplicas": 0,
  "pollingInterval": 30,
  "rules": null
}
```

- minReplicas: `0`
- maxReplicas: `1`
- scale-to-zero possibile: Si
