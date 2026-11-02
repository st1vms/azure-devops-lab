# UD14 — Verifica finale

## Scenario 1

1. L'applicazione riceve il traffico sulla porta errata (9999 anziché 8000), quindi non risponde alle chiamate dello smoke test.
2. Non toccherei il codice dell'applicazione che funziona correttamente, ma correggerei solo la configurazione della porta su Terraform.

## Scenario 2

1. Controllo che l'identità della service connection abbia il ruolo di `Storage Blob Data Contributor` sul container dello state.
2. Perché lo state contiene dati sensibili e rischia di creare conflitti e problemi di concorrenza tra i vari agenti e job.

## Scenario 3

1. Controllo la service connection `sc-azure-ud13-15` e che abbia il ruolo `AcrPush` sull'Azure Container Registry.
2. Perché si preferisce usare un'autenticazione sicura basata su identità e token temporanei senza password fisse.

## Scenario 4

1. Confronto il Build ID della pipeline, il tag dell'immagine su ACR, la versione configurata e l'endpoint `/health` dell'applicazione.

## 1. Distingui Continuous Integration e Continuous Delivery

**Risposta:** La CI verifica codice e costruisce le immagini; la CD distribuisce l'artefatto sull'infrastruttura e verifica che il servizio risponda correttamente.

## 2. Perché UD14 utilizza uno state remoto?

**Risposta:** Perché ogni job pulisce l'ambiente locale e serve uno spazio condiviso e sicuro per ricordare lo stato delle risorse.

## 3. Perché lo Storage Account dello state viene preparato prima del laboratorio?

**Risposta:** Perché Terraform ha bisogno di un backend già esistente per poter salvare e leggere lo state fin dal primo comando.

## 4. Come si autentica Terraform nella pipeline?

**Risposta:** Terraform riutilizza la sessione di autenticazione di Azure CLI aperta tramite la service connection.

## 5. Quali risorse sono data source e quali sono gestite da Terraform?

**Risposta:** Il Resource Group, l'ACR e la managed identity sono letti come esistenti (data source); l'Environment e la Container App sono gestiti direttamente da Terraform.

## 6. Perché il piano viene eseguito anche prima della build?

**Risposta:** Per validare la sintassi e verificare la coerenza dell'infrastruttura prima di avviare la creazione dell'immagine.

## 7. Perché viene ricreato nello stage Deploy?

**Risposta:** Perché lo stato dell'infrastruttura potrebbe essere cambiato e serve un piano aggiornato prima di applicare le modifiche.

## 8. Perché la pipeline utilizza `AzureCLI@2` invece di `Docker@2`?

**Risposta:** Per poter usare un'unica service connection e gestire insieme comandi Azure, Docker e Terraform nella stessa sessione.

## 9. Quale ruolo ha la pipeline sull'ACR?

**Risposta:** Ha il ruolo `AcrPush` per poter caricare le nuove immagini dei container.

## 10. Quale ruolo ha la managed identity della Container App?

**Risposta:** Ha il ruolo `AcrPull` per poter scaricare e leggere in sicurezza l'immagine dal registry.

## 11. Perché `workspace: clean: all` non deve cancellare lo state della delivery?

**Risposta:** Perché lo state è salvato nel Blob Storage remoto su Azure e non sui file locali dell'agente.

## 12. Che cosa viene eliminato da `terraform destroy` alla fine?

**Risposta:** Vengono eliminate tutte le risorse gestite dallo state di Terraform della UD14 (Container App e relativo Environment).

## Cleanup finale

- pipeline Terraform destroy: Eseguito
- Container App rimossa: Si
- Environment rimosso: SI
- Resource Group eliminato: Si
- service connection rimosse: SI
- Agent deregistrato: Si
- repository conservato: Si
