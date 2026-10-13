# Consegna UD02 — Laboratorio autonomo

## Requisito e piano

- requisito interpretato: Creare una rete isolata e uno spazio di archiviazione vuoto, l'ambiente deve rimanere separato dagli altri laboratori e deve poter essere eliminato come un'unica unità.
- risorse previste: `Resource Group`, `VNet`, `Storage Account`.
- nomi e tag scelti: `course=cloud-engineer-academy, unit=UD02, environment=dev, scenario=autonomous e deleteAfter`
- verifiche preliminari:

Verifico se la sottoscrizione è corretta e abilitata:

```bash
$ az account show \
  --query "{Name:name,State:state,IsDefault:isDefault}" \
  --output table
Name                  State    IsDefault
--------------------  -------  -----------
Azure subscription 1  Enabled  True
```

Verifico l'ambiente:

```bash
$ printf 'Location: %s\nRG: %s\nVNet: %s\nSubnet: %s\nStorage: %s\n' \
  "$AUTO_LOCATION" "$AUTO_RG" "$AUTO_VNET" "$AUTO_SUBNET" "$AUTO_STORAGE"
Location: italynorth
RG: rg-cea-ud02-auto-6636608c
VNet: vnet-cea-auto
Subnet: snet-workload
Storage: stceaauto6636608c
```

## Svolgimento

Riporta i passaggi essenziali, i controlli da portale e CLI e gli output anonimizzati che dimostrano il risultato.

## Diagnosi

- errore o anomalia analizzata: Nessuna
- ipotesi: -
- controllo: -
- correzione: -
- verifica successiva: -

## Cleanup e consegna

- risorse eliminate: 2
- controllo finale: Verificato
- hash abbreviato e messaggio del commit: 99a4f6a "UD02 Lab Guidato completato"

## Breve nota tecnica

Utilizzare il gruppo di risorse permette alle risorse di condividere il ciclo di vita, questo permetterà di eliminare tutte le risorse in un unico comando al termine del test.
La località è stata impostata su Italia del Nord sia per minimizzare la latenza operativa sul territorio, sia per mantenere la residenza dei dati entro i confini nazionali. La differenza tra VNet e Storage account è che VNet fornisce l'infrastruttura (IaaS) per isolare e instradare il traffico, mentre lo storage account opera come servizio (PaaS) che si occupa solo dell'archiviazione dei dati.
I tag servono a classicare le risorse per permettere di organizzarle meglio.
Per dimostrare il cleanup, userò il comando `az resource list`.

## Registro cronologico delle evidenze

Compila durante il lavoro. Per ogni fase riporta data/ora e contesto (WSL, Cloud Shell Bash, Cloud Shell PowerShell o Portal), comando/pagina, breve risultato anonimizzato e interpretazione. Non inserire output di esempio come prova reale. Registra anche controlli negati, attese e azioni non eseguite.

| Data/ora | Fase e contesto | Comando o pagina | Risultato reale ripulito | Interpretazione / passo successivo |
|---|---|---|---|---|

## 1) Creazione del gruppo di risorse

- Data/ora: 13/10/26 15:07
- Fase e contesto: Creazione del gruppo di risorse, Azure CLI.

- Comando/Pagina:

```bash
az group create --name "$AUTO_RG" --location "$AUTO_LOCATION" --tags course='cloud-
engineer-academy' unit='UD02' environment='dev' scenario='autonomous' deleteAfter="$AUTO_DELETE_AFTER" --output table
```

- Risultato:

```bash
Location    Name
----------  -------------------------
italynorth  rg-cea-ud02-auto-6636608c
```

- Interpretazione / passo successivo: Gruppo creato con successo, procedo con la creazione delle risorse.

## 2) Creazione della rete virtuale

- Data/ora: 13/10/26 15:13
- Fase e contesto: Creazione della rete virtuale, Azure CLI.

- Comando/Pagina:

```bash
az network vnet create --resource-group "$AUTO_RG" --name "$AUTO_VNET" --location "$AUTO_LOCATION" --address-prefixes '10.30.0.0/16' --subnet-name "$AUTO_SUBNET" --subnet-prefixes '10.30.10.0/24' --tags course='cloud-engineer-academy' unit='UD02' environment='dev' scenario='autonomous' deleteAfter="$AUTO_DELETE_AFTER" --output jsonc
```

- Risultato:

