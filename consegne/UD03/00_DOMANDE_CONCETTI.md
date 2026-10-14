# Consegna UD03 — Domande sui concetti

Per ciascuna domanda 1–8 riporta una risposta motivata.

1. L'autenticazione riuscita dimostra semplicemente che l'utente è chi dice di essere, ma non dice cosa può fare l'utente, mentre l'autorizzazione sufficiente permette all'utente di compiere le azioni necessarie in piattaforma.
2. I ruoli Microsoft Entra autorizzano la gestione degli oggetti della directory (es. creazione utente nel tenant), mentre i ruoli Azure autorizzano operazioni sulle risorse Azure tramite Azure Resource Manager (es. leggere una VNet).
3. Una role assignment è formata da tre elementi: un Ruolo, un'Identità e uno Scope.
4. Perché per evitare compromissioni è necessario adottare sempre la policy Zero-Trust, e assegnare solo i permessi strettamente necessari. Un Reader con la sola necessita di consultare il progetto non dovrebbe poterlo modificare.
5. Per ragioni di sicurezza e coerenza dell'architettura, in Azure, il controllo degli accessi basato sui ruoli (RBAC) segue un modello strettamente gerarchico a cascata. Se un ruolo viene assegnato a un livello superiore (scope padre, come un Gruppo di gestione, una Sottoscrizione o un Gruppo di risorse), viene automaticamente ereditato da tutte le risorse contenute al suo interno. Per rimuovere l'accesso, è necessario eliminare l'assegnazione di ruolo esattamente al livello (scope) in cui è stata originariamente creata.
6. No perché un tag è solo un modo per categorizzare le risorse e i gruppi, di per se non comporta nessuna azione.
7. Un lock `CanNotDelete` protegge uno scope da eliminazione, il ruolo `Reader` permette di poter leggere la risorsa.
8. Un budget serve soltanto a generare notifiche per persone o sistemi automatizzati quando la spesa supera una soglia, ma di per se non blocca automaticamente la spesa e non spegne le risorse.
