# Consegna UD04 — Domande sui concetti

Per ciascuna domanda 1–8 riporta una risposta motivata.

1. Perché i due modelli di storage sono intrinsicamente diversi, blob storage conserva dati grezzi senza metadati, mentre files storage archivia file strutturati in una cartella condivisa.
2. Il management plane permette operazioni come creare account, modificarne la rete o leggere proprietà, mentre il data plane gestisce le operazioni di caricare, leggere o eliminare un blob tramite Azure Resource Manager.
3. Perché `Contributor` è un ruolo del management plane, mentre per il data plane servono ruoli specifici, come `Storage Blob Data Reader` o `Storage Blob Data Contributor`.
4. La ridondanza non equivale a backup, serve ad avere copie identiche dello stesso database, le quali conservano anche le modifiche apportate al database principale, serve a proteggere da disservizi di un singolo database. Il backup invece è uno snapshot nel tempo del database e rimane immutato.
5. Valuterei la frequenza e il tempo massimo di recupero, la permanenza minima e i costi delle operazioni.
6. Un'account key fornisce l'accesso completo e incondizionato a tutti i servizi dello storage account e a tutte le risorse al suo interno, permette qualsiasi azione del management plane e del data plane. Mentre una SAS limitata definisce permessi granulari limitati solo a ciò che è strettamente necessario, seguenzo il prinicipio di ZeroTrust.
7. Una SAS permette di applicare restrizioni sui permessi di accesso alle singole risorse, è configurata per avere una data di scadenza, e impone restrizioni di sicurezza come l'utilizzo di HTTPS, o le restrizioni per IP.
8. Perché l'elaborazione del job non è immediato e può iniziare dopo ore.
