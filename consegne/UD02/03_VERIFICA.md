# Consegna UD02 — Verifica

## Parte A — Scelte operative

Per le domande 1–8 riporta risposta e motivazione.

1. Il modello più coerente è IaaS, perché permette di personalizzare il sistema operativo e l'ambiente in ogni aspetto, così da configure la macchina per supportare il componente.
2. Configurazione dell'applicazione, identità, accessi e dati. Azure App Service è un PaaS, fornisce già la piattaforma e l'infrastruttura per far girare l'app, il cliente deve solo pensare a gestire l'applicazione.
3. È un contenitore logico per risorse che possono condividere ciclo di vita e governance. Questo permette alle risorse di essere eliminate in gruppo quando non più necessari, evitando così di lasciare risorse orfane frammentate che potrebbero consumare budget.
4. La località indica dove Azure conserva i metadati del resource group; le risorse possono avere località proprie, essendo i datacenter fisici sparsi per tutto il mondo.
5. Il comando `az account show` permette di controllare il tenant e la sottoscrizione attivi sui quali il gruppo di risorse verrà creato.
6. `stcea02a7f9`. Sono ammessi solo numeri e lettere minuscole, senza spazi, senza trattini e con una lunghezza compresa tra 3 e 24 caratteri.
7. Il tag documenta l'intenzione, ma serve ancora una procedura o una policy che esegua l'eliminazione. Categorizzare una risorsa di per se non fa nulla.
8. `az group exists --name <NOME>` restituisce `false`. Questo significa che il gruppo di risorse non esiste più, e tutte le risorse con esso associate sono state eliminate.

## Parte B — Risposte brevi

9. Prendendo come esempio un sito di e-commerce, con un cloud pubblico il cliente non possiede l'infrastruttura, la piattaforma o le risorse perché queste sono fornite da un provider. Macchine virtuali, backend/frontend e database sono tutti ospitati sull'infrastruttura del provider. Con un cloud privato, il cliente possiede tutto il necessario per eseguire la propria applicazione; questo approccio offre un maggiore controllo a scapito dei costi. Con un cloud ibrido, invece, le risorse del provider e del cliente collaborano; il backend e il frontend del sito di e-commerce potrebbero essere ospitati su un'infrastruttura privata, mentre i database potrebbero essere servizi messi a disposizione dal provider.
10. Microsoft Entra Tenant definisce l'identità, i meccanismi di accesso e le policy di sicurezza per un'organizzazione. La sottoscrizione è un accordo commerciale che lega risorse al budget e alle politiche di quota, funge da confine logico per la fatturazione. Il resource group è un contenitore logico che raggruppa più risorse che devono condividere il ciclo di vita (creazione, aggiornamento, eliminazione). La risorsa è l'elemento computazionale o di archiviazione finale creato all'interno del gruppo di risorse.
11. Una region rappresenta una macro area geografica, mentre un'availability zone rappresenta il singolo datacenter fisico all'interno della region, servono a proteggere i carichi di lavoro all'interno della stessa region.
12. Il portale offre una navigazione intuitiva per esplorare tutte le funzionalità, mentre la CLI permette di eseguire subito operazioni complesse, come la registrazione ad un provider o l'eliminazione di un gruppo.
13. In Azure, l'architettura di base stabilisce che i tag non sono ereditati di default, se volessimo taggare le risorse oltre a farle condividere lo stesso ciclo di vita, bisogna taggarle singolarmente.

## Parte C — Interpretazione tecnica

1. Sottoscrizione `<omitted>`, Resource group: `rg-cea-test`, Provider: `Microsoft.Storage`, Tipo: `Microsoft.Storage/storageAccounts`, Nome: `stceatest01`.
2. Località: `italynorth`, Tag: `environment: lab, unit: UD02`
3. `az storage account show --name stceatest01 --resource-group rg-cea-test`.
4. `az group delete --name rg-cea-test --yes --no-wait`
5. Verificherei che il gruppo esiste ancora con: `az group exists --name rg-cea-test`.
