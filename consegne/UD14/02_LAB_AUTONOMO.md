# UD14 — Consegna LAB autonomo

- branch errore: `fix/ud15-target-port`
- target port errato: `9999`
- differenza nel Terraform plan: `Plan: 0 to add, 1 to change, 0 to destroy.`
- IaC: OK
- Test: OK
- BuildPush: OK
- Deploy: OK
- Smoke: Errore
- evidenza ingress:

```bash
az containerapp ingress show   --name catalog-api-ud15   --resource-group rg-ud13-15-delivery   --query "{External:external,TargetPort:targetPort,FQDN:fqdn}"   --output table
External    TargetPort    FQDN
----------  ------------  --------------------------------------------------------------------
True        9999          catalog-api-ud15.niceplant-7e58fd27.italynorth.azurecontainerapps.io
```

- evidenza log:

```bash
az containerapp logs show   --name catalog-api-ud15   --resource-group rg-ud13-15-delivery   --tail 30
{"TimeStamp": "2026-11-03T08:44:25.80825", "Log": "Connecting to the container 'catalog-backend'..."}
{"TimeStamp": "2026-11-03T08:44:25.83407", "Log": "Successfully Connected to container: 'catalog-backend' [Revision: 'catalog-api-ud15--0000004', Replica: 'catalog-api-ud15--0000004-dd86d76c4-m6jqw']"}
{"TimeStamp": "2026-11-03T08:40:51.6928544+00:00", "Log": "backend 16 listening on 0.0.0.0:8000"}
```

- causa: TargetPort errata
- correzione minima: Ripristinare target port a 8000
- branch correzione: `fix/ud15-target-port-correct`
- run finale: OK
- smoke finale: OK