```bash
{
  "newVNet": {
    "addressSpace": {
      "addressPrefixes": [
        "10.30.0.0/16"
      ]
    },
    "enableDdosProtection": false,
    "etag": "W/\"9ea554be-db20-412e-9c49-3dce53933da7\"",
    "id": "/subscriptions/<omitted>/resourceGroups/rg-cea-ud02-auto-6636608c/providers/Microsoft.Network/virtualNetworks/vnet-cea-auto",
    "location": "italynorth",
    "name": "vnet-cea-auto",
    "privateEndpointVNetPolicies": "Disabled",
    "provisioningState": "Succeeded",
    "resourceGroup": "rg-cea-ud02-auto-6636608c",
    "resourceGuid": "<omitted>",
    "subnets": [
      {
        "addressPrefix": "10.30.10.0/24",
        "defaultOutboundAccess": false,
        "delegations": [],
        "etag": "W/\"9ea554be-db20-412e-9c49-3dce53933da7\"",
        "id": "/subscriptions/<omitted>/resourceGroups/rg-cea-ud02-auto-6636608c/providers/Microsoft.Network/virtualNetworks/vnet-cea-auto/subnets/snet-workload",
        "name": "snet-workload",
        "privateEndpointNetworkPolicies": "Disabled",
        "privateLinkServiceNetworkPolicies": "Enabled",
        "provisioningState": "Succeeded",
        "resourceGroup": "rg-cea-ud02-auto-6636608c",
        "type": "Microsoft.Network/virtualNetworks/subnets"
      }
    ],
    "tags": {
      "course": "cloud-engineer-academy",
      "deleteAfter": "2026-10-15",
      "environment": "dev",
      "scenario": "autonomous",
      "unit": "UD02"
    },
    "type": "Microsoft.Network/virtualNetworks",
    "virtualNetworkPeerings": []
  }
}
```

- Interpretazione / passo successivo: Rete virtuale creata con successo, procedo con la creazione dello storage account.

## 3 ) Creazione dello storage account

- Data/ora: 13/10/26 15:22
- Fase e contesto: Creazione dello storage account, Azure CLI.

- Comando/Pagina:

```bash
az storage account create --resource-group "$AUTO_RG" --name "$AUTO_STORAGE" --location "$AUTO_LOCATION" --kind StorageV2 --sku Standard_LRS --https-only true --min-tls-version TLS1_2 --allow-blob-public-access false --tags course='cloud-engineer-academy' unit='UD02' environment='dev' scenario='autonomous' deleteAfter="$AUTO_DELETE_AFTER" --output jsonc
```

- Risultato:

```bash
{
  "accessTier": "Hot",
  "accountMigrationInProgress": null,
  "allowBlobPublicAccess": false,
  "allowCrossTenantReplication": null,
  "allowSharedKeyAccess": null,
  "allowSharedKeyAccessForServices": null,
  "allowedCopyScope": null,
  "azureFilesIdentityBasedAuthentication": null,
  "blobRestoreStatus": null,
  "creationTime": "2026-10-13T13:30:47.237011+00:00",
  "customDomain": null,
  "dataCollaborationPolicyProperties": null,
  "defaultToOAuthAuthentication": null,
  "dnsEndpointType": null,
  "dualStackEndpointPreference": null,
  "enableExtendedGroups": null,
  "enableHttpsTrafficOnly": true,
  "enableNfsV3": null,
  "encryption": {
    "encryptionIdentity": null,
    "keySource": "Microsoft.Storage",
    "keyVaultProperties": null,
    "requireInfrastructureEncryption": null,
    "services": {
      "blob": {
        "enabled": true,
        "keyType": "Account",
        "lastEnabledTime": "2026-10-13T13:30:47.337136+00:00"
      },
      "file": {
        "enabled": true,
        "keyType": "Account",
        "lastEnabledTime": "2026-10-13T13:30:47.337136+00:00"
      },
      "queue": null,
      "table": null
    }
  },
  "extendedLocation": null,
  "failoverInProgress": null,
  "geoPriorityReplicationStatus": null,
  "geoReplicationStats": null,
  "id": "/subscriptions/<omitted>/resourceGroups/rg-cea-ud02-auto-6636608c/providers/Microsoft.Storage/storageAccounts/stceaauto6636608c",
  "identity": null,
  "immutableStorageWithVersioning": null,
  "isHnsEnabled": null,
  "isLocalUserEnabled": null,
  "isSftpEnabled": null,
  "isSkuConversionBlocked": null,
  "keyCreationTime": {
    "key1": "2026-10-13T13:30:47.326950+00:00",
    "key2": "2026-10-13T13:30:47.326950+00:00"
  },
  "keyPolicy": null,
  "kind": "StorageV2",
  "largeFileSharesState": null,
  "lastGeoFailoverTime": null,
  "location": "italynorth",
  "minimumTlsVersion": "TLS1_2",
  "name": "stceaauto6636608c",
  "networkRuleSet": {
    "bypass": "None",
    "defaultAction": "Allow",
    "ipRules": [],
    "ipv6Rules": [],
    "resourceAccessRules": null,
    "virtualNetworkRules": []
  },
  "placement": null,
  "primaryEndpoints": {
    ...
  },
  "primaryLocation": "italynorth",
  "privateEndpointConnections": [],
  "provisioningState": "Succeeded",
  "publicNetworkAccess": null,
  "resourceGroup": "rg-cea-ud02-auto-6636608c",
  "routingPreference": null,
  "sasPolicy": null,
  "secondaryEndpoints": null,
  "secondaryLocation": null,
  "sku": {
    "name": "Standard_LRS",
    "tier": "Standard"
  },
  "statusOfPrimary": "available",
  "statusOfSecondary": null,
  "storageAccountSkuConversionStatus": null,
  "systemData": null,
  "tags": {
    "course": "cloud-engineer-academy",
    "deleteAfter": "2026-10-15",
    "environment": "dev",
    "scenario": "autonomous",
    "unit": "UD02"
  },
  "type": "Microsoft.Storage/storageAccounts",
  "zones": null
}
```

