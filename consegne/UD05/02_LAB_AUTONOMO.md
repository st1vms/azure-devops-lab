# Consegna UD05 — Laboratorio autonomo

## Inventario iniziale

Riporta VNet, subnet, NIC, associazioni e regole in forma anonimizzata.

### Verifico l'esistenza della VNet creata nel laboratorio guidato

```bash
az network vnet show \
--resource-group "$LAB_RG" \
--name "$LAB_VNET" \
--query "{Name:name,Location:location,Address:addressSpace.addressPrefixes,Subnets:subnets[].{Name:name,Prefix:addressPrefixes},Tags:tags}" \
--output jsonc
{
  "Address": [
    "10.50.0.0/16"
  ],
  "Location": "italynorth",
  "Name": "vnet-cea-b31ccd",
  "Subnets": [
    {
      "Name": "snet-web",
      "Prefix": null
    },
    {
      "Name": "snet-data",
      "Prefix": null
    }
  ],
  "Tags": null
}
```

### Verifico l'esistenza di subnets, NIC e regole

```bash
az network vnet subnet list \
--resource-group "$LAB_RG" \
--vnet-name "$LAB_VNET" \
--output jsonc \
| sed -E 's#/subscriptions/[^/]+#/subscriptions/<omitted>#'
[
  {
    "addressPrefix": "10.50.10.0/24",
    "defaultOutboundAccess": false,
    "delegations": [],
    "etag": "W/\"b23c2935-b217-44a7-9d3d-dd89b4f5c6ae\"",
    "id": "/subscriptions/<omitted>/resourceGroups/rg-cea-network-b31ccd/providers/Microsoft.Network/virtualNetworks/vnet-cea-b31ccd/subnets/snet-web",
    "ipConfigurations": [
      {
        "id": "/subscriptions/<omitted>/resourceGroups/RG-CEA-NETWORK-B31CCD/providers/Microsoft.Network/networkInterfaces/NIC-WEB-01/ipConfigurations/IPCONFIG1",
        "resourceGroup": "RG-CEA-NETWORK-B31CCD"
      }
    ],
    "name": "snet-web",
    "privateEndpointNetworkPolicies": "Disabled",
    "privateLinkServiceNetworkPolicies": "Enabled",
    "provisioningState": "Succeeded",
    "resourceGroup": "rg-cea-network-b31ccd",
    "type": "Microsoft.Network/virtualNetworks/subnets"
  },
  {
    "addressPrefix": "10.50.20.0/24",
    "delegations": [],
    "etag": "W/\"b23c2935-b217-44a7-9d3d-dd89b4f5c6ae\"",
    "id": "/subscriptions/<omitted>/resourceGroups/rg-cea-network-b31ccd/providers/Microsoft.Network/virtualNetworks/vnet-cea-b31ccd/subnets/snet-data",
    "ipConfigurations": [
      {
        "id": "/subscriptions/<omitted>/resourceGroups/RG-CEA-NETWORK-B31CCD/providers/Microsoft.Network/networkInterfaces/NIC-DATA-01/ipConfigurations/IPV4CONFIG",
        "resourceGroup": "RG-CEA-NETWORK-B31CCD"
      }
    ],
    "name": "snet-data",
    "networkSecurityGroup": {
      "id": "/subscriptions/<omitted>/resourceGroups/rg-cea-network-b31ccd/providers/Microsoft.Network/networkSecurityGroups/nsg-data-b31ccd",
      "resourceGroup": "rg-cea-network-b31ccd"
    },
    "privateEndpointNetworkPolicies": "Disabled",
    "privateLinkServiceNetworkPolicies": "Enabled",
    "provisioningState": "Succeeded",
    "resourceGroup": "rg-cea-network-b31ccd",
    "type": "Microsoft.Network/virtualNetworks/subnets"
  }
]
```

