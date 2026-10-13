# Consegna UD02 — Laboratorio guidato

## Contesto verificato

- Azure Portal accessibile: Si
- Azure CLI autenticata: Si
- sottoscrizione corretta verificata senza pubblicarne l'ID: Si
- località scelta e motivo: Italia del nord, scelta del professore.

## Ambiente creato

| Elemento | Nome tecnico | Tipo | Località | Scopo |
|---|---|---|---|---|
| Resource group | rg-cea-ud02-9eb9d8e5 | Resource group | italynorth | Organizzare risorse |
| Rete virtuale | vnet-cea-ud02 | Rete virtuale | italynorth | Gestire la rete |
| Storage account | stcea9eb9d8e5 | Storage account | italynorth | Gestire i database |

## Decisioni e verifiche

Descrivi perché le risorse appartengono allo stesso resource group, quali responsabilità rimangono al cliente, perché sono stati applicati nomi e tag e quale differenza hai osservato tra portale e CLI. Riporta soltanto comandi essenziali e output anonimizzati.

### Risposta

Le risorse appartengono allo stesso resource group per poterle organizzare in un contenitore logico che condivide lo stesso ciclo di vita, le risorse così nascono e muoiono insieme per lo stesso scopo. Il cliente è comunque responsabile della gestione dei dati, degli accessi e della sicurezza dei dispositivi che si connettono.
Il portale offre una navigazione intuitiva per esplorare tutte le funzionalità, mentre la CLI permette di eseguire subito operazioni complesse, come la registrazione ad un provider o l'eliminazione di un gruppo.

## Cleanup