- Interpretazione / passo successivo: Storage account creato con successo, procedo con il cleanup.

## 4) Cleanup e verifica

- Proprietà prima dell'eliminazione:

```txt
Location: italynorth
RG: rg-cea-ud02-auto-6636608c
VNet: vnet-cea-auto
Subnet: snet-workload
Storage: stceaauto6636608c
Cleanup entro: 2026-10-15
```

- Inventario prima dell'eliminazione:

```txt
Name                       ResourceGroup              Location    Type                               Status
-------------------------  -------------------------  ----------  ---------------------------------  ---------
NetworkWatcher_italynorth  NetworkWatcherRG           italynorth  Microsoft.Network/networkWatchers  Succeeded
vnet-cea-auto              rg-cea-ud02-auto-6636608c  italynorth  Microsoft.Network/virtualNetworks  Succeeded
stceaauto6636608c          rg-cea-ud02-auto-6636608c  italynorth  Microsoft.Storage/storageAccounts  Succeeded
```

- Richiesta di eliminazione:

```bash
az group delete --name "$AUTO_RG" --yes --no-wait
```

- Eseguo la richiesta di attesa:

```bash
az group wait --name "$AUTO_RG" --deleted
```

- La richiesta di attesa parte, e dopo aver aspettato ritorna senza output, verifico l'eliminazione:

```bash
az group exists --name "$AUTO_RG"
```

Il comando di verifica ritorna `false`, il gruppo di risorse è stato eliminato correttamente.

```bash
az resource list
[
  {
    "changedTime": "2026-10-13T10:48:50.852462+00:00",
    "createdTime": "2026-10-13T10:38:50.150547+00:00",
    "extendedLocation": null,
    "id": "/subscriptions/<omitted>/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkWatchers/NetworkWatcher_italynorth",
    "identity": null,
    "kind": null,
    "location": "italynorth",
    "managedBy": null,
    "name": "NetworkWatcher_italynorth",
    "plan": null,
    "properties": null,
    "provisioningState": "Succeeded",
    "resourceGroup": "NetworkWatcherRG",
    "sku": null,
    "tags": null,
    "type": "Microsoft.Network/networkWatchers"
  }
]
```

Il comando `az resource list` conferma l'eliminazione delle risorse.

## Citazione commit

[99a4f6a197342d675b9d97b0ba2fea25d2b2c54f](https://github.com/st1vms/azure-devops-lab/commit/99a4f6a197342d675b9d97b0ba2fea25d2b2c54f)

---

Riporta le proprietà e l'inventario prima dell'eliminazione, poi richiesta, attesa e assenza finale. Per il guidato includi il confronto CLI/Azure PowerShell; per l'autonomo motivazioni e requisiti. Nella conferma finale cita un commit già pubblicato, non l'hash del documento che stai ancora modificando.

## Autovalutazione

Indica `Completato` oppure `Da ripetere`.

| Capacità | Valutazione |
|---|---|
| Traduco requisiti in nomi, tag e risorse | Completato |
| Verifico account e località prima della creazione | Completato |
| Interpreto le proprietà di VNet e storage | Completato |
| Confronto portale e CLI | Completato |
| Anonimizzo gli identificativi | Completato |
| Diagnostico una variabile o un nome errato | Completato |
| Verifico la conclusione del cleanup | Completato |
