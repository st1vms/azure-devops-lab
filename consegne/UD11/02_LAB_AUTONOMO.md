# UD11 — Consegna laboratorio autonomo

## Baseline

- status: `ok`
- version: `v2`
- target port: `8000`

## Errore

- nuovo target port: `9999`
- sintomo: La richiesta verso l'endpoint `/health` ritorna error 503.
- HTTP/timeout:

```bash
HTTP/2 503
content-length: 190
content-type: text/plain
date: Tue, 27 Oct 2026 13:28:38 GMT

upstream connect error or disconnect/reset before headers. retried and the latest reset reason: remote connection failure, transport failure reason: delayed connect error: Connection refused
```

## Evidenze

- running status:

```bash
az containerapp show \
  --name "$ACA_APP" \
  --resource-group "$LAB_RG" \
  --query "{State:properties.runningStatus,FQDN:properties.configuration.ingress.fqdn}" \
  --output table
State    FQDN
-------  -------------------------------------------------------------------
Running  catalog-api-ud11.kindpond-6ea78ed6.italynorth.azurecontainerapps.io
```

- revision:

```bash
az containerapp revision list \
  --name "$ACA_APP" \
  --resource-group "$LAB_RG" \
  --query "[].{
    Name:name,
    Active:properties.active,
    Health:properties.healthState
  }" \
  --output table
Name                  Active    Health
--------------------  --------  --------
catalog-api-ud11--v2  True      Healthy
```

- health: Irraggiungibile
- log listen port:

```bash
az containerapp logs show \
  --name "$ACA_APP" \
  --resource-group "$LAB_RG" \
  --tail 30
{"TimeStamp": "2026-10-27T13:30:45.61615", "Log": "Connecting to the container 'catalog-api-ud11'..."}
{"TimeStamp": "2026-10-27T13:30:45.68553", "Log": "Successfully Connected to container: 'catalog-api-ud11' [Revision: 'catalog-api-ud11--v2', Replica: 'catalog-api-ud11--v2-676c45b459-gl9n6']"}
{"TimeStamp": "2026-10-27T13:28:35.3441601+00:00", "Log": "F Catalog backend v2 listening on http://0.0.0.0:8000 threshold=5"}
```

- ingress target port:

```bash
az containerapp ingress show \
  --name "$ACA_APP" \
  --resource-group "$LAB_RG" \
  --query "{External:external,TargetPort:targetPort}" \
  --output table
External    TargetPort
----------  ------------
True        9999
```

## Diagnosi

- Sintomo: La chiamata all'endpoint `/health` restituisce un errore HTTP 503 (`remote connection failure, Connection refused`).
- Risultato atteso: La risposta HTTP dovrebbe ritornare lo stato dell'applicazione in formato JSON con versione `v2`.
- Evidenza: L'ingress della Container App è configurato sul `targetPort` 9999, mentre il backend logga l'ascolto sulla porta 8000.
- Ipotesi: Il traffico in ingresso viene instradato verso una porta errata dove nessun processo è in ascolto.
- Causa: La configurazione dell'ingress punta a una porta non coincidente con quella effettiva del container.
- Correzione minima: Aggiornare il `targetPort` dell'ingress riportandolo a 8000.

## Verifica

- target port: `8000`
- health:

```bash
{
    "status": "ok",
    "service": "catalog-backend",
    "version": "v2"
}
```

- version: `v2`

## Domande

### 1. Era necessario creare una nuova image?

**Risposta:** No, l'image era corretta e funzionante; il problema riguardava esclusivamente la configurazione dell'ingress.

### 2. Era necessario fare push di v3?

**Risposta:** No, non vi era alcuna necessità di rilasciare una nuova versione o fare il push di una tag v3.

### 3. Il problema era ACR, managed identity o ingress?

**Risposta:** Il problema risiedeva interamente nella configurazione dell'ingress e nel disallineamento della porta.

### 4. Quale evidenza ha identificato la causa?

**Risposta:** Il confronto tra i log applicativi, che indicavano l'ascolto sulla porta 8000, e la configurazione dell'ingress impostata sulla porta 9999.

### 5. Perché modificare più impostazioni contemporaneamente sarebbe stato un errore metodologico?

**Risposta:** Perché avrebbe impedito di isolare la causa radice del guasto, violando il principio di troubleshooting incrementale.

## Passaggio alla verifica

- target port ripristinato a 8000: Si
- health v2 nuovamente OK: Si
- Resource Group mantenuto disponibile: sì