- operazione di eliminazione: [Qui](#eliminazione-inventario)
- controllo utilizzato: [Qui](#eliminazione-inventario)
- risultato finale: [Qui](#eliminazione-inventario)
- eventuale anomalia e soluzione: Nessuna

## Rilevanza professionale

Spiega come inventario, tag e verifica del cleanup rendono una procedura ripetibile e controllabile.

## Registro cronologico delle evidenze

Compila durante il lavoro. Per ogni fase riporta data/ora e contesto (WSL, Cloud Shell Bash, Cloud Shell PowerShell o Portal), comando/pagina, breve risultato anonimizzato e interpretazione. Non inserire output di esempio come prova reale. Registra anche controlli negati, attese e azioni non eseguite.

| Data/ora | Fase e contesto | Comando o pagina | Risultato reale ripulito | Interpretazione / passo successivo |

### 1) Verifica contesto locale

- Data/ora: 13/10/26 11:30
- Fase e contesto: Verifica contesto locale, Bash.
- Comando/Pagina:

```bash
az account show \
  --query "{Name:name,State:state,IsDefault:isDefault}" \
  --output table
```

- Risultato:

```txt
Name                  State    IsDefault
--------------------  -------  -----------
Azure subscription 1  Enabled  True
```

- Interpretazione/passo successivo: Sottoscrizione di default selezionata correttamente e abilitata. Prossimo passo: verificare i provider.

### 2) Verifica località e provider

- Data/ora: 13/10/26 11:31
- Fase e contesto: Verifica località e provider, Bash.
- Comando/Pagina:

```bash
az account list-locations \
  --query "[?name=='italynorth'].{Name:name,DisplayName:displayName}" \
  --output table

az provider show \
  --namespace Microsoft.Network \
  --query "{Namespace:namespace,State:registrationState}" \
  --output table

az provider show \
  --namespace Microsoft.Storage \
  --query "{Namespace:namespace,State:registrationState}" \
  --output table

# Providers non registrati, si procede a registrarli
az provider register --namespace Microsoft.Network --wait
az provider register --namespace Microsoft.Storage --wait
```

- Risultato:

```txt
Name        DisplayName
----------  -------------
italynorth  Italy North
```

- Interpretazione/passo successivo: I providers necessitavano di registrazione e la località Italia del Nord
è disponibile. Procedo con la preparazione environment (nomi e tag).

### 3) Preparazione environment

- Data/ora: 13/10/26 11:40
- Fase e contesto: Preparazione environment, Bash.

- Comando/Pagina:

```bash
source consegne/UD02/01_VARIABILI_LAB.sh

printf 'Località: %s\nRG: %s\nVNet: %s\nSubnet: %s\nStorage: %s\nCleanup entro: %s\n' \
  "$LAB_LOCATION" "$LAB_RG" "$LAB_VNET" "$LAB_SUBNET" \
  "$LAB_STORAGE" "$LAB_DELETE_AFTER"
```

- Risultato:

```txt
Località: italynorth
RG: rg-cea-ud02-9eb9d8e5
VNet: vnet-cea-ud02
Subnet: snet-app
Storage: stcea9eb9d8e5
Cleanup entro: 2026-10-15
```

- Interpretazione/prossimo passo: Proprietà configurate nell'environment, procedo con la creazione del resource group dal portale.

### 4) Creazione resource group

Data/ora: 13/10/26 11:45

Fase e contesto: Creazione resource group, Portale.

Comando/Pagina: `https://portal.azure.com/#servicemenu/Microsoft_Azure_Resources/ResourceManager/resourcegroups`

Risultato:

```txt
$ az group show \
  --name "$LAB_RG" \
  --query "{Name:name,Location:location,State:properties.provisioningState,Tags:tags}" \
  --output jsonc
{
  "Location": "italynorth",
  "Name": "rg-cea-ud02-9eb9d8e5",
  "State": "Succeeded",
  "Tags": {
    "course": "cloud-engineer-academy",
    "deleteAfter": "2026-10-15",
    "environment": "lab",
    "unit": "UD02"
  }
}
```

Interpretazione/prossimo step: Resource group creato correttamente. Procedo con la creazione della rete virtuale

### 5) Creazione rete virtuale

Data/ora: 13/10/26 11:55

Fase e contesto: Creazione della rete virtuale, Portale

Comando/Pagina: `https://portal.azure.com/#servicemenu/Microsoft_Azure_Network/NetworkFoundation/virtualnetworks`

Risultato:

```bash
az network vnet show \
--resource-group "$LAB_RG" \
--name "$LAB_VNET" \
--query "{Name:name,Location:location,Address:addressSpace.addressPrefixes,Subnets:subnets[].{Name:name,Prefix:addressPrefixes},Tags:tags}" \
--output jsonc

{
  "Address": [
    "10.20.0.0/16"
  ],
  "Location": "italynorth",
  "Name": "vnet-cea-ud02",
  "Subnets": [
    {
      "Name": "snet-app",
      "Prefix": [
        "10.20.1.0/24"
      ]
    }
  ],
  "Tags": {
    "course": "cloud-engineer-academy",
    "deleteAfter": "2026-10-15",
    "environment": "lab",
    "unit": "UD02"
  }
}
```

Interpretazione/prossimo step: Rete virtuale creata con successo, procedo con la creazione dello storage account

### 6) Creazione storage account

Data/ora: 13/10/26 12:10

Fase e contesto: Creazione dello storage account, Portale.

Comando/Pagina: `https://portal.azure.com/#browse/Microsoft.ClassicStorage%2FStorageAccounts`

Risultato:

```bash
az storage account show \
  --resource-group "$LAB_RG" \
  --name "$LAB_STORAGE" \
  --query "{Name:name,Location:location,Kind:kind,Sku:sku.name,HttpsOnly:enableHttpsTrafficOnly,MinimumTls:minimumTlsVersion,PublicBlobAccess:allowBlobPublicAccess,State:provisioningState,Tags:tags}" \
  --output jsonc

{
  "HttpsOnly": true,
  "Kind": "StorageV2",
  "Location": "italynorth",
  "MinimumTls": "TLS1_2",
  "Name": "stcea9eb9d8e5",
  "PublicBlobAccess": false,
  "Sku": "Standard_LRS",
  "State": "Succeeded",
  "Tags": {
    "course": "cloud-engineer-academy",
    "deleteAfter": "2026-10-15",
    "environment": "lab",
    "unit": "UD02"
  }
}
```

Interpretazione/prossimo step: Storage account creato corretamente, procedo con la costruzione dell'inventario.

### 7) Costruzione inventario

Data/ora: 13/10/26 12:25

Fase e contesto: Costruzione dell'inventario. Bash.

Comando/Pagina:

```bash
$ az resource list \
  --resource-group "$LAB_RG" \
  --query "[].id" \
  --output tsv \
  | sed -E 's#/subscriptions/[^/]+#/subscriptions/<omitted>#'
```

Risultato:

```txt
/subscriptions/<omitted>/resourceGroups/rg-cea-ud02-9eb9d8e5/providers/Microsoft.Network/virtualNetworks/vnet-cea-ud02
/subscriptions/<omitted>/resourceGroups/rg-cea-ud02-9eb9d8e5/providers/Microsoft.Storage/storageAccounts/stcea9eb9d8e
```

Interpretazione/prossimo step: L'inventario è stato corretamente creato. Procedo con l'eliminazione delle gruppo di risorse.

### Output Comandi Sezione 9A

- Comandi in Bash:

```bash
$ az version
{
  "azure-cli": "2.90.0",
  "azure-cli-core": "2.90.0",
  "azure-cli-telemetry": "1.1.0",
  "extensions": {
    "ml": "2.45.0",
    "ssh": "2.0.9"
  }
}
$ az account show --query "{Name:name,State:state,IsDefault:isDefault}" --output table
Name                  State    IsDefault
--------------------  -------  -----------
Azure subscription 1  Enabled  True
```

- Powershell commands:

```powershell
> Get-Module -ListAvailable Az.Resources | Select-Object Name,Version

Name         Version
----         -------
Az.Resources 10.2.0

> Get-AzContext | Select-Object @{Name='SubscriptionName';Expression={$_.Subscription.Name}}

SubscriptionName
----------------
Azure subscription 1

> Get-AzResourceGroup -Name 'rg-cea-ud02-9eb9d8e5' | Select-Object ResourceGroupName,Location,ProvisioningState

ResourceGroupName    Location   ProvisioningState
-----------------    --------   -----------------
rg-cea-ud02-9eb9d8e5 italynorth Succeeded
```

```powershell
> az group show -n 'rg-cea-ud02-9eb9d8e5'
{
  ...
  "location": "italynorth",
  "managedBy": null,
  "name": "rg-cea-ud02-9eb9d8e5",
  "properties": {
    "provisioningState": "Succeeded"
  },
  ...
}
```

### Risposta alla sezione 9 (Confronto portale e CLI)

Il portale consente di esplorare tutte le funzionalità, prendendosi il tempo necessario per esaminare ogni opzione e visualizzare i suggerimenti utili, che risultano molto più pratici per gestire le prime operazioni complesse, come creare un network account o uno storage account. Una volta compresi i processi e consolidate le configurazioni da utilizzare, è possibile procedere all'automazione tramite la CLI, che velocizza le operazioni.

---

Riporta le proprietà e l'inventario prima dell'eliminazione, poi richiesta, attesa e assenza finale. Per il guidato includi il confronto CLI/Azure PowerShell; per l'autonomo motivazioni e requisiti. Nella conferma finale cita un commit già pubblicato, non l'hash del documento che stai ancora modificando.

### Eliminazione inventario

- Proprietà prima dell'eliminazione:

```txt
Località: italynorth
RG: rg-cea-ud02-9eb9d8e5
VNet: vnet-cea-ud02
Subnet: snet-app
Storage: stcea9eb9d8e5
Cleanup entro: 2026-10-15
```

- Inventario prima dell'eliminazione:

```txt
/subscriptions/<omitted>/resourceGroups/rg-cea-ud02-9eb9d8e5/providers/Microsoft.Network/virtualNetworks/vnet-cea-ud02
/subscriptions/<omitted>/resourceGroups/rg-cea-ud02-9eb9d8e5/providers/Microsoft.Storage/storageAccounts/stcea9eb9d8e5
```

- Richiesta di eliminazione:

```bash
az group delete --name "$LAB_RG" --yes --no-wait
```

- Eseguo la richiesta di attesa:

```bash
az group wait --name "$LAB_RG" --deleted
```

- La richiesta di attesa parte, e dopo aver aspettato ritorna senza output, verifico l'eliminazione:

```bash
az group exists --name "$LAB_RG"
```

Il comando di verifica ritorna `false`, il gruppo di risorse è stato eliminato correttamente.