```bash
az network nic show \
  --resource-group "$LAB_RG" \
  --name nic-data-01 \
  --query "{PrivateIp:ipConfigurations[0].privateIPAddress,Subnet:ipConfigurations[0].subnet.id,PublicIp:ipConfigurations[0].publicIPAddress}" \
  --output jsonc \
  | sed -E 's#/subscriptions/[^/]+#/subscriptions/<omitted>#'
{
  "PrivateIp": "10.50.20.4",
  "PublicIp": null,
  "Subnet": "/subscriptions/<omitted>/resourceGroups/rg-cea-network-b31ccd/providers/Microsoft.Network/virtualNetworks/vnet-cea-b31ccd/subnets/snet-data"
}
```

```bash
az network nsg rule list \
  --resource-group "$LAB_RG" \
  --nsg-name "$LAB_NSG" \
  --query "sort_by([].{Priority:priority,Name:name,Access:access,Source:sourceAddressPrefix,Port:destinationPortRange}, &Priority)" \
  --output table
Priority    Name                Access    Source         Port
----------  ------------------  --------  -------------  ------
300         Allow-Web-Postgres  Allow     10.50.10.0/24  5432
```

### Introduco la regola guasto

```bash
az network nsg rule create \
  --resource-group "$LAB_RG" \
  --nsg-name "$LAB_NSG" \
  --name Deny-Web-Postgres-Auto \
  --priority 250 \
  --direction Inbound \
  --access Deny \
  --protocol Tcp \
  --source-address-prefixes 10.50.10.0/24 \
  --destination-address-prefixes '*' \
  --destination-port-ranges 5432
{
  "access": "Deny",
  "destinationAddressPrefix": "*",
  "destinationAddressPrefixes": [],
  "destinationPortRange": "5432",
  "destinationPortRanges": [],
  "direction": "Inbound",
  "etag": "W/\"4ba8e440-8f5b-40bc-8f01-91eb5758ecca\"",
  "id": "/subscriptions/<omitted>/resourceGroups/rg-cea-network-b31ccd/providers/Microsoft.Network/networkSecurityGroups/nsg-data-b31ccd/securityRules/Deny-Web-Postgres-Auto",
  "name": "Deny-Web-Postgres-Auto",
  "priority": 250,
  "protocol": "Tcp",
  "provisioningState": "Succeeded",
  "resourceGroup": "rg-cea-network-b31ccd",
  "sourceAddressPrefix": "10.50.10.0/24",
  "sourceAddressPrefixes": [],
  "sourcePortRange": "*",
  "sourcePortRanges": [],
  "type": "Microsoft.Network/networkSecurityGroups/securityRules"
}
```

Verifico la presenza della regola:

```bash
az network nsg rule list \
  --resource-group "$LAB_RG" \
  --nsg-name "$LAB_NSG" \
  --query "sort_by([].{Priority:priority,Name:name,Access:access,Source:sourceAddressPrefix,Port:destinationPortRange}, &Priority)" \
  --output table
Priority    Name                    Access    Source         Port
----------  ----------------------  --------  -------------  ------
250         Deny-Web-Postgres-Auto  Deny      10.50.10.0/24  5432
300         Allow-Web-Postgres      Allow     10.50.10.0/24  5432
```

### Risposta domanda 5 (Attività)

L'assenza di una Virtual Machine impedisce un test IP Flow Verify completo perché lo strumento richiede un'interfaccia di rete specifica come target per simulare il traffico. Senza la VM e la relativa NIC, il sistema non può calcolare le regole di sicurezza effettive, che sono il risultato della combinazione dinamica delle policy applicate sia a livello Subnet sia a livello di singola interfaccia di rete.
Tuttavia, ciò non impedisce di individuare un conflitto di regole poiché le NSG sono risorse statiche e indipendenti. È possibile eseguire un'analisi di configurazione direttamente sull'NSG associato alla Subnet, esamindando la tabella delle regole per identificare eventuali sovrapposizioni o contraddizioni logiche, un'operazione che non richiede un'istanza computazionale attiva per essere verificata.

### Rimozione regola Deny e verifica regola Allow

