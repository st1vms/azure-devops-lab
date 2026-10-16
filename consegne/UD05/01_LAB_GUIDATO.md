# Consegna UD05 — Laboratorio guidato

Flusso previsto:

```txt
10.50.10.0/24:any -> 10.50.20.0/24:5432 TCP
```

Configurazione NSG e associazioni verificate; prova del flusso rinviata alla UD06.

## Piano di indirizzamento

| Elemento | CIDR | Scopo | Sovrapposizioni |
|---|---|---|---|
| VNet | 10.50.0.0/16 | Indirizzamento principale | Nessuna, contiene web e data |
| subnet web | 10.50.10.0/24 | Server Web | Nessuna, contenuta in VNet |
| subnet data | 10.50.20.0/24 | Database | Nessuna, contenuta in VNet |

## NSG e associazioni

| NSG | Scope associato | Regola | Priorità | Origine | Porta | Esito |
| --- | --- | --- | --- | --- | --- | --- |
| `nsg-data` | `snet-data` | `Allow-Web-Postgres` | `300` | `10.50.10.0/24` | `5432` | `Allow` |

## Verifica della configurazione

- NIC create e subnet: Confermato
- NSG associato alla subnet e regole osservate: Confermato
- Route table associata alla subnet (o assente): Confermato
- ciò che è stato verificato: NSG, subnet, regole, NIC e configurazioni di routing.
- report effettivi e test di flusso rinviati alla UD06: Si

## Costi e cleanup

Registra risorse create, possibili costi, eliminazione e verifica finale.

### Creazione gruppo di risorse

```bash
az group create --name "$LAB_RG" --location "$LAB_LOCATION" \
  --tags course=cloud-engineer-academy unit=UD05 environment=lab --output table
Location    Name
----------  ---------------------
italynorth  rg-cea-network-b31ccd
```

### Creazione VNet

```bash
az network vnet create \
  --resource-group "$LAB_RG" \
  --name "$LAB_VNET" \
  --location "$LAB_LOCATION" \
  --address-prefixes 10.50.0.0/16 \
  --subnet-name snet-web \
  --subnet-prefixes 10.50.10.0/24 \
  --output table
```

### Creazione SubNet

```bash
az network vnet subnet create \
  --resource-group "$LAB_RG" \
  --vnet-name "$LAB_VNET" \
  --name snet-data \
  --address-prefixes 10.50.20.0/24 \
  --output table
AddressPrefix    Name       PrivateEndpointNetworkPolicies    PrivateLinkServiceNetworkPolicies    ProvisioningState    ResourceGroup
---------------  ---------  --------------------------------  -----------------------------------  -------------------  ---------------------
10.50.20.0/24    snet-data  Disabled                          Enabled                              Succeeded            rg-cea-network-b31ccd
```

### Creazione NSG dal portale

Configurazione:

| Campo | Valore |
|---|---|
| Source | IP Addresses |
| Source IP/CIDR | `10.50.10.0/24` |
| Source port ranges | `*` |
| Destination | Any |
| Service | Custom |
| Destination port | `5432` |
| Protocol | TCP |
| Action | Allow |
| Priority | `300` |
| Name | `Allow-Web-Postgres` |

Verifica da CLI

```bash
az network nsg rule show \
  --resource-group "$LAB_RG" \
  --nsg-name "$LAB_NSG" \
  --name Allow-Web-Postgres \
  --query "{Priority:priority,Direction:direction,Access:access,Protocol:protocol,Source:sourceAddressPrefix,Port:destinationPortRange}" \
  --output jsonc
{
  "Access": "Allow",
  "Direction": "Inbound",
  "Port": "5432",
  "Priority": 300,
  "Protocol": "TCP",
  "Source": "10.50.10.0/24"
}
```

### Verifica associazione subnet a NSG

```bash
az network vnet subnet show \
  --resource-group "$LAB_RG" \
  --vnet-name "$LAB_VNET" \
  --name snet-data \
  --query "{Prefix:addressPrefix,Nsg:networkSecurityGroup.id}" \
  --output jsonc \
  | sed -E 's#/subscriptions/[^/]+#/subscriptions/<omitted>#'
{
  "Nsg": "/subscriptions/<omitted>/resourceGroups/rg-cea-network-b31ccd/providers/Microsoft.Network/networkSecurityGroups/nsg-data-b31ccd",
  "Prefix": "10.50.20.0/24"
}
```

### Verifica creazione NIC

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

### Creazione seconda NIC da CLI

```bash
az network nic create \
  --resource-group "$LAB_RG" \
  --name nic-web-01 \
  --vnet-name "$LAB_VNET" \
  --subnet snet-web \
  --location "$LAB_LOCATION" \
  --output table
```

Verifico:

```bash
az network nic show \
  --resource-group "$LAB_RG" \
  --name nic-web-01 \
  --query "{PrivateIp:ipConfigurations[0].privateIPAddress,Subnet:ipConfigurations[0].subnet.id,PublicIp:ipConfigurations[0].publicIPAddress}" \
  --output jsonc \
  | sed -E 's#/subscriptions/[^/]+#/subscriptions/<omitted>#'
{
  "PrivateIp": "10.50.10.4",
  "PublicIp": null,
  "Subnet": "/subscriptions/<omitted>/resourceGroups/rg-cea-network-b31ccd/providers/Microsoft.Network/virtualNetworks/vnet-cea-b31ccd/subnets/snet-web"
}
```

### Lettura regole personalizzate

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

### Introduzione e correzione di un guasto di priorità

```bash
az network nsg rule create \
  --resource-group "$LAB_RG" \
  --nsg-name "$LAB_NSG" \
  --name Deny-Web-Postgres \
  --priority 200 \
  --direction Inbound \
  --access Deny \
  --protocol Tcp \
  --source-address-prefixes 10.50.10.0/24 \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 5432 \
  --description "Guasto didattico: nega il flusso previsto" \
  --output table
Access    Description                                DestinationAddressPrefix    DestinationPortRange    Direction    Name               Priority    Protocol    ProvisioningState    ResourceGroup          SourceAddressPrefix    SourcePortRange
--------  -----------------------------------------  --------------------------  ----------------------  -----------  -----------------  ----------  ----------  -------------------  ---------------------  ---------------------  -----------------
Deny      Guasto didattico: nega il flusso previsto  *                           5432                    Inbound      Deny-Web-Postgres  200         Tcp         Succeeded            rg-cea-network-b31ccd  10.50.10.0/24          *
```

```bash
az network nsg rule list \
  --resource-group "$LAB_RG" \
  --nsg-name "$LAB_NSG" \
  --query "sort_by([].{Priority:priority,Name:name,Access:access,Source:sourceAddressPrefix,Port:destinationPortRange}, &Priority)" \
  --output table
Priority    Name                Access    Source         Port
----------  ------------------  --------  -------------  ------
200         Deny-Web-Postgres   Deny      10.50.10.0/24  5432
300         Allow-Web-Postgres  Allow     10.50.10.0/24  5432
```

Correggo l'errore rimuovendo la regola di guasto:

```bash
az network nsg rule delete \
  --resource-group "$LAB_RG" \
  --nsg-name "$LAB_NSG" \
  --name Deny-Web-Postgres
```

Verifico l'eliminazione:

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

### Costi introdotti

Le risorse di rete di base create in questa configurazione (VNet, NSG, NIC) non comportano costi diretti.

### Cleanup

### Rimozione del resource group

```bash
az group delete --name "$LAB_RG" --yes --no-wait
az group wait --name "$LAB_RG" --deleted
az group exists --name "$LAB_RG"
```

L'ultimo comando ritorna `false`, questo significa che il resource group è stato eliminato con successo.
Verifico l'eliminazione delle risorse.

VNet:

```bash
az network vnet show \
--resource-group "$LAB_RG" \
--name "$LAB_VNET" \
--query "{Name:name,Location:location,Address:addressSpace.addressPrefixes,Subnets:subnets[].{Name:name,Prefix:addressPrefixes},Tags:tags}" \
--output jsonc
(ResourceGroupNotFound) Resource group 'rg-cea-network-b31ccd' could not be found.
Code: ResourceGroupNotFound
Message: Resource group 'rg-cea-network-b31ccd' could not be found.
```

NSG:

```bash
az network nsg rule show \
  --resource-group "$LAB_RG" \
  --nsg-name "$LAB_NSG" \
  --name Allow-Web-Postgres \
  --query "{Priority:priority,Direction:direction,Access:access,Protocol:protocol,Source:sourceAddressPrefix,Port:destinationPortRange}" \
  --output jsonc
(ResourceGroupNotFound) Resource group 'rg-cea-network-b31ccd' could not be found.
Code: ResourceGroupNotFound
Message: Resource group 'rg-cea-network-b31ccd' could not be found.
```

NIC:

```bash
az network nic show \
  --resource-group "$LAB_RG" \
  --name nic-data-01 \
  --query "{PrivateIp:ipConfigurations[0].privateIPAddress,Subnet:ipConfigurations[0].subnet.id,PublicIp:ipConfigurations[0].publicIPAddress}" \
  --output jsonc \
  | sed -E 's#/subscriptions/[^/]+#/subscriptions/<omitted>#'
ERROR: (ResourceGroupNotFound) Resource group 'rg-cea-network-b31ccd' could not be found.
Code: ResourceGroupNotFound
Message: Resource group 'rg-cea-network-b31ccd' could not be found.
```

Tutte le risorse sono state eliminate con successo.

## Rilevanza professionale

Spiega perché progettazione CIDR e controllo delle regole devono precedere il deployment dei workload.

La progettazione del CIDR e il controllo delle regole devono precedere il deployment dei workload perché correggere l'indirizzamento di rete dopo l'integrazione delle risorse può richiedere migrazioni complesse. Inoltre, l'associazione preventiva dei NSG alle subnet applica una baseline di sicurezza univoca a tutte le interfacce di rete che verranno successivamente collegate, evitando così configurazioni individali incoerenti.
