# Consegna UD02 — Domande sui concetti

Per ciascuna domanda 1–8 riporta una risposta motivata.

1. In una macchina virtuale il cliente gestisce il sistema operativo, le patch e il runtime. App Service è invece un modello in cui Microsoft si fa carico dell'infrastruttura, il cliente ha solo la responsabilità del codice dell'applicazione e dei dati.
2. Il tenant rappresenta l'organizzazione che gestisce le risorse cloud, definisce un confine delle identità; la sottoscrizione è un accordo commerciale che lega risorse al budget e alle politiche di quota, funge da confine logico per la fatturazione; un resource group è un contenitore logico di risorse vincolato dalla sottoscrizione, le risorse all'interno del resource group condividono normalmente ciclo di vita, scopo o responsabilità.
3. La località del resource group indica quale infrastruttura viene utilizzata per gestire i metadati del gruppo, ma ogni risorsa può adoperare su una o più località diverse, indipendemente dalle località delle altre risorse o del resource group.
4. Una region è un'ampia area geografica globale (es. Europa Occidentale) composta da più data center. Un'availability zone rappresenta invece uno o più data center fisici separati situati all'interno della stessa region, permettono di proteggere i servizi da guasti di singole strutture.
5. Perché è necessario verificare il tenant e la sottoscrizione impostata nella CLI per evitare di creare risorse associate ad ambienti sbagliati.
6. I tag sono semplici metadati in chiaro progettati esclusivamente per la categorizzazione logica, non applicano regole di sicurezza (isolamento, autorizzazione) e sono visbili da chiunque abbia i privilegi di lettura sulla risorsa.
7. Adoperare sulla CLI permette di velocizzare e automatizzare l'esecuzione di processi e operazioni complesse, che altrimenti richiederebbero molto più tempo se si utilizasse l'interfaccia grafica. (es. `az group delete`). Con la CLI si possono salvare i comandi in script, versionarli e riprodurre le operazioni in modo controllato.
8. Quando si manda una richiesta di eliminazione, bisogna aspettare che Azure processi la richiesta, siccome la richiesta potrebbe fallire bisogna sempre verificarne l'esito.
