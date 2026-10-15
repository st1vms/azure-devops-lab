# Consegna UD04 — Laboratorio guidato

## Contesto anonimizzato

- resource group: `rg-cea-storage-d13988a1`
- storage account: `stcead13988a1`
- region: `italynorth`
- tipo e ridondanza: `StorageV2`, `Standard_LRS`

## Servizi e configurazione

| Elemento | Configurazione | Motivazione |
|---|---|---|
| Blob container | Standard_LRS | Archiviazione di file temporanei con costi ridotti |
| access tier | Hot | Accesso frequente richiesto (> 1 volta al mese) |
| accesso pubblico | Disabilitato | Disabilitato per motivi di sicurezza |
| trasferimento/TLS | Abilitato | Richiesto per motivi di sicurezza |

## Autorizzazione e lifecycle

Documenta ruolo dati e scope, differenze tra Entra ID, Shared Key e SAS e configurazione della lifecycle rule senza riportare chiavi, SAS o URL firmate.

### Differenza tra Entra ID, Shared Key e SAS

Entra ID è l'approccio consigliato per l'autenticazione tramite utenti e gruppi usando permessi RBAC granulari. Una shared key da accesso completo e illimitato a tutto l'account e le operazioni, mentre una SAS è un URL con parametri firmati, ha una scadenza, e si utilizza quando è necessario un accesso ristretto temporaneo, senza la necessità di dover condividere le chiavi principali.

### Configurazione lifecycle rule

- Name: `delete-temporary`;
- Scope: `Limit blobs with filters`;
- Type: `Block blobs`;
- SubType: `Base blobs`;
- Condition: Delete if not modified in 1 day;
- Prefix: `documents/temporary/`;

## Verifiche, costi e cleanup

Riporta esiti essenziali, principali driver di costo, rimozione del ruolo temporaneo e verifica dell'eliminazione del resource group.

### Esiti essenziali

Creazione environment:

```bash
export LAB_SUFFIX="d13988a1"
export LAB_RG="rg-cea-storage-${LAB_SUFFIX}"
export LAB_STORAGE="stcea${LAB_SUFFIX}"
export LAB_CONTAINER="archive"
export LAB_LOCATION="italynorth"
export LAB_DELETE_AFTER="$(date -u -d '+1 day' +%F)"
```

Creazione Resource Group:

```bash
az group create \
  --name "$LAB_RG" \
  --location "$LAB_LOCATION" \
  --tags course=cloud-engineer-academy unit=UD04 environment=lab deleteAfter="$LAB_DELETE_AFTER" \
  --output table

Location    Name
----------  -----------------------
italynorth  rg-cea-storage-d13988a1
```

Creazione Storage Account:

```bash
az storage account create \
  --resource-group "$LAB_RG" \
  --name "$LAB_STORAGE" \
  --location "$LAB_LOCATION" \
  --sku Standard_LRS \
  --kind StorageV2 \
  --https-only true \
  --min-tls-version TLS1_2 \
  --allow-blob-public-access false \
  --tags course=cloud-engineer-academy unit=UD04 environment=lab deleteAfter="$LAB_DELETE_AFTER" \
  --output table

AccessTier    AllowBlobPublicAccess    CreationTime                      EnableHttpsTrafficOnly    Kind       Location    MinimumTlsVersion    Name           PrimaryLocation    ProvisioningState    ResourceGroup            StatusOfPrimary
------------  -----------------------  --------------------------------  ------------------------  ---------  ----------  -------------------  -------------  -----------------  -------------------  -----------------------  -----------------
Hot           False                    2026-10-15T08:26:04.368619+00:00  True                      StorageV2  italynorth  TLS1_2               stcead13988a1  italynorth         Succeeded            rg-cea-storage-d13988a1  availa
```

Verifica proprietà e endpoint:

```bash
 az storage account show \
  --resource-group "$LAB_RG" \
  --name "$LAB_STORAGE" \
  --query "{Sku:sku.name,Kind:kind,Https:enableHttpsTrafficOnly,Tls:minimumTlsVersion,PublicBlob:allowBlobPublicAccess,BlobEndpoint:primaryEndpoints.blob}" \
  --output jsonc
{
  "BlobEndpoint": "https://stcead13988a1.blob.core.windows.net/",
  "Https": true,
  "Kind": "StorageV2",
  "PublicBlob": false,
  "Sku": "Standard_LRS",
  "Tls": "TLS1_2"
}
```

Verifica del container del blob dopo aver aggiunto il ruolo `Storage Blob Data Contributor`:

```bash
az storage container list \
  --account-name "$LAB_STORAGE" \
  --auth-mode login \
  --query "[].{Container:name,PublicAccess:properties.publicAccess}" \
  --output table
Container
-----------
documents
```

```bash
az storage blob list   --account-name "$LAB_STORAGE"   --container-name "$LAB_CONTAINER"   --auth-mode login   --query "[].{Blob:name,Tier:properties.blobTier,Bytes:properties.contentLength}"   --output table
Blob                  Tier    Bytes
--------------------  ------  -------
01_DOCUMENTO_LAB.txt  Hot     49
```

Upload file temporaneo:

```bash
az storage blob upload \
  --account-name "$LAB_STORAGE" \
  --container-name "$LAB_CONTAINER" \
  --name temporary/temporaneo.txt \
  --file ud04-temporaneo.txt \
  --auth-mode login \
  --overwrite \
  --output table
Client_request_id                     Content_md5               Date                       LastModified               Request_id                            Request_server_encrypted    Version
------------------------------------  ------------------------  -------------------------  -------------------------  ------------------------------------  --------------------------  ----------
8efa0744-c874-11f1-8834-c87f5406fb07  g58VN8xr26W0SshiTr4DhQ==  2026-10-15T08:43:56+00:00  2026-10-15T08:43:56+00:00  3eaef73e-401e-0038-1881-5c34c3000000  True                        2026-04-06
```

Scaricamento blob:

```bash
az storage blob download \
  --account-name "$LAB_STORAGE" \
  --container-name "$LAB_CONTAINER" \
  --name 01_DOCUMENTO_LAB.txt \
  --file documento-lab-scaricato.txt \
  --auth-mode login \
  --overwrite \
  --output table
Name                  Blob Type    Blob Tier    Length    Content Type    Last Modified              Snapshot
--------------------  -----------  -----------  --------  --------------  -------------------------  ----------
01_DOCUMENTO_LAB.txt  BlockBlob                 49        text/plain      2026-10-15T08:32:36+00:00
```

Il comando `cmp` non ritorna output, questo significa che il file scaricato risulta uguale a quello caricato.

Dopo aver creato una chiave temporanea, la uso per leggere il container:

```bash
az storage blob list \
  --account-name "$LAB_STORAGE" \
  --container-name "$LAB_CONTAINER" \
  --auth-mode key \
  --query "[].name" \
  --output table
Result
------------------------
01_DOCUMENTO_LAB.txt
temporary/temporaneo.txt
```

Genero e uso una User Delegation SAS:

```bash
SAS_EXPIRY="$(date -u -d '+30 minutes' +%Y-%m-%dT%H:%MZ)"
SAS_URL="$(az storage blob generate-sas \
  --account-name "$LAB_STORAGE" \
  --container-name "$LAB_CONTAINER" \
  --name 01_DOCUMENTO_LAB.txt \
  --permissions r \
  --expiry "$SAS_EXPIRY" \
  --auth-mode login \
  --as-user \
  --full-uri \
  --output tsv)"
curl --fail --silent --show-error "$SAS_URL" --output documento-sas.txt
cmp consegne/UD04/01_DOCUMENTO_LAB.txt documento-sas.txt
```

Gli ultimi due comandi non ritornano output, questo significa che il file è stato scaricato correttamente ed è integro.
Il permesso è di lettura, lo scope è `/documents/01_DOCUMENTO_LAB.txt`, e dura per 30 minuti.

Verifico la creazione della regola lifecycle creata dal portale:

```bash
az storage account management-policy show \
  --account-name "$LAB_STORAGE" \
  --resource-group "$LAB_RG" \
  --query "policy.rules[].{Name:name,Enabled:enabled,Prefixes:definition.filters.prefixMatch,DeleteAfter:definition.actions.baseBlob.delete.daysAfterModificationGreaterThan}" \
  --output jsonc
[
  {
    "DeleteAfter": 1.0,
    "Enabled": true,
    "Name": "delete-temporary",
    "Prefixes": [
      "documents/temporary/"
    ]
  }
]
```

La lifecycle policy è stata creata con successo.

### Driver di costo

I driver di costo per Blob Storage includono: capacità di archiviazione, frequenza delle operazioni di lettura/scrittura/cancellazione/modifica, trasferimento dati verso altre regioni, e i servizi di data management utilizzati, come lifecycle management, versioning, snapshots, indexing e soft delete.

### Rimozione ruolo temporaneo

Verifico la rimozione del ruolo temporaneo:

```bash
az storage blob list \
  --account-name "$LAB_STORAGE" \
  --container-name "$LAB_CONTAINER" \
  --auth-mode login \
  --query "[].{Blob:name,Tier:properties.blobTier,Bytes:properties.contentLength}" \
  --output table
```

Il comando ritorna errore di permessi, questo significa che l'assegnazione del ruolo è stata rimossa con successo.

### Rimuovo i file temporanei e le variabili di ambiente

```bash
rm documento-sas.txt documento-lab-scaricato.txt ud04-temporaneo.txt

unset AZURE_STORAGE_KEY SAS_URL
```

### Elimino il resource group (e con se lo storage account)

```bash
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
az group delete --name "$LAB_RG" --yes --no-wait
az group wait --name "$LAB_RG" --deleted
az group exists --name "$LAB_RG"
false
```

L'ultimo comando ritorna false, questo vuol dire che il resource group è stato eliminato.

### Verifico l'eliminazione dello storage account

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

## Rilevanza professionale

Motiva una scelta tra Blob e Files e il relativo metodo di autorizzazione.

Utilizzerei Blob Storage per archiviazione di file non strutturati, come immagini, video o documenti grezzi, per l'accesso utilizzerei Microsoft Entra ID + RBAC per assegnare permessi granulari per l'accesso alle risorse. Utilizzerei Files se necessitassi di un file system condiviso (SMB/NFS), per l'autenticazione utilizzerei sempre Microsoft Entra o Active Directory Domain Services per la gestione dei permessi NTFS a livello di file e cartella.
