# Consegna UD04 — Verifica

## Parte A — Scelta singola

Per le domande 1–8 riporta risposta e motivazione.

1. A. Blob
2. B. Files
3. B. No, serve un ruolo del piano dati
4. B. ZRS
5. B. SAS
6. C. segnala una soglia ma non blocca i consumi
7. B. soltanto Blob che corrispondono al filtro
8. A. rende esplicito l'uso dell'identità Entra

## Parte B — Risposte brevi

9. La ridondanza serve ad avere copie identiche dello stesso database, le quali conservano anche le modifiche apportate al database principale, serve a proteggere da disservizi di un singolo database. Il backup invece è uno snapshot nel tempo del database e rimane immutato, serve a garantire un processo di recovery dei dati.
10. Il management plane permette operazioni come creare account, modificarne la rete o leggere proprietà (esempio `az network vnet show`), mentre il data plane gestisce le operazioni di caricare, leggere o eliminare un blob tramite Azure Resource Manager (esempio `az storage blob upload`).
11. Una SAS a minimo privilegio deve avere: permessi minimi, scope più ristretto possibile, scadenza breve e trasporto HTTPS;
12. I dati memorizzati nel livello Archive sono mantenuti offline. Per poter accedere al contenuto di un file o scaricarlo, il blob deve prima essere trasferito (reidratato) ad un livello accessibile (Hot, Cold). Questo processo può richiedere diverse ore in base alla priorità scelta.
13. Gli account key sono credenziali a livello di account che forniscono il controllo completo e illimitato su tutte le risorse dello storage, mentre le SAS sono URI firmati temporanei che concedono permessi delegati e limitati nel tempo a risorse specifiche. Trattandosi di veri e propri segreti, lasciarli nel repository consentirebbe a chiunque altro con accesso in lettura al repository di accedere a segreti destinati a individui specifici.

## Parte C — Caso situazionale

14. Utilizzo delle account keys rispetto a RBAC; Condivisione dell'account key; Creazione di un SAS token senza scadenza breve e con permessi eccessivi che viola il principio del minimo privilegio;
15. Utilizzerei Entra ID per l'autenticazione e RBAC per restringere l'accesso ai documenti privati solo ad identità selezionate con il ruolo di `Storage Blob Data Contributor`.
Per accessi temporanei creerei una SAS con solo i permessi sufficienti e necessari, scope limitato al container, e scadenza breve, seguendo così il principio del Least Privilege.
16. Utilizzerei il comando `az storage blob download` per scaricare un documento privato dal container, utilizzando la flag `--auth-mode login` in modo da autenticarmi con Entra ID.
Per verificare un cleanup dei documenti utilizzerei un comando di list `az storage blob list` per verificarne l'esistenza, assicurandomi di utilizzare sempre la flag per l'autenticazione con Entra ID.
