# Consegna UD03 — Verifica

## Parte A — Scelta singola

Per le domande 1–8 riporta risposta e motivazione.

1. B. L'autenticazione è riuscita, ma manca un'autorizzazione applicabile
2. D. Password
3. C. Reader sul resource group
4. B. ereditato
5. B. Contributor
6. C. impedisce l'eliminazione finché applicabile
7. B. genera una condizione di notifica, ma non costituisce un tetto automatico
8. B. Microsoft Entra ID con ruolo appropriato

## Parte B — Risposte brevi

9. Assegnare ruoli ai gruppi garantisce scalability e semplifica la gestione. Si possono modificare i permessi dei membri di un team senza dover alterare le singole assegnazioni di ruolo.
10. I ruoli di Microsoft Entra ID gestiscono le identià e le configurazioni al livello di tenant, mentre i ruoli Azure RBAC gestiscono l'accesso alle risorse.
11. L'utente ha accesso effettivo come Contributor, questo perché le autorizzazioni sono additive in Azure, i permessi ereditati si sommano a quelli assegnati direttamente, Contributor include tutti i permessi di lettura e scrittura e quindi supera il ruolo Reader.
12. - (a) Identificare l'esatto Security Principal che ha generato l'errore.
    - (b) Verificare le assegnazioni di ruolo dello scope target e assicurarsi che includano l'azione richiesta.
    - (c) Controllare se sullo scopo e sugli scope padre è applicato un lock di tipo ReadOnly.
    - (d) Verificare le assegnazioni di Azure Policy per accertarsi che non ci sia un effetto Deny che blocca la creazione o la modifica della risorsa.
13. Il tag `deleteAfter ` è un metadato, non esegue alcuna azione di per se, il lock `CanNotDelete` è un blocco nativo che impedisce l'eliminazione della risorsa da parte di chiunque, inclusi gli amministratori. Il Budget è uno strumento di monitoraggio e controllo dei costi che permette di mandare notifiche al raggiungimento di una soglia di spesa, ma non arresta le risorse e non blocca i costi.

## Parte C — Caso situazionale

14. Assegnare `Contributor` sull'intera sottoscrizione viola il principio di ZeroTrust, al tecnico è stato concesso il diritto di creare, modificare ed eliminare qualsiasi risorsa nell'intera infrastruttura, quando aveva bisogno solo dei permessi di lettura per uno scope ben preciso. Un secondo errore è stato il presupposto errato che il ruolo di Contributor consentisse la gestione dei permessi.

15. Il ruolo più appropriato sarebbe stato `Reader` essendo il requisito minimo e necessario per consultare la VNet.
16. Non riesce ad assegnare il ruolo perché `Contributor` non fornisce i permessi la gestione degli accessi e delle identità, per quello serve il ruolo `Owner` o `User Access Administrator`.
Riceve l'errore `ScopeLocked` perché è stato applicato un lock di tipo `CanNotDelete` o `ReadOnly`.
