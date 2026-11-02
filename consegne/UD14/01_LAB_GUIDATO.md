# UD14 — Consegna LAB guidato

## Controlli iniziali

- ACR: `acrud1315vanpejrkpcmd6`
- `LegacyRegistryPermissions`: Assegnato
- `sc-azure-ud13-15`: Esistente
- `AcrPush`: Assegnato al principal del ACR
- Storage state: Available
- container state: Available
- `Storage Blob Data Contributor`: Assegnato
- managed identity: Creata
- `AcrPull`: Assegnato
- Agent: `Online`

## Terraform

- init: Success
- validate: Success
- plan iniziale: Eseguito con successo
- apply: Non Eseguito
- state remoto: `/tfstate/ud15.tfstate`

## Pipeline

- Build ID: `#20261102.1`
- IaC: Eseguito con successo
- Test: Eseguito con successo
- BuildPush: Eseguito con successo
- Deploy: Eseguito con successo
- Smoke: Eseguito con successo

## Deployment

- image tag: `12, 8, 7`
- FQDN: `catalog-api-ud15.niceplant-7e58fd27.italynorth.azurecontainerapps.io`
- APP_VERSION: `12`
- revision: `catalog-api-ud15--ov6tb65`
- health:

```json
{
    "status": "ok",
    "service": "catalog-backend",
    "version": "12"
}
```
