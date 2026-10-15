# Consegna UD04 — Laboratorio autonomo

## Scelta del servizio e della ridondanza

Riporta requisito, servizio scelto, ridondanza e motivazione.

Ho scelto Azure Blob Storage perché è l'unico servizio ottimizzato per l'archiviazione di documenti, con supporto nativo per regole di Lifecycle e delega dell'accesso tramite User Delegation SAS.
Ho impostato la tier su Hot siccome i dati devono essere accessibili frequentemente entro 30 giorni.
Se il requisito comprende resilienza a un guasto zonale sceglierei ZRS, il quale distribuisce copie dei dati in zone distinte, proteggendo da disservizi dei singoli data-center.
Inoltre è necessario creare una SAS per l'eliminazione automatica dei file temporanei dopo un giorno.

## Operazioni e verifica

Documenta container, Blob e SAS limitata riportando soltanto configurazione ed esito.

Creazione container:

```bash
az storage container create --account-name "$LAB_STORAGE" --name archive --auth-mode login
{
  "created": true
}
```

Caricamento file:

```bash
az storage blob upload --account-name "$LAB_STORAGE" --container-name archive --name current/documento.txt --file consegne/UD04/01_DOCUMENTO_LAB.txt --auth-mode login --overwrite
{
  "client_request_id": "<ommited>",
  "content_md5": "iHJM98k0MPZjlOJ7uiHd5g==",
  "date": "2026-10-15T10:52:34+00:00",
  "encryption_key_sha256": null,
  "encryption_scope": null,
  "etag": "\"0x8DF2AAA6B51D9DD\"",
  "lastModified": "2026-10-15T10:52:34+00:00",
  "request_id": "<omitted>",
  "request_server_encrypted": true,
  "structured_body": null,
  "version": "2026-04-06",
  "version_id": null
}
```

Verifica caricamento blob:

```bash
az storage blob list --account-name "$LAB_STORAGE" --container-name archive --auth-mode login --output table
Name                   Blob Type    Blob Tier    Length    Content Type    Last Modified              Snapshot
---------------------  -----------  -----------  --------  --------------  -------------------------  ----------
current/documento.txt  BlockBlob    Hot          49        text/plain      2026-10-15T10:52:34+00:00
```

Configurazione Blob:

- Name: `current/documento.txt`
- Type: `BlockBlob`;
- Tier: `Hot`;

Creazione SAS:

```bash
SAS_EXPIRY="$(date -u -d '+15 minutes' +%Y-%m-%dT%H:%MZ)"

SAS_URL="$(az storage blob generate-sas \
  --account-name "$LAB_STORAGE" \
  --container-name "$LAB_CONTAINER" \
  --name current/documento.txt \
  --permissions r \
  --expiry "$SAS_EXPIRY" \
  --auth-mode login \
  --as-user \
  --full-uri \
  --output tsv)"

unset SAS_URL
```

Comandi di verifica:

```bash
curl --fail --silent --show-error "$SAS_URL" --output current-documento-sas.txt

cmp consegne/UD04/01_DOCUMENTO_LAB.txt current-documento-sas.txt
```

I comandi di verifica della SAS non ritornano output, questo significa che il file è recuperabile integralmente.

Configurazione SAS:

- File: `current/documento.txt`;
- Durata: `15 minuti`;
- Permessi: `Lettura`;

## Diagnosi

Per ciascun errore separa sintomo, piano interessato, causa, controllo e correzione.

**Errore (A)**:

```txt
AuthorizationPermissionMismatch
```

- Sintomo: L'operazione viene rifiutata con codice di errore.

- Piano: Data Plane o Management Plane

- Causa: Le credenziali fornite sono valide, ma non dispongono dei permessi necessari per eseguire l'operazione.

- Controllo: Verificare i permessi assegnati all'identità che esegue la richiesta (o inclusi in una stringa SAS).

- Correzione: Assegnare il ruolo RBAC appropriato all'identità che esegue la richiesta  o rigenerare la firma SAS includendo i permessi necessari.

**Errore (B)**:

```txt
ResourceNotFound: The specified container does not exist
```

- Sintomo: La richiesta fallisce specificando che il container non esiste.

- Piano: Data Plane.

- Causa: Il container indicato nell'URI non esiste o è stato eliminato oppure il relativo nome contiene un errore di battitura.

