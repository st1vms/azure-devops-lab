# UD12 — Verifica individuale

## Parte A

1. B. lo stato desiderato
2. A. Azure Resource Manager
3. B. prevedere le modifiche di un deployment
4. B. prepara la directory e i provider
5. B. controlla la configurazione senza applicare risorse
6. B. collegare gli oggetti Terraform alle risorse gestite
7. B. rimuove le risorse gestite dalla configurazione/state
8. B. codice IaC, strumenti e agent configurato

## Parte B

## 9. Distingui approccio imperativo e dichiarativo

**Risposta:** L'approccio imperativo descrive la sequenza dettagliata delle azioni da compiere passo dopo passo. L'approccio dichiarativo descrive invece lo stato finale desiderato, lasciando che lo strumento interpreti come ottenerlo.

## 10. Perché è utile separare parametri e definizione delle risorse?

**Risposta:** Permette di riutilizzare lo stesso file di codice IaC in ambienti differenti (come test o produzione) modificando unicamente i valori esterni dei parametri.

## 11. Distingui Bicep What-If e Terraform Plan

**Risposta:** Il What-If di Bicep mostra le modifiche previste da Azure Resource Manager sul cloud. Il Terraform Plan calcola invece le variazioni confrontando la configurazione locale, i provider e lo state di Terraform.

## 12. Perché il Terraform state non deve essere committato come un normale sorgente?

**Risposta:** Il file di state contiene metadati operativi e potenziali dati sensibili legati alle risorse gestite, per cui va protetto da modifiche concorrenti o esposizioni accidentali.

## 13. Distingui `terraform validate`, `plan` e `apply`

**Risposta:** `validate` controlla la correttezza sintattica e formale della configurazione; `plan` calcola e mostra in anteprima le operazioni che verranno eseguite; `apply` applica concretamente le modifiche sull'infrastruttura reale.

## 14. Perché in questa UD distruggiamo le risorse Azure ma conserviamo i file IaC?

**Risposta:** Le risorse Azure sono temporanee e vengono eliminate per evitare costi inutili, mentre i file IaC costituiscono il codice sorgente del progetto e vanno conservati nel repository per gli utilizzi futuri.

## Parte C

> Un collega modifica main.tf. terraform validate riesce. terraform plan mostra 1 to add, 0 to change, 2 to destroy, ma il collega si aspettava soltanto l'aggiunta di un tag.

## 15. Deve eseguire immediatamente `terraform apply`? Spiega il perché

**Risposta:** No, non deve eseguirlo immediatamente. Il piano mostra due elementi da eliminare (destroy), mentre il collega si aspettava solo l'aggiunta di un tag: procedere cancellerebbe risorse esistenti per errore.

## 16. Quali controlli dovrebbe fare prima di applicare qualsiasi modifica?

**Risposta:** Dovrebbe verificare con attenzione il report del terraform plan per individuare eventuali eliminazioni o modifiche non desiderate e riesaminare il file main.tf per correggere l'errore commesso.

## 17. Perché installare Terraform in WSL2 prepara il self-hosted Agent ma non garantisce nulla sul Microsoft-hosted Agent?

**Risposta:** Perché il self-hosted Agent si appoggia a una macchina persistente (il WSL2) dove i tool restano installati, mentre i Job Microsoft-hosted utilizzano macchine virtuali temporanee e pulite fornite da Microsoft.

## 18. Perché un Job Microsoft-hosted non deve dipendere da file creati dal Job precedente?

**Risposta:** Perché ogni Job Microsoft-hosted viene eseguito su una macchina virtuale nuova e isolata, senza alcuna persistenza dei file o dello stato del Job precedente.

## 19. Perché è utile verificare `terraform version`, `az version` e `az bicep version` all'interno di una pipeline?

**Risposta:** Per accertarsi che l'ambiente di esecuzione disponga esattamente degli strumenti e delle versioni compatibili necessari al corretto svolgimento del deployment.

## 20. Qual è il vantaggio e quale il rischio di usare `ubuntu-latest` rispetto a un'immagine versionata?

**Risposta:** Il vantaggio è l'utilizzo continuo delle ultime versioni software e patch disponibili. Il rischio è che gli aggiornamenti automatici possano introdurre modifiche o comportamenti inaspettati che interrompono la pipeline.

## Gate 2

- agent Online: Si
- Terraform disponibile: Si
- Azure CLI/Bicep disponibile: Si
- Git/Python/Docker disponibili: Si

## Gate 2A — self-hosted

- Agent Online: Si
- Terraform: disponibile
- Azure CLI: disponibile
- Bicep: disponibile
- Git: disponibile
- Python: disponibile
- Docker: disponibile

## Gate 2B — Microsoft-hosted

- stato: `MICROSOFT_HOSTED_READY`