```bash
az network nsg rule delete \
  --resource-group "$LAB_RG" \
  --nsg-name "$LAB_NSG" \
  --name Deny-Web-Postgres-Auto
```

Verifico:

```bash
az network nsg rule list \
  --resource-group "$LAB_RG" \
  --nsg-name "$LAB_NSG" \
  --query "sort_by([].{Priority:priority,Name:name,Access:access,Source:sourceAddressPrefix,Port:destinationPortRange}, &Priority)" \
  --output table
Priority    Name                Access    Source         Port
----------  ------------------  --------  -------------  ------
300         Allow-Web-Postgres  Allow     10.50.10.0/24  5432
```

Regola rimossa con successo.

## Guasto e diagnosi

- regola introdotta: `Deny-Web-Postgres-Auto`
- ordine di priorità osservato: La regola `Deny-Web-Postgres-Auto` (priorità 250) viene valutata prima della regola `Allow-Web-Postgres` (priorità 300) a causa del valore numerico inferiore.
- sintomo: Il livello web non può connettersi al database tramite la porta TCP 5432.
- ipotesi: Il blocco della comunicazione è causato dalla regola di Deny che intercetta e scarta il traffico prima che la regola di Allow possa autorizzarlo.
- controllo: Esecuzione di `az network nsg rule list` per confermare la sequenza di valutazione delle regole applicate all'NSG.
- correzione minima: Rimozione della regola `Deny-Web-Postgres-Auto` tramite CLI.
- verifica dopo la correzione: Lettura della tabella delle regole NSG per accertarsi che `Allow-Web-Postgres` sia diventata nuovamente la regola dominante per quel flusso.

### Analisi sintomi (quesito 7 in Attività)

- Sintomo:

```txt
InvalidAddressPrefix
```

- Livello: VNet o Subnet
- Controllo: Revisione formale del valore CIDR dichiarato per identificare errori di formattazione o di calcolo della subnet mask.
- Correzione minima: Inserire una notazione CIDR valida e coerente con lo spazio di indirizzamento allocato.

- Sintomo:

```txt
SecurityRuleConflict
```

- Livello: Network Security Group
- Controllo: Analisi statica della tabella delle regole per individuare duplicati, priorità identiche non valide o port range sovrapposti.
- Correzione minima: Variare il parametro di priorità assegnando un numero univoco oppure differenziare gli intervalli di porte/indirizzi.

- Sintomo:

```txt
un nome DNS non viene risolto
```

- Livello: Configurazione DNS
- Controllo: Interrogazione dei record DNS esistenti e ispezione dei server DNS associati alla VNet.
- Correzione minima: Creazione del record DNS appropriato o assegnazione del server DNS corretto nelle impostazioni della VNet.

- Sintomo:

```txt
la porta risulta filtrata da un NSG
```

- Livello: Subnet/NIC
- Controllo: Analisi delle regole NSG in Inbound/Outbound.
- Correzione minima: Creazione di una regola specifica di "Allow" per la porta e il protocollo di interesse, impostando una priorità sufficientemente alta da scavalcare la regola di blocco predefinita.

## Casi ulteriori

Distingui diagnosi di CIDR, DNS, routing, NSG e servizio non in ascolto, separando fatti osservati e prove non ancora eseguibili.

Allo stato attuale, i fatti osservati confermano la correttezza dei prefissi CIDR di VNet e subnet e permettono l'analisi statica delle regole NSG per individuare eventuali conflitti. Al contrario, le prove non ancora eseguibili includono la risoluzione DNS, il controllo del traffico tramite IP Flow Verify e la diagnosi di un eventuale servizio non in ascolto sulla porta 5432, poiché l'assenza temporanea delle macchine virtuali e dell'applicazione non consente di generare né testare il traffico reale di rete.

## Cleanup e risultato finale

- regola autonoma rimossa: Si
- cleanup verificato: Si
- hash abbreviato e messaggio del commit: `6e3f606` `UD05 Completa laboratorio guidato reti Azure e NSG`