- Controllo: Verificare la correttezza dell'URL o del percorso specificato nella richiesta; Verificare anche l'esistenza del container (`az storage container list`);

- Correzione: Se l'URL presenta errori correggerli; Se il container non esiste, crearlo da portale o con:
`az storage container create`

**Errore (C)**:

```txt
curl: (22) The requested URL returned error: 403
```

- Sintomo: Il comando `curl` ritorna un errore a causa del codice di stato HTTP 403 ritornato dal server.

- Piano: Data Plane

- Causa: Il server remoto ha ricevuto la richiesta ma rifiuta di servirla. La causa più probabile è che l'identità che esegue la richiesta non ha i permessi di accederci, questo può essere per via di permessi mancanti nell'URL SAS, o per una chiave segreta scaduta.

- Controllo: Verificare se l'URL punta ad una SAS scaduta o con permessi errati o mancanti; se si utilizza autenticazione via chiave, controllare la scadenza della chiave con `az storage account keys list`.

- Correzione: rigenerare la SAS con le autorizzazioni corrette e necessarie; rigenerare la chiave scaduta se ne è in uso una.

## Lifecycle, costi e cleanup

Spiega la relazione tra prefisso e lifecycle rule, indica i driver di costo e registra la verifica del cleanup.

Una regola di gestione lifecycle è un insieme di condizioni e azioni applicate ai BLOB, il prefisso funge da filtro di ambito (scope filter) all'interno della regola di lifecycle e permette di applicare una regola solo a uno specifico sottoinsieme di oggetti, una regola scoped per il contenitore `documents/temporary/` non si applicherà ad uno scope differente, i.e. `archive/current/document.txt`.
I driver di costo includono: la tier (hot/cool/cold/archive), passando da Hot ad Archive il costo per GB decresce progressivamente; passare da una tier ad un'altra comporta pure un costo; esiste anche una penale per le rimozioni anticipate; infine anche la valutazione e l'esecuzione giornaliera delle regole di lifecycle su milioni di piccoli oggetti genera costi operativi, correlati al volume di BLOB scansionati.

### Cleanup

#### Rimuovo i file temporanei e le variabili di ambiente

```bash
rm current-documento-sas.txt documento-sas.txt documento-lab-scaricato.txt ud04-temporaneo.txt

unset AZURE_STORAGE_KEY SAS_URL
az group show --name "$LAB_RG" --query "{Name:name,Tags:tags}" --output jsonc
{
  "Name": "rg-cea-storage-d13988a1",
  "Tags": {
    "course": "cloud-engineer-academy",
    "deleteAfter": "2026-10-16",
    "environment": "lab",
    "unit": "UD04"
  }
}
```

#### Verifico la rimozione del ruolo temporaneo

```bash
az storage blob list \
  --account-name "$LAB_STORAGE" \
  --container-name "$LAB_CONTAINER" \
  --auth-mode login \
  --query "[].{Blob:name,Tier:properties.blobTier,Bytes:properties.contentLength}" \
  --output table
```

Il comando ritorna errore di permessi, questo significa che l'assegnazione del ruolo `Storage Blob Data Contributor` è stata rimossa con successo.

#### Elimino il resource group (e con se lo storage account)

```bash
az group delete --name "$LAB_RG" --yes --no-wait
az group wait --name "$LAB_RG" --deleted
az group exists --name "$LAB_RG"
false
```

L'ultimo comando ritorna false, questo vuol dire che il resource group è stato eliminato.

#### Verifico l'eliminazione dello storage account

```bash
 az storage account show \
  --resource-group "$LAB_RG" \
  --name "$LAB_STORAGE" \
  --query "{Sku:sku.name,Kind:kind,Https:enableHttpsTrafficOnly,Tls:minimumTlsVersion,PublicBlob:allowBlobPublicAccess,BlobEndpoint:primaryEndpoints.blob}" \
  --output jsonc
(ResourceGroupNotFound) Resource group 'rg-cea-storage-d13988a1' could not be found.
Code: ResourceGroupNotFound
Message: Resource group 'rg-cea-storage-d13988a1' could not be found.
```

Il comando ritorna errore, questo significa che lo storage account è stato rimosso con successo.

## Risultato finale

- nessun segreto pubblicato: Confermato
- hash abbreviato e messaggio del commit: `ccb66e0` `UD04 Completa laboratorio guidato Azure Storage`
