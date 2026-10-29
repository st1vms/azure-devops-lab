# UD13 — Consegna LAB autonomo

- branch: `fix/ud13-pipeline-path` Pushata
- path errato: `infra/bicep/delivery-NON-ESISTE.bicep`
- stage: `Validate`
- job: `ValidateIaC`
- step: `Bicep lint`
- messaggio:

```txt
ERROR: An error occurred reading file. Could not find file '/home/user/Scrivania/workspace/azdo-agent-ud09/_work/1/s/infra/bicep/delivery-NON-ESISTE.bicep'.
```

- classe del problema: Errore tipografico.
- correzione: Ripristinare il path corretto: `infra/bicep/delivery.bicep`
- run finale: Eseguita con successo
- PR/merge: Eseguito
